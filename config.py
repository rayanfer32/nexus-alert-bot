import os

NXS_BASE_URL = "http://api.nexus-interactions.io:8080"
ALERT_AMOUNT = 10000 # in NXS
DEBUG_MODE = False # debug mode bot will send messages to developer only
DEVELOPER_CHAT_ID = 628650705
ALERT_CHANNEL_ID= -1001581163183
POLLING_INTERVAL = 20 # in seconds
BOT_NAME = "nexus-alerts-bot"
API_ID=os.environ.get("API_ID")
API_HASH=os.environ.get("API_HASH")
BOT_TOKEN=os.environ.get("BOT_TOKEN")