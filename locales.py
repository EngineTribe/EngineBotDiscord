from pydantic import BaseModel
import os
import yaml
from config import LOCALE_IDS, API_TOKENS
from api import login_session as api_login_session


class LocaleModel(BaseModel):
    alias: str
    REGISTER: str
    REGISTER_DESC: str
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


locales: dict[str, LocaleModel] = {}

for locale_file in os.listdir('locales'):
    with open(f'locales/{locale_file}') as file:
        locales[locale_file.replace('.yml', '')] = LocaleModel.parse_obj(yaml.safe_load(file))


def get_locale_model(roles: list) -> LocaleModel:
    role_ids = map(lambda role: role.id, roles)
    for locale in LOCALE_IDS:
        if LOCALE_IDS[locale] in role_ids:
            return locales[locale]
    return locales['ES']


async def login_session(roles: list) -> str:
    role_ids = map(lambda role: role.id, roles)
    for locale in API_TOKENS:
        if API_TOKENS[locale] in role_ids:
            return await api_login_session(API_TOKENS[locale])
    return await api_login_session(API_TOKENS['ES'])


def discord_localizations(word: str) -> dict[str:str]:
    localizations = {}
    for locale in locales:
        localizations[locales[locale].alias] = locales[locale].__getattribute__(word)
    return localizations
