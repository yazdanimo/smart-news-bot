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

# تنظیمات لاگ
logging.basicConfig(
    format="%(asctime)s %(levelname)s: %(message)s",
    level=logging.INFO
)

def main():
    # ساخت اپلیکیشن با توکن
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # 1) لاگ همه‌ی پیام‌های متنی (شامل پیام‌های کاربر و discussion)
    app.add_handler(
        MessageHandler(filters.TEXT, debug_all_messages)
    )

    # 2) هندلر پست‌های کانال
    #    این فیلتر مختص update.channel_post است و فقط متن را می‌گیرد.
    app.add_handler(
        MessageHandler(
            filters.UpdateType.CHANNEL_POST & filters.TEXT,
            handle_channel_post
        )
    )

    # ست کردن وبهوک روی مسیری که شامل توکن است
    webhook_path = f"/{BOT_TOKEN}"
    full_webhook = f"{WEBHOOK_URL}{webhook_path}"
    logging.info(f"🔗 ست وبهوک روی {full_webhook}")

    # اجرا در حالت وبهوک (تنها یک سرور Tornado روی پورت مشخص)
    app.run_webhook(
        listen="0.0.0.0",
        port=PORT,
        url_path=BOT_TOKEN,
        webhook_url=full_webhook
    )

if __name__ == "__main__":
    logging.info("🚀 بوت در حالت وبهوک شروع می‌شود…")
    main()
