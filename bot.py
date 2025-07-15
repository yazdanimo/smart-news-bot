import logging
import os
from flask import Flask, request
from telegram import Bot, Update
from telegram.ext import Dispatcher, MessageHandler, Filters
from config import TOKEN, BASE_URL, PORT
from handlers import news_handler
from db import init_db

# تنظیمات لاگ
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# مقداردهی اولیه دیتابیس
init_db()

# ساخت اپ Flask و بات تلگرام
app = Flask(__name__)
bot = Bot(token=TOKEN)
dp = Dispatcher(bot, update_queue=None, workers=4, use_context=True)

# ثبت handler برای همه‌ی پیام‌های متنی (غیر از کامندها)
dp.add_handler(MessageHandler(Filters.text & ~Filters.command, news_handler))

# مسیر وب‌هوک باید دقیقاً /<TOKEN> باشد
WEBHOOK_PATH = f"/{TOKEN}"

@app.route(WEBHOOK_PATH, methods=["POST"])
def webhook_handler():
    """
    این endpoint داده‌ی آپدیت تلگرام را دریافت و پردازش می‌کند.
    """
    data = request.get_json(force=True)
    update = Update.de_json(data, bot)
    dp.process_update(update)
    return "OK", 200

if __name__ == "__main__":
    # ثبت وب‌هوک در تلگرام
    webhook_url = f"{BASE_URL}/{TOKEN}"
    bot.set_webhook(webhook_url)
    logger.info(f"Webhook set to: {webhook_url}")

    # راه‌اندازی سرور Flask
    app.run(host="0.0.0.0", port=PORT)
