import re
import os
from os import environ
SESSION = environ.get('SESSION', 'Media_search')
API_ID = int(os.environ.get("API_ID", ""))
API_HASH = os.environ.get("API_HASH", "")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "")
APP_NAME = os.getenv("APP_NAME")
TELEGRAM_USERNAME = os.getenv("TELEGRAM_USERNAME")
DB_URL = os.environ.get("DB_URL", "")
DB_NAME = os.environ.get("DB_NAME", "BroadcastBot")
LOG_CHANNEL = os.environ.get("LOG_CHANNEL", "123")
BROADCAST_AS_COPY = bool(os.environ.get("BROADCAST_AS_COPY", True))
