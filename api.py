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
            url=API_HOST + '/user/register',
            data={
                'username': username,
                'password_hash': password_hash,
                'im_id': im_id,
                'api_key': API_KEY
            }
    ) as response:
        return await response.json()


async def update_password(
        user_identifier: str | int,
        password_hash: str,
        im_id: int,
):
    async with request(
            method='POST',
            url=API_HOST + f'/user/{user_identifier}/update_password',
            data={
                'password_hash': password_hash,
                'api_key': API_KEY,
                'im_id': im_id
            }
    ) as response:
        return await response.json()


async def user_info(
        user_identifier: str | int
):
    async with request(
            method='POST',
            url=API_HOST + f'/user/{user_identifier}/info',
    ) as response:
        return await response.json()
