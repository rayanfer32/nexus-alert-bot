import os
import dotenv
dotenv.load_dotenv()

# * DEV
DEBUG_MODE = True  # debug mode bot will send messages to developer only
ALERT_AMOUNT = 1  # in NXS
POLLING_INTERVAL = 20  # in seconds

# * PROD
if os.environ.get("ENV") == "PROD":
    print("Production mode")
    DEBUG_MODE = False
    ALERT_AMOUNT = 1000
    POLLING_INTERVAL = 20
else:
    print("Development mode")


BOT_NAME = "nexus-alerts-bot"
HIDE_DEBIT_TXNS = True  # hide debit transactions

# * load configurations from env
DEVELOPER_CHAT_ID = int(os.environ.get('DEVELOPER_CHAT_ID'))
DEVELOPER_CHAT_IDS = list(
    map(int, os.environ.get('DEVELOPER_CHAT_IDS').split(',')))
ALERT_CHANNEL_ID = int(os.environ.get('ALERT_CHANNEL_ID'))  # t.me/nexusalerts
EXPLORER_DOMAIN = os.environ.get('EXPLORER_DOMAIN')
NXS_BASE_URL = os.environ.get('NXS_BASE_URL')
API_ID = os.environ.get("API_ID")
API_HASH = os.environ.get("API_HASH")
BOT_TOKEN = os.environ.get("BOT_TOKEN")
