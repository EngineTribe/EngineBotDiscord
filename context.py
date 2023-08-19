from datetime import datetime, timedelta

expire: timedelta = timedelta(minutes=30)
auth_code: dict[str, str] = {}
auth_code_expires: dict[str, datetime] = {}

user_locales: dict[int, str] = {}

LOADING: str = '⏰ Cargando...'