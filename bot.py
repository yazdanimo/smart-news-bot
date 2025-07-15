import logging
from flask import Flask, request
from telegram import Bot, Update
from telegram.ext import Dispatcher, MessageHandler, Filters, Updater

from config import BOT_TOKEN, WEBHOOK_URL, PORT, MODE
from handlers import news_handler   # <-- ایمپورت مستقیم

# تنظیمات لاگ
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# مقداردهی اولیه دیتابیس
from db import init_db
init_db()

# ساخت شی Bot و Dispatcher
bot = Bot(token=BOT_TOKEN)
dp  = Dispatcher(bot, update_queue=None, workers=4, use_context=True)

# ثبت handler به‌صورت مستقیم
dp.add_handler(MessageHandler(Filters.text & ~Filters.command, news_handler))

if MODE.lower() == "polling":
    # حالت long-polling
    updater = Updater(bot=bot, use_context=True)
    updater.dispatcher = dp

    logger.info("شروع در حالت polling...")
    updater.start_polling()
    updater.idle()

else:
    # حالت webhook با Flask
    app = Flask(__name__)

    @app.route(f"/{BOT_TOKEN}", methods=["POST"])
    def webhook_handler():
        data = request.get_json(force=True)
        update = Update.de_json(data, bot)
        dp.process_update(update)
        return "OK", 200

    # ست کردن وب‌هوک
    bot.set_webhook(WEBHOOK_URL)
    logger.info(f"Webhook set to: {WEBHOOK_URL}")

    if __name__ == "__main__":
        app.run(host="0.0.0.0", port=PORT)
