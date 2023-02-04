import nextcord
from nextcord import (
    Interaction,
    File,
    Embed,
    SlashOption
)
from nextcord.ext import commands
from typing import Optional

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
    get_locale_model,
    login_session,
    discord_localizations
)

bot = commands.Bot(intents=nextcord.Intents.all(), command_prefix='/')


@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')


@bot.slash_command(
    name="register",
    name_localizations=discord_localizations('REGISTER'),
    description="📝 Register to start playing SMM:WE.",
    description_localizations=discord_localizations('REGISTER_DESC'),
    guild_ids=GUILD_IDS,
)
async def register(interaction: Interaction):
    locale_model = get_locale_model(interaction.user.roles)
    user_info_response = await api.user_info(user_identifier=str(interaction.user.id))
    if 'error_type' not in user_info_response:
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
    name="change_password",
    name_localizations=discord_localizations('CHANGE_PASSWORD'),
    description="🔐 Change your password.",
    description_localizations=discord_localizations('CHANGE_PASSWORD_DESC'),
    guild_ids=GUILD_IDS,
)
async def change_password(interaction: Interaction):
    locale_model = get_locale_model(interaction.user.roles)
    user_info_response = await api.user_info(user_identifier=str(interaction.user.id))
    if 'error_type' not in user_info_response:
        await interaction.send(
            locale_model.NOT_REGISTERED
        )
    else:
        await interaction.send(
            locale_model.UNKNOWN_ERROR
        )


@bot.slash_command(
    name="levels",
    name_localizations=discord_localizations('LEVELS'),
    description="📊 Get levels by yourself or certain user.",
    description_localizations=discord_localizations('LEVELS_DESC'),
    guild_ids=GUILD_IDS
)
async def levels(
        interaction: Interaction,
        user_identifier: Optional[str] = SlashOption(
            name="user_identifier",
            name_localizations=discord_localizations('LEVELS_ARG1'),
            description="User's username or Discord ID",
            description_localizations=discord_localizations('LEVELS_ARG1_DESC'),
            required=False
        )
):
    locale_model = get_locale_model(interaction.user.roles)
    user_identifier: str = str(interaction.user.id) if user_identifier is None else user_identifier
    response_texts: list[str] = []
    user_info_response = await api.user_info(
        user_identifier=user_identifier
    )
    if 'result' not in user_info_response:
        await interaction.send(
            locale_model.NOT_REGISTERED
        )
    else:
        user_info = user_info_response['result']
        user = bot.get_user(int(user_info['im_id']))
        response_texts.append(
            f"**{user_info['username']}** {user.mention if user is not None else ''}"
            + f'{f"**{locale_model.STAGE_MODERATOR}**" if user_info["is_mod"] else ""}'
            + f'{f"**{locale_model.BOOSTER}**" if user_info["is_booster"] else ""}'
        )
        response_texts.append(
            f"{locale_model.UPLOADS}{user_info['uploads']}"
        )
        response_texts.append(
            locale_model.LOADING
        )

        message = (await interaction.send(
            content='\n'.join(response_texts)
        ))
        response_texts.pop()

        username = user_info['username']
        auth_code = await login_session(interaction.user.roles)
        levels = await api.get_user_levels(
            username=username,
            auth_code=auth_code,
            rows_perpage=user_info['uploads'] + 1
        )
        for level in levels:
            response_texts.append(
                f"> {level['name']} "
                f"{'✨ ' if level['featured'] == 1 else ''}"
                f"`{level['id']}` | "
                f"❤️ {level['likes']} "
                f"💙 {level['dislikes']}"
            )
        await message.edit(
            content='\n'.join(response_texts)
        )


app = FastAPI()


@app.post('/upload')
async def upload_level(
        request_body: UploadRequestBody
) -> UploadResponseBody:
    try:
        author = bot.get_user(request_body.level_author_im_id)
        message = await (bot.get_channel(LEVEL_POST_CHANNEL_ID)).send(
            files=[
                File(
                    fp=BytesIO(request_body.level_data.encode()),
                    filename=request_body.level_id + '.swe'
                )
            ],
            embeds=[
                Embed(
                    title=request_body.level_name,
                    description=f'Author: **{request_body.level_author}** '
                                f'{author.mention if author is not None else ""}\n'
                                f'ID: `{request_body.level_id}`\n'
                                f'Etiquetas: `{request_body.level_tags}`'
                )
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


async def set_rich_presence_timer():
    delay: int = 10
    while True:
        await asyncio.sleep(delay)
        await bot.change_presence(
            
        )

@app.on_event('startup')
async def startup():
    print('Starting Discord bot...')
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
