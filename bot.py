import logging
import threading
from flask import Flask
from telegram.ext import ApplicationBuilder, MessageHandler, ChannelPostHandler, filters
from telegram import Update
from config import BOT_TOKEN, CHANNEL_ID, WEBHOOK_URL, PORT
from handlers import debug_all_messages, handle_channel_post

# تنظیمات لاگ
logging.basicConfig(
    format="%(asctime)s %(levelname)s: %(message)s",
    level=logging.INFO
)

# راه‌اندازی Flask برای keep-alive
app_flask = Flask(__name__)
@app_flask.route("/")
def ping():
    return "I'm alive!"

def run_flask():
    app_flask.run(host="0.0.0.0", port=PORT)

def main():
    # ساخت اپلیکیشن تلگرام
    application = ApplicationBuilder().token(BOT_TOKEN).build()

    # ثبت هندلرها
    application.add_handler(MessageHandler(filters.TEXT, debug_all_messages))
    application.add_handler(ChannelPostHandler(handle_channel_post))

    # ست کردن webhook
    path       = f"/{BOT_TOKEN}"
    full_url   = f"{WEBHOOK_URL}{path}"
    logging.info(f"🔗 Setting webhook to {full_url}")

    # شروع وب‌هوک
    application.run_webhook(
        listen="0.0.0.0",
        port=PORT,
        url_path=BOT_TOKEN,
        webhook_url=full_url
    )

if __name__ == "__main__":
    logging.info("🚀 Bot starting in webhook mode…")
    # استارت Flask در یک ترد جدا
    threading.Thread(target=run_flask, daemon=True).start()
    main()
