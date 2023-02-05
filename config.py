import yaml
import os

config_path = os.getenv('CONFIG_PATH', 'config.yml')
_config = yaml.safe_load(open(config_path, 'r'))

WEBSITE_URL = "https://web.enginetribe.gq/"

BOT_TOKEN = _config['bot']['token']
GUILD_IDS = _config['bot']['guild_ids']
LOCALE_IDS = _config['bot']['locale_ids']
LEVEL_POST_CHANNEL_ID = _config['bot']['level_post_channel_id']
BOOSTER_ROLE_ID = _config['bot']['booster_role_id']
STAGE_MODERATOR_ROLE_ID = _config['bot']['stage_moderator_role_id']
MEMBER_ROLE_ID = _config['bot']['member_role_id']

API_HOST = _config['enginetribe_api']['host']
API_KEY = _config['enginetribe_api']['api_key']
API_TOKENS = _config['enginetribe_api']['tokens']

WEBHOOK_HOST = _config['webhook']['host']
WEBHOOK_PORT = _config['webhook']['port']
