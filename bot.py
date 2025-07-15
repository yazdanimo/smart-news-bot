import logging
from flask import Flask, request
from telegram import Bot, Update
from telegram.ext import Dispatcher, Updater, MessageHandler, Filters
from config import BOT_TOKEN, WEBHOOK_URL, PORT, MODE

# لاگ روی INFO
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# دیتابیس را آماده می‌کند
from db import init_db
init_db()

# در هر دو حالت، Dispatcher و handler را تعریف می‌کنیم
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot, update_queue=None, workers=4, use_context=True)
dp.add_handler(MessageHandler(Filters.text & ~Filters.command, __import__('handlers').handlers.news_handler))

if MODE.lower() == "polling":
    # حالت Long Polling
    updater = Updater(bot=bot, use_context=True)
    updater.dispatcher = dp

    logger.info("Starting in polling mode...")
    updater.start_polling()
    updater.idle()

else:
    # حالت Webhook با Flask
    app = Flask(__name__)

    @app.route(f"/{BOT_TOKEN}", methods=["POST"])
    def webhook_handler():
        data = request.get_json(force=True)
        update = Update.de_json(data, bot)
        dp.process_update(update)
        return "OK", 200

    # ست کردن وب‌هوک در تلگرام
    bot.set_webhook(WEBHOOK_URL)
    logger.info(f"Webhook set to: {WEBHOOK_URL}")

    if __name__ == "__main__":
        app.run(host="0.0.0.0", port=PORT)
