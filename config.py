import yaml

_config = yaml.safe_load(open('config.yml'))

BOT_TOKEN = _config['bot']['token']
GUILD_IDS = _config['bot']['guild_ids']
LOCALE_IDS = _config['bot']['locale_ids']
LEVEL_POST_CHANNEL_ID = _config['bot']['level_post_channel_id']

API_HOST = _config['enginetribe_api']['host']
API_KEY = _config['enginetribe_api']['api_key']

WEBHOOK_HOST = _config['webhook']['host']
WEBHOOK_PORT = _config['webhook']['port']