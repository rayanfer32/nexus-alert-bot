import os

# * DEV
# DEBUG_MODE = True # debug mode bot will send messages to developer only
# ALERT_AMOUNT = 1 # in NXS
# POLLING_INTERVAL = 10 # in seconds

# # * PROD
DEBUG_MODE = False # debug mode bot will send messages to developer only
ALERT_AMOUNT = 1000 # in NXS
POLLING_INTERVAL = 20 # in seconds

NXS_BASE_URL = "http://api.nexus-interactions.io:8080"
DEVELOPER_CHAT_ID = 628650705
ALERT_CHANNEL_ID= -1001581163183 # t.me/nexusalerts
BOT_NAME = "nexus-alerts-bot"
API_ID=os.environ.get("API_ID")
API_HASH=os.environ.get("API_HASH")
BOT_TOKEN=os.environ.get("BOT_TOKEN")