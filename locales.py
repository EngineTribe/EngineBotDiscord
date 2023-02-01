from dataclasses import dataclass
from config import (
    EN_LOCALE_ID,
    ZH_LOCALE_ID,
    PT_LOCALE_ID
)


def get_locale_model(roles: list):
    role_ids = map(lambda role: role.id, roles)
    if EN_LOCALE_ID in role_ids:
        return EN
    elif ZH_LOCALE_ID in role_ids:
        return ZH
    elif PT_LOCALE_ID in role_ids:
        return PT
    else:
        return ES


@dataclass
class ZH:
    USERNAME: str = '👤 用户名'
    PASSWORD: str = '🔐 密码'
    CONFIRM_PASSWORD: str = '🔐 确认密码'
    PASSWORD_MISSMATCH: str = '❌ 密码不匹配。'
    REGISTER_SUCCESS: str = '注册成功，现在你可以开始享受游戏了。'
    ALREADY_REGISTERED: str = '❌ 你已经注册过账号了。'
    YOUR_USERNAME_IS: str = '你的用户名是：'
    USERNAME_ALREADY_TAKEN: str = '❌ 用户名已被占用。'
    UNKNOWN_ERROR: str = '❌ 未知错误。'
    NOT_REGISTERED: str = '❌ 你还没有注册账号。'


@dataclass
class ES:
    USERNAME: str = '👤 Nombre de usuario'
    PASSWORD: str = '🔐 Contraseña'
    CONFIRM_PASSWORD: str = '🔐 Confirmar contraseña'
    PASSWORD_MISSMATCH: str = '❌ Las contraseñas no coinciden.'
    REGISTER_SUCCESS: str = 'Registro exitoso, ahora puedes empezar a jugar.'
    ALREADY_REGISTERED: str = '❌ Ya te has registrado.'
    YOUR_USERNAME_IS: str = 'Tu nombre de usuario es:'
    USERNAME_ALREADY_TAKEN: str = '❌ El nombre de usuario ya está en uso.'
    UNKNOWN_ERROR: str = '❌ Error desconocido.'
    NOT_REGISTERED: str = '❌ Aún no te has registrado.'


@dataclass
class EN:
    USERNAME: str = '👤 Username'
    PASSWORD: str = '🔐 Password'
    CONFIRM_PASSWORD: str = '🔐 Confirm password'
    PASSWORD_MISSMATCH: str = '❌ Passwords mismatch.'
    REGISTER_SUCCESS: str = 'Successfully registered, now you can start playing.'
    ALREADY_REGISTERED: str = '❌ You are already registered.'
    YOUR_USERNAME_IS: str = 'Your username is:'
    USERNAME_ALREADY_TAKEN: str = '❌ Username is already taken.'
    UNKNOWN_ERROR: str = '❌ Unknown error.'
    NOT_REGISTERED: str = '❌ You are not registered yet.'


@dataclass
class PT:
    USERNAME: str = '👤 Nome de usuário'
    PASSWORD: str = '🔐 Senha'
    CONFIRM_PASSWORD: str = '🔐 Confirmar senha'
    PASSWORD_MISSMATCH: str = '❌ As senhas não correspondem.'
    REGISTER_SUCCESS: str = 'Registro bem-sucedido, agora você pode começar a jogar.'
    ALREADY_REGISTERED: str = '❌ Você já está registrado.'
    YOUR_USERNAME_IS: str = 'Seu nome de usuário é:'
    USERNAME_ALREADY_TAKEN: str = '❌ O nome de usuário já está em uso.'
    UNKNOWN_ERROR: str = '❌ Erro desconhecido.'
    NOT_REGISTERED: str = '❌ Você ainda não está registrado.'
