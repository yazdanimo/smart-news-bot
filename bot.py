import os
import threading
from dotenv import load_dotenv
from flask import Flask
from telegram import Update, Bot
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    MessageHandler,
    ChannelPostHandler,
    filters
)
from db import is_duplicate, save_message

# بارگذاری متغیرهای محیطی
load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = int(os.getenv("CHANNEL_ID"))
PORT = int(os.getenv("PORT", 8080))

# راه‌اندازی Flask برای پینگ مداوم (Railway)
app_flask = Flask(__name__)
@app_flask.route("/")
def ping():
    return "I'm alive!"

def run_flask():
    app_flask.run(host="0.0.0.0", port=PORT)

# لاگینگ
import logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s"
)

# هندلر دیباگ برای همه پیام‌های متنی (گروه/دایرکت)
async def debug_all_messages(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.effective_message
    if msg and msg.text:
        logging.info(f"[DEBUG-MSG] chat_id={msg.chat.id} ({msg.chat.type}): {msg.text}")

# هندلر دیباگ برای پست‌های کانال
async def debug_channel_posts(update: Update, context: ContextTypes.DEFAULT_TYPE):
    post = update.channel_post
    if post and post.text:
        logging.info(f"[DEBUG-CHAN] chat_id={post.chat.id}: {post.text}")

# هندلر حذف پیام‌های تکراری در کانال
async def handle_channel_post(update: Update, context: ContextTypes.DEFAULT_TYPE):
    post = update.channel_post
    if not post or not post.text:
        return

    # فقط کانال مورد نظر
    if post.chat.id != CHANNEL_ID:
        return

    text = post.text.strip()
    if is_duplicate(text):
        await context.bot.delete_message(
            chat_id=CHANNEL_ID,
            message_id=post.message_id
        )
        logging.info(f"❌ حذف تکراری: {text}")
    else:
        save_message(text)
        logging.info(f"✅ ثبت جدید: {text}")

if __name__ == "__main__":
    # استارت Flask
    threading.Thread(target=run_flask, daemon=True).start()
    logging.info("🚀 Flask server started")

    # ساخت اپلیکیشن تلگرام
    app = ApplicationBuilder().token(TOKEN).build()

    # ثبت هندلرها
    app.add_handler(MessageHandler(filters.TEXT, debug_all_messages))
    app.add_handler(ChannelPostHandler(filters.TEXT, debug_channel_posts))
    app.add_handler(ChannelPostHandler(filters.TEXT, handle_channel_post))

    # اجرای ربات
    logging.info("🚀 Bot is running...")
    app.run_polling()
