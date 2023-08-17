from pydantic import BaseModel
import os
import yaml
from functools import lru_cache
from config import LOCALE_IDS, API_TOKENS
from api import login_session as api_login_session
from datetime import datetime
from context import (
    auth_code,
    auth_code_expires,
    expire,
    user_locales
)


class LocaleModel(BaseModel):
    alias: str
    REGISTER: str
    REGISTER_DESC: str
    REGISTER_TITLE: str
    LEVELS: str
    LEVELS_DESC: str
    LEVELS_ARG1: str
    LEVELS_ARG1_DESC: str
    USERNAME: str
    PASSWORD: str
    CONFIRM_PASSWORD: str
    PASSWORD_MISSMATCH: str
    REGISTER_SUCCESS: str
    ALREADY_REGISTERED: str
    YOUR_USERNAME_IS: str
    USERNAME_ALREADY_TAKEN: str
    UNKNOWN_ERROR: str
    NOT_REGISTERED: str
    UPLOADS: str
    STAGE_MODERATOR: str
    BOOSTER: str
    LOADING: str
    PASSWORD_CHANGE_SUCCESS: str
    CHANGE_PASSWORD: str
    CHANGE_PASSWORD_DESC: str
    SERVER_STATS: str
    SERVER_STATS_DESC: str
    SERVER_STATS_TITLE: str
    SERVER_STATS_OS_VERSION: str
    SERVER_STATS_PYTHON_VERSION: str
    SERVER_STATS_PLAYER_COUNT: str
    SERVER_STATS_LEVEL_COUNT: str
    SERVER_STATS_UPTIME: str
    SERVER_STATS_QPM: str
    MINUTES: str
    PERMISSION: str
    PERMISSION_DESC: str
    PERMISSION_ARG1: str
    PERMISSION_ARG1_DESC: str
    PERMISSION_ARG2: str
    PERMISSION_ARG2_DESC: str
    PERMISSION_ARG3: str
    PERMISSION_ARG3_DESC: str
    PERMISSION_SUCCESS: str
    PERMISSION_FAILED: str
    RANDOM: str
    RANDOM_DESC: str
    RANDOM_ARG1: str
    RANDOM_ARG1_DESC: str
    AUTHOR: str
    QUERY: str
    QUERY_DESC: str
    QUERY_ARG1: str
    QUERY_ARG1_DESC: str
    BAN: str
    BAN_DESC: str
    UNBAN: str
    UNBAN_DESC: str
    BAN_SUCCESS: str
    UNBAN_SUCCESS: str
    ALPHANUMERIC_USERNAME: str
    ALPHANUMERIC_PASSWORD: str


locales: dict[str, LocaleModel] = {}

locales_dir = os.getenv('LOCALES_DIR', 'locales')
for locale_file in os.listdir(locales_dir):
    with open(f'{locales_dir}/{locale_file}') as file:
        locales[locale_file.replace('.yml', '')] = LocaleModel.parse_obj(yaml.safe_load(file))


def get_locale_id(user) -> str:
    user_id = user.id
    if user_id in user_locales:
        return user_locales[user_id]
    else:
        locale = 'ES'
        role_ids = map(lambda role: role.id, user.roles)
        for locale in LOCALE_IDS:
            if LOCALE_IDS[locale] in role_ids:
                break
        user_locales[user_id] = locale
        return locale


def get_locale_model(user) -> LocaleModel:
    return locales[get_locale_id(user)]


async def login_session(user) -> str:
    locale = get_locale_id(user)
    if locale in auth_code:
        if datetime.now() > auth_code_expires[locale] + expire:
            # session expired, renew
            auth_code[locale] = await api_login_session(API_TOKENS[locale])
            auth_code_expires[locale] = datetime.now() + expire
        return auth_code[locale]
    else:
        auth_code_expires[locale] = datetime.now() + expire
        auth_code[locale] = await api_login_session(API_TOKENS[locale])
        return auth_code[locale]


@lru_cache
def discord_localizations(word: str) -> dict[str:str]:
    localizations = {}
    for locale in locales:
        localizations[locales[locale].alias] = locales[locale].__getattribute__(word)
    return localizations
