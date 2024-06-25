import os
from dotenv import load_dotenv, dotenv_values

load_dotenv()

API_ID = int(os.getenv('TG_API_ID'))
API_HASH = os.getenv('TG_API_HASH')
HISTORY_LIMIT = int(os.getenv('HISTORY_LIMIT'))
CHANNEL_USERNAME = os.getenv('TELEGRAM_CHANNEL_USERNAME', 'mrakopedia')
MONGO_URI = os.getenv('MONGO_URI')
DATABASE_NAME = os.getenv('DATABASE_NAME')
COLLECTION_NAME = os.getenv('COLLECTION_NAME')