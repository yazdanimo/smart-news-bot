import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN   = os.getenv("BOT_TOKEN")
CHANNEL_ID  = int(os.getenv("CHANNEL_ID", 0))
WEBHOOK_URL = os.getenv("WEBHOOK_URL", "").rstrip("/")
PORT        = int(os.getenv("PORT", 8080))

if not all([BOT_TOKEN, CHANNEL_ID, WEBHOOK_URL]):
    raise RuntimeError("Environment variables BOT_TOKEN, CHANNEL_ID or WEBHOOK_URL missing")
