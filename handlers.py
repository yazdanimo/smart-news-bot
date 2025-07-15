import os
from telegram import Update, Bot
from telegram.ext import Dispatcher, MessageHandler, Filters
from flask import Flask, request

TOKEN   = os.environ["TELEGRAM_TOKEN"]
WEBHOOK = f"/{TOKEN}"
PORT    = int(os.environ.get("PORT", 8443))

app = Flask(__name__)
bot = Bot(token=TOKEN)
dp  = Dispatcher(bot, update_queue=None, workers=0, use_context=True)

# یک handler ساده برای تست
def echo(update: Update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="🔔 دریافت شد!")

dp.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

# این route باید دقیقاً برابر webhook URL باشد
@app.route(WEBHOOK, methods=["POST"])
def webhook_handler():
    data = request.get_json(force=True)
    update = Update.de_json(data, bot)
    dp.process_update(update)
    return "OK", 200

if __name__ == "__main__":
    # ثبت وب‌هوک
    bot.set_webhook(f"https://YOUR_APP_DOMAIN/{TOKEN}")
    # راه‌اندازی سرور
    app.run(host="0.0.0.0", port=PORT)
