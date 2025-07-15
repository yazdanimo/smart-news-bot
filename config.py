# config.py
import os

# بارگذاری متغیرهای محیطی
_raw_url   = os.getenv("WEBHOOK_URL", "")
_raw_token = os.getenv("BOT_TOKEN", "")

# پاک‌سازی انتهای رشته‌ها
WEBHOOK_URL = _raw_url.rstrip(";/")
BOT_TOKEN   = _raw_token.rstrip(";/")
CHANNEL_ID  = int(os.getenv("CHANNEL_ID", "0"))
MODE        = os.getenv("MODE", "webhook")
PORT        = os.getenv("PORT", "8080")
DB_PATH     = os.getenv("DB_PATH", "/tmp/messages.db")
