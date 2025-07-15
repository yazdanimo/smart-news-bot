# bot.py
import logging
from flask import Flask, request
from telegram import Bot, Update
from telegram.ext import Dispatcher, MessageHandler, Filters, Updater

from config import BOT_TOKEN, WEBHOOK_URL, PORT, MODE
from handlers import news_handler
from db import init_db

# Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize database
init_db()

# Create Bot and Dispatcher
bot = Bot(token=BOT_TOKEN)
dp  = Dispatcher(bot, update_queue=None, workers=4, use_context=True)
dp.add_handler(MessageHandler(Filters.text & ~Filters.command, news_handler))

if MODE.lower() == "polling":
    updater = Updater(bot=bot, use_context=True)
    updater.dispatcher = dp
    logger.info("Starting in polling mode")
    updater.start_polling()
    updater.idle()

else:
    app = Flask(__name__)

    WEBHOOK_PATH     = f"/{BOT_TOKEN}"
    WEBHOOK_URL_FULL = f"{WEBHOOK_URL}{WEBHOOK_PATH}"

    @app.route(WEBHOOK_PATH, methods=["POST"])
    def webhook_handler():
        data = request.get_json(force=True)
        update = Update.de_json(data, bot)
        dp.process_update(update)
        return "OK", 200

    bot.set_webhook(WEBHOOK_URL_FULL)
    logger.info(f"Webhook set to: {WEBHOOK_URL_FULL}")

    if __name__ == "__main__":
        app.run(host="0.0.0.0", port=PORT)
