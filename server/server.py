"""This module contains a test server functionality"""

import random

from aiohttp import web
from aiohttp.web_request import Request
from aiohttp.web_response import Response

from server_auth import BasicAuthMiddleware

MIN_INDEXES = 50000
MAX_INDEXES = 50000

MIN_INDEX_VALUE = 0
MAX_LAC_VALUE = 0xFFFF
MAX_CELLID_VALUE = 0xFFFF
MAX_ECI_VALUE = 0xFFFFFFF


def generate_random_value(min_value, max_value) -> int | None:
    return random.choice([None, random.randint(min_value, max_value)])


def generate_index():
    return {
        "lac": generate_random_value(min_value=MIN_INDEX_VALUE, max_value=MAX_LAC_VALUE),
        "cellid": generate_random_value(min_value=MIN_INDEX_VALUE, max_value=MAX_CELLID_VALUE),
        "eci": generate_random_value(min_value=MIN_INDEX_VALUE, max_value=MAX_ECI_VALUE),
    }


def generate_indexes_list():
    return [generate_index() for _ in range(random.randint(MIN_INDEXES, MAX_INDEXES))]


async def get_indexes(_request: Request) -> Response:
    indexes = generate_indexes_list()
    return web.json_response(data=indexes)


def main():

    auth_middleware = BasicAuthMiddleware(username="admin", password="admin")

    app = web.Application(middlewares=[auth_middleware])
    app.add_routes([web.get('/indexes', get_indexes)])

    web.run_app(app)


if __name__ == '__main__':
    main()
