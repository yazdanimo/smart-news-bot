# bot.py

import logging
from telegram.ext import (
    ApplicationBuilder,
    MessageHandler,
    filters,
)
# سعی می‌کنیم اول از import معمول استفاده کنیم، اگر نبود از مسیر داخلی handlers:
try:
    from telegram.ext import ChannelPostHandler
except ImportError:
    from telegram.ext.handlers import ChannelPostHandler  # fallback

from handlers import debug_all_messages, handle_channel_post
from config import BOT_TOKEN, WEBHOOK_URL, PORT

# تنظیم لاگ
logging.basicConfig(
    format="%(asctime)s %(levelname)s: %(message)s",
    level=logging.INFO
)

def main():
    # ۱) ساخت اپلیکیشن با توکن
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # ۲) ثبت هندلر لاگ تمام پیام‌های متنی (پیام‌های معمولی و discussion)
    app.add_handler(MessageHandler(filters.TEXT, debug_all_messages))

    # ۳) ثبت هندلر پست‌های کانال
    app.add_handler(ChannelPostHandler(handle_channel_post))

    # ۴) ست کردن وبهوک
    path       = f"/{BOT_TOKEN}"
    full_url   = f"{WEBHOOK_URL}{path}"
    logging.info(f"🔗 ست وبهوک روی {full_url}")

    # ۵) اجرای وبهوک (تک سرور Tornado روی پورت مشخص)
    app.run_webhook(
        listen="0.0.0.0",
        port=PORT,
        url_path=BOT_TOKEN,
        webhook_url=full_url
    )

if __name__ == "__main__":
    logging.info("🚀 بوت در حالت وبهوک شروع می‌شود…")
    main()
