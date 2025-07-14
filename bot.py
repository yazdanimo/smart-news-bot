# bot.py

import logging
from telegram.ext import (
    ApplicationBuilder,
    MessageHandler,
    filters
)
from handlers import debug_all_messages, handle_channel_post
from config import BOT_TOKEN, WEBHOOK_URL, PORT

# تنظیم لاگ
logging.basicConfig(
    format="%(asctime)s %(levelname)s: %(message)s",
    level=logging.INFO
)

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # لاگ همهٔ پیام‌های متنی
    app.add_handler(MessageHandler(filters.TEXT, debug_all_messages))

    # فقط پست‌های کانال (update.channel_post) را به handle_channel_post بده
    app.add_handler(
        MessageHandler(filters.UpdateType.CHANNEL_POST, handle_channel_post)
    )

    # ست کردن وبهوک
    webhook_path = f"/{BOT_TOKEN}"
    full_webhook = f"{WEBHOOK_URL}{webhook_path}"
    logging.info(f"🔗 ست وبهوک روی {full_webhook}")

    # اجرا در حالت وبهوک
    app.run_webhook(
        listen="0.0.0.0",
        port=PORT,
        url_path=BOT_TOKEN,
        webhook_url=full_webhook
    )

if __name__ == "__main__":
    logging.info("🚀 بوت در حالت وبهوک شروع می‌شود…")
    main()
