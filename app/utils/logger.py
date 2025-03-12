import logging
import sys

from queue import Queue
from logging.handlers import QueueHandler, QueueListener


def create_queue_logger(name: str) -> logging.Logger:
    """
    Configures logger with QueueHandler.
    QueueListener is used to log to stdout in separate thread to avoid blocking.

    :param name:
    :return:
    """

    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.INFO)

    formatter = logging.Formatter(
        fmt="%(asctime)s.%(msecs)03d %(levelname)s %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    handler.setFormatter(formatter)

    logging_queue = Queue(-1)
    queue_handler = QueueHandler(logging_queue)
    listener = QueueListener(logging_queue, handler)
    listener.start()

    logger.addHandler(queue_handler)
    logger.propagate = False

    return logger
