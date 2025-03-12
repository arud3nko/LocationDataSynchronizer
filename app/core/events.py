"""This module contains Event and EventManager classes"""

import functools

from typing import MutableMapping, List, Any
from collections.abc import Callable


class Event:
    """
    This class contains simple event logic according to **observer** pattern.
    Can be used to provide **side effects** on any functions or methods.
    Every instance of this class contains list of subscribers (handlers).
    When being triggered, this event runs all handlers with args & kwargs,
    provided into trigger method.
    """

    def __init__(self):
        """Construct without additional arguments"""

        self._handlers: List[Callable[[Any, ...], Any]] = []

    def subscribe(self, handler: Callable[[Any, ...], Any]):
        """
        Appends provided handler to event's handlers list.

        :param handler: Callable handler
        """

        self._handlers.append(handler)

    def trigger(self, *args, **kwargs):
        """Run event's handlers"""

        for handler in self._handlers:
            handler(*args, **kwargs)


class EventManager:
    """
    This class contains `events` class variable, that contains all created events.
    Additionally, this class contains `event` method - unified way to add event
    on async function simply using decorator.
    """

    events: MutableMapping[str, Event] = {}

    @classmethod
    def event(cls, name: str):
        """
        This method creates & registers new event with provided name on provided function.

        :param name: Event name
        """

        cls.events[name] = Event()

        def inner(func):
            """Creates function wrapper"""
            @functools.wraps(func)
            async def wrapper(*args, **kwargs):
                """
                Runs function & triggers its events,
                if any event is registered for this function.

                Returns function result.
                """
                result = await func(*args, **kwargs)
                cls.events[name].trigger(result)
                return result

            return wrapper

        return inner
