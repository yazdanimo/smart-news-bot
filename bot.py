# bot.py

import logging
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    MessageHandler,
    filters,
    ContextTypes
)
from handlers import debug_all_messages, handle_channel_post
from config import BOT_TOKEN, WEBHOOK_URL, PORT

# تنظیمات پایه‌ی لاگ
logging.basicConfig(
    format="%(asctime)s %(levelname)s: %(message)s",
    level=logging.INFO
)

def main():
    # ساخت اپلیکیشن با توکن
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # ۱) لاگ همه‌ی پیام‌های متنی (شامل پیام‌های کاربر در گروه/دایرکت)
    app.add_handler(
        MessageHandler(filters.TEXT, debug_all_messages)
    )

    # ۲) هندل کردن پست‌های کانال (update.channel_post)
    app.add_handler(
        MessageHandler(
            filters.UpdateType.CHANNEL_POST & filters.TEXT,
            handle_channel_post
        )
    )

    # ست کردن وبهوک روی مسیر حاوی توکن
    webhook_url = f"{WEBHOOK_URL}/{BOT_TOKEN}"
    logging.info(f"🔗 ست وبهوک روی {webhook_url}")

    # اجرای وبهوک (تک سرور Tornado روی پورت مشخص)
    app.run_webhook(
        listen="0.0.0.0",
        port=PORT,
        url_path=BOT_TOKEN,
        webhook_url=webhook_url
    )

if __name__ == "__main__":
    logging.info("🚀 بوت در حالت وبهوک شروع می‌شود…")
    main()
