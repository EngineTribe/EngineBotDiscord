# Engine Tribe API wrapper

from aiohttp import request
from config import *


async def user_register(
        username: str,
        im_id: int,
        password_hash: str,
):
    async with request(
            method='POST',
            url=API_HOST + '/user/update_password',
            json={'username': username,
                  'password_hash': password_hash,
                  'user_id': im_id,
                  'api_key': API_KEY}
    ) as response:
        return await response.json()


async def user_info(
        user_identifier: str
):
    async with request(
            method='POST',
            url=API_HOST + f'/user/{user_identifier}/info',
    ) as response:
        return await response.json()
