# config.py
import os

BOT_TOKEN   = os.environ["BOT_TOKEN"]
WEBHOOK_URL = os.environ["WEBHOOK_URL"]
CHANNEL_ID  = os.environ["CHANNEL_ID"]
DB_PATH     = os.environ["DB_PATH"]
MODE        = os.environ.get("MODE", "webhook")
PORT        = int(os.environ.get("PORT", "8443"))
