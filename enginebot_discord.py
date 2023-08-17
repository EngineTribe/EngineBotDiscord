import nextcord
from nextcord import (
    Interaction,
    File,
    Embed,
    SlashOption,
    Activity,
    ActivityType,
    Status,
    Member,
    Role
)
from nextcord.ext import commands
from typing import Optional

import asyncio

from fastapi import FastAPI
import uvicorn
from models import (
    UploadRequestBody,
    UploadResponseBody
)
from io import BytesIO

from config import *
import api
from activities import (
    Register,
    ChangePassword
)
from locales import (
    get_locale_model,
    login_session,
    discord_localizations
)

bot = commands.Bot(
    intents=nextcord.Intents.all(),
    command_prefix='/',
    default_guild_ids=GUILD_IDS
)

LOADING: str = '⏰ Cargando...'

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')


@bot.slash_command(
    name="register",
    name_localizations=discord_localizations('REGISTER'),
    description="📝 Register to start playing SMM:WE.",
    description_localizations=discord_localizations('REGISTER_DESC'),
)
async def register(interaction: Interaction):
    locale_model = get_locale_model(interaction.user)
    await interaction.response.send_modal(
        Register(
            locale_model=locale_model
        )
    )


@bot.slash_command(
    name="change_password",
    name_localizations=discord_localizations('CHANGE_PASSWORD'),
    description="🔐 Change your password.",
    description_localizations=discord_localizations('CHANGE_PASSWORD_DESC'),
)
async def change_password(interaction: Interaction):
    locale_model = get_locale_model(interaction.user)
    await interaction.response.send_modal(
        ChangePassword(
            locale_model=locale_model
        )
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
    message = await interaction.send(LOADING)
    locale_model = get_locale_model(interaction.user)
    user_identifier: str = str(interaction.user.id) if user_identifier is None else user_identifier
    response_texts: list[str] = []
    user_info_response = await api.user_info(
        user_identifier=user_identifier
    )
    if 'result' not in user_info_response:
        await message.edit(
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

        await message.edit(
            content='\n'.join(response_texts)
        )
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


@bot.slash_command(
    name="server_stats",
    name_localizations=discord_localizations('SERVER_STATS'),
    description="📊 Get server stats.",
    description_localizations=discord_localizations('SERVER_STATS_DESC'),
)
async def server_stats(interaction: Interaction):
    message = await interaction.send(LOADING)
    locale_model = get_locale_model(interaction.user)
    stats = await api.server_stats()
    await message.edit(
        f'{locale_model.SERVER_STATS_TITLE}\n'
        f'> {locale_model.SERVER_STATS_OS_VERSION} {stats.os}\n'
        f'> {locale_model.SERVER_STATS_PYTHON_VERSION} {stats.python}\n'
        f'> {locale_model.SERVER_STATS_PLAYER_COUNT} {stats.player_count}\n'
        f'> {locale_model.SERVER_STATS_LEVEL_COUNT} {stats.level_count}\n'
        f'> {locale_model.SERVER_STATS_UPTIME} {int(stats.uptime / 60)} {locale_model.MINUTES}\n'
        f'> {locale_model.SERVER_STATS_QPM} {stats.connection_per_minute}\n'
    )


@bot.slash_command(
    name="permission",
    name_localizations=discord_localizations('PERMISSION'),
    description="🔒 Change user's permission.",
    description_localizations=discord_localizations('PERMISSION_DESC'),
)
async def update_permission(
        interaction: Interaction,
        user_identifier: str = SlashOption(
            name="user_identifier",
            name_localizations=discord_localizations('PERMISSION_ARG1'),
            description="👤 User's username or Discord ID",
            description_localizations=discord_localizations('PERMISSION_ARG1_DESC'),
            required=True
        ),
        permission: str = SlashOption(
            name="permission",
            name_localizations=discord_localizations('PERMISSION_ARG2'),
            description="🔒 Permission to change",
            description_localizations=discord_localizations('PERMISSION_ARG2_DESC'),
            required=True,
            choices={
                'Stage Mod': 'mod',
                'Booster': 'booster',
                'Member': 'valid',
                'Banned': 'banned',
                'Administrator': 'admin'
            }
        ),
        value: bool = SlashOption(
            name="value",
            name_localizations=discord_localizations('PERMISSION_ARG3'),
            description="🔒 Permission value",
            description_localizations=discord_localizations('PERMISSION_ARG3_DESC'),
            required=True,
            choices={
                'True': True,
                'False': False
            }
        )
):
    message = await interaction.send(LOADING)
    locale_model = get_locale_model(interaction.user)
    response_json = await api.update_permission(
        user_identifier=user_identifier,
        permission=permission,
        value=value
    )
    if 'error_type' in response_json:
        await message.edit(
            locale_model.PERMISSION_FAILED + '\n' + f"{response_json['error_type']} - {response_json['message']}"
        )
    else:
        await message.edit(
            locale_model.PERMISSION_SUCCESS
        )


def level_details_to_string(level: dict, locale_model) -> str:
    clears: int = level['victorias']
    attempts: int = level['intentos']
    clear_rate: str = str(round(clears / attempts * 100, 2)) + '%'
    return (
        f"**{level['name']}**{' ✨' if level['featured'] == 1 else ''}\n"
        f"> 👤 {locale_model.AUTHOR} **{level['author']}**\n"
        f"> ID: `{level['id']}`\n"
        f"> 🏷️ {level['etiquetas']}\n"
        f"> ❤️ {level['likes']} | 💙 {level['dislikes']}\n"
        f"> ⛳ {clears} / 🎮 {attempts} ({clear_rate})\n"
    )


@bot.slash_command(
    name="random",
    name_localizations=discord_localizations('RANDOM'),
    description="🎲 Get random level.",
    description_localizations=discord_localizations('RANDOM_DESC'),
)
async def random_level(
        interaction: Interaction,
        difficulty: Optional[str] = SlashOption(
            name="difficulty",
            name_localizations=discord_localizations('RANDOM_ARG1'),
            description="🎲 Level difficulty",
            description_localizations=discord_localizations('RANDOM_ARG1_DESC'),
            required=False,
            choices={
                'Easy': '0',
                'Normal': '1',
                'Expert': '2',
                'Super Expert': '3'
            }
        )
):
    message = await interaction.send(LOADING)
    locale_model = get_locale_model(interaction.user)
    auth_code = await login_session(interaction.user.roles)
    level = (await api.random_level(auth_code=auth_code, difficulty=difficulty))['result']
    await message.edit(
        level_details_to_string(level, locale_model)
    )


@bot.slash_command(
    name="query",
    name_localizations=discord_localizations('QUERY'),
    description="🔍 Query level.",
    description_localizations=discord_localizations('QUERY_DESC'),
)
async def query_level(
        interaction: Interaction,
        level_id: str = SlashOption(
            name="level_id",
            name_localizations=discord_localizations('QUERY_ARG1'),
            description="🔍 Level ID",
            description_localizations=discord_localizations('QUERY_ARG1_DESC'),
            required=True
        )
):
    message = await interaction.send(LOADING)
    locale_model = get_locale_model(interaction.user)
    auth_code = await login_session(interaction.user.roles)
    level = await api.query_level(auth_code=auth_code, level_id=level_id)
    if 'error_type' in level:
        await message.edit(
            f"❌ {level['error_type']} - {level['message']}"
        )
    else:
        await message.edit(
            level_details_to_string(level, locale_model)
        )


@bot.slash_command(
    name="ban",
    name_localizations=discord_localizations('BAN'),
    description="🔨 Ban user.",
    description_localizations=discord_localizations('BAN_DESC'),
)
async def ban_user(
        interaction: Interaction,
        user_identifier: str = SlashOption(
            name="user_identifier",
            name_localizations=discord_localizations('PERMISSION_ARG1'),
            description="🔨 User identifier",
            description_localizations=discord_localizations('PERMISSION_ARG1_DESC'),
            required=True
        )
):
    locale_model = get_locale_model(interaction.user)
    message = await interaction.send(
        locale_model.LOADING
    )
    response_json = await api.update_permission(
        user_identifier=user_identifier,
        permission='banned',
        value=True
    )
    if 'error_type' in response_json:
        await message.edit(
            locale_model.PERMISSION_FAILED + '\n' + f"{response_json['error_type']} - {response_json['message']}"
        )
    else:
        await message.edit(
            locale_model.BAN_SUCCESS
        )


@bot.slash_command(
    name="unban",
    name_localizations=discord_localizations('UNBAN'),
    description="🔓 Unban user.",
    description_localizations=discord_localizations('UNBAN_DESC'),
)
async def unban_user(
        interaction: Interaction,
        user_identifier: str = SlashOption(
            name="user_identifier",
            name_localizations=discord_localizations('PERMISSION_ARG1'),
            description="🔓 User identifier",
            description_localizations=discord_localizations('PERMISSION_ARG1_DESC'),
            required=True
        )
):
    locale_model = get_locale_model(interaction.user)
    message = await interaction.send(
        locale_model.LOADING
    )
    response_json = await api.update_permission(
        user_identifier=user_identifier,
        permission='banned',
        value=False
    )
    if 'error_type' in response_json:
        await message.edit(
            locale_model.PERMISSION_FAILED + '\n' + f"{response_json['error_type']} - {response_json['message']}"
        )
    else:
        await message.edit(
            locale_model.UNBAN_SUCCESS
        )


@bot.event
async def on_member_update(before: Member, after: Member):
    def check_role(roles: list[Role], role_id: int):
        for role in roles:
            if role.id == role_id:
                return True
        return False

    has_stage_mod_role = check_role(after.roles, STAGE_MODERATOR_ROLE_ID)
    has_booster_role = check_role(after.roles, BOOSTER_ROLE_ID)
    has_member_role = check_role(after.roles, MEMBER_ROLE_ID)
    user_identifier = str(after.id)
    for permission, value in [('mod', has_stage_mod_role), ('booster', has_booster_role), ('valid', has_member_role)]:
        await api.update_permission(
            user_identifier=user_identifier,
            permission=permission,
            value=value
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
                                f'Etiquetas: `{request_body.level_tags}`\n'
                                f'Descripción: `{request_body.description}`'
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
    async def change_presence(
            activity_type: ActivityType,
            name: str,
            status: Status = Status.online
    ):
        await bot.change_presence(
            activity=Activity(
                type=activity_type,
                name=name,
                url=WEBSITE_URL
            ),
            status=status
        )
        await asyncio.sleep(delay)

    delay: int = 30
    await bot.wait_until_ready()
    while True:
        for activity in RICH_PRESENCE_ACTIVITIES:
            await change_presence(
                activity_type=ActivityType[activity['type']],
                name=activity['name'],
                status=activity['status']
            )
        await change_presence(ActivityType.watching, f"{bot.get_guild(GUILD_IDS[0]).member_count} members")


@app.on_event('startup')
async def startup():
    print('Starting Discord bot...')
    asyncio.create_task(bot.start(BOT_TOKEN))
    if RICH_PRESENCE_ENABLED:
        asyncio.create_task(set_rich_presence_timer())


@app.on_event('shutdown')
async def shutdown():
    await bot.wait_until_ready()
    await bot.change_presence(activity=None, status=Status.offline)
    await bot.close()


def run():
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


if __name__ == '__main__':
    run()
