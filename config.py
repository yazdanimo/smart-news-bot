# config.py
import os

_raw = os.getenv("WEBHOOK_URL", "")
# حذف هر s ) ؛ یا / اضافه در انتهای آدرس
WEBHOOK_URL = _raw.rstrip(";/")
BOT_TOKEN    = os.getenv("BOT_TOKEN")
CHANNEL_ID   = int(os.getenv("CHANNEL_ID", "0"))
MODE         = os.getenv("MODE", "webhook")
PORT         = os.getenv("PORT", "8080")
DB_PATH      = os.getenv("DB_PATH", "/tmp/messages.db")
