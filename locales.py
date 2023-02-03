from pydantic import BaseModel
import os
import yaml
from config import LOCALE_IDS

locales: dict[str, dict] = {}

for locale_file in os.listdir('locales'):
    with open(f'locales/{locale_file}') as file:
        locales[locale_file.replace('.yml', '')] = yaml.safe_load(file)


def get_locale_model(roles: list):
    role_ids = map(lambda role: role.id, roles)
    for locale in LOCALE_IDS:
        if LOCALE_IDS[locale] in role_ids:
            return LocaleModel.parse_obj(locales[locale])
    return LocaleModel.parse_obj(locales['ES'])


class LocaleModel(BaseModel):
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
