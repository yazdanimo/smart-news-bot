import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
from handlers import debug_all_messages, handle_channel_post
from config import BOT_TOKEN, CHANNEL_ID, WEBHOOK_URL, PORT

# تنظیمات لاگ
logging.basicConfig(
    format="%(asctime)s %(levelname)s: %(message)s",
    level=logging.INFO
)

def main():
    # ساخت اپلیکیشن تلگرام با توکن از config
    application = ApplicationBuilder().token(BOT_TOKEN).build()

    # هندلر برای لاگ همه‌ی پیام‌های متنی (پیام‌های عادی و discussion)
    application.add_handler(
        MessageHandler(filters.TEXT, debug_all_messages)
    )

    # هندلر برای پست‌های کانال (update.channel_post)
    application.add_handler(
        MessageHandler(filters.CHANNEL_POST & filters.TEXT, handle_channel_post)
    )

    # ست کردن وب‌هوک روی مسیر حاوی توکن
    webhook_path  = f"/{BOT_TOKEN}"
    full_webhook  = f"{WEBHOOK_URL}{webhook_path}"
    logging.info(f"🔗 ست وبهوک روی {full_webhook}")

    # اجرای وب‌هوک (تنها سرور Tornado پایتون-تلگرام-بات)
    application.run_webhook(
        listen="0.0.0.0",
        port=PORT,
        url_path=BOT_TOKEN,
        webhook_url=full_webhook
    )

if __name__ == "__main__":
    logging.info("🚀 بوت در حالت وبهوک شروع می‌شود…")
    main()
