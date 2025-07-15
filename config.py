# config.py
import os
from dotenv import load_dotenv

# بارگذاری متغیرهای محیطی از .env
load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN", "")
CHANNEL_ID = int(os.getenv("CHANNEL_ID", "0"))
MODE = os.getenv("MODE", "polling")  # polling یا webhook
WEBHOOK_URL = os.getenv("WEBHOOK_URL", "")
PORT = os.getenv("PORT", "8080")
DB_PATH = os.getenv("DB_PATH", "messages.db")
