# config.py
import os

def clean_env(key: str) -> str:
    """
    بارگذاری و پاک‌سازی مقادیر محیطی:
    حذف فاصله‌ها و کاراکترهای ; یا / اضافی ابتدای/انتهای رشته
    """
    raw = os.getenv(key, "")
    return raw.strip().strip(";/")

BOT_TOKEN   = clean_env("BOT_TOKEN")
WEBHOOK_URL = clean_env("WEBHOOK_URL")
CHANNEL_ID  = int(clean_env("CHANNEL_ID") or 0)
MODE        = clean_env("MODE") or "webhook"
PORT        = clean_env("PORT") or "8080"
DB_PATH     = clean_env("DB_PATH") or "/tmp/messages.db"
