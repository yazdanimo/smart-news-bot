import logging
from telegram.ext import ApplicationBuilder, MessageHandler, filters
from handlers import debug_and_handle
from config import BOT_TOKEN, WEBHOOK_URL, PORT

logging.basicConfig(
    format="%(asctime)s %(levelname)s: %(message)s",
    level=logging.INFO
)

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # تنها یک هندلر برای لاگ و پردازش پست‌های کانال
    app.add_handler(
        MessageHandler(filters.TEXT, debug_and_handle)
    )

    webhook_url = f"{WEBHOOK_URL}/{BOT_TOKEN}"
    logging.info(f"🔗 ست وبهوک روی {webhook_url}")

    app.run_webhook(
        listen="0.0.0.0",
        port=PORT,
        url_path=BOT_TOKEN,
        webhook_url=webhook_url
    )

if __name__ == "__main__":
    logging.info("🚀 بوت در حالت وبهوک شروع می‌شود…")
    main()
