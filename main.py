import nextcord
from nextcord import (
    Interaction,
    File,
    Embed
)
from nextcord.ext import commands

import asyncio

from fastapi import FastAPI
import uvicorn, contextlib, time
from threading import Thread
from models import (
    UploadRequestBody,
    UploadResponseBody
)
from io import BytesIO

from config import *
import api
from activates import (
    Register
)
from locales import (
    get_locale_model
)

bot = commands.Bot(intents=nextcord.Intents.all(), command_prefix='/')


@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')


@bot.slash_command(
    description="Register in SMM:WE (Engine Tribe)",
    guild_ids=GUILD_IDS,

)
async def register(interaction: Interaction):
    locale_model = get_locale_model(interaction.user.roles)
    user_info_response = await api.user_info(user_identifier=str(interaction.user.id))
    if 'error_type' in user_info_response:
        await interaction.response.send_modal(
            Register(
                locale_model=locale_model
            )
        )
    else:
        await interaction.send(
            locale_model.ALREADY_REGISTERED
        )


@bot.slash_command(
    description="Change password",
    guild_ids=GUILD_IDS,
)
async def password(interaction: Interaction):
    locale_model = get_locale_model(interaction.user.roles)
    user_info_response = await api.user_info(user_identifier=str(interaction.user.id))
    if 'error_type' in user_info_response:
        await interaction.send(
            locale_model.NOT_REGISTERED
        )
    else:
        pass  # TODO


@bot.slash_command(
    description="Get user's levels",
    guild_ids=GUILD_IDS,
)
async def stats(interaction: Interaction):
    locale_model = get_locale_model(interaction.user.roles)
    user_info_response = await api.user_info(user_identifier=str(interaction.user.id))
    if 'error_type' in user_info_response:
        await interaction.send(
            locale_model.NOT_REGISTERED
        )
    else:
        pass


app = FastAPI()


@app.post('/upload')
async def upload_level(
        request_body: UploadRequestBody
) -> UploadResponseBody:
    try:
        embed = Embed(title=request_body.level_name)
        embed.add_field(name='Author', value=request_body.level_author)
        embed.add_field(name='ID', value=request_body.level_id)
        embed.add_field(name='Etiquetas', value=request_body.level_tags)
        message = await (bot.get_channel(LEVEL_POST_CHANNEL_ID)).send(
            files=[
                File(
                    fp=BytesIO(request_body.level_data.encode()),
                    filename=request_body.level_id + '.swe'
                )
            ],
            embeds=[
                embed
            ]
        )
        return UploadResponseBody(
            status='success',
            attachment_id=message.attachments[0].id
        )
    except Exception as e:
        print(e)
        return UploadResponseBody(
            status=str(e)
        )


@app.on_event('startup')
async def startup():
    asyncio.create_task(bot.start(BOT_TOKEN))


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    webhook_server = uvicorn.Server(
        config=uvicorn.Config(
            app,
            host=WEBHOOK_HOST,
            port=WEBHOOK_PORT,
            loop="asyncio",
            workers=1
        )
    )
    loop.run_until_complete(webhook_server.serve())
