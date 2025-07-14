import os
import sys
import threading
from dotenv import load_dotenv
from flask import Flask
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters
# <YOUR_IMPORTS> مثل:
# from db import is_duplicate, save_message

# ۱) تعریف توابع هندلر قبل از استفاده

# همه‌ی پیام‌های متنی (برای دیباگ)
async def debug_all_messages(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.effective_message
    if msg and msg.text:
        print(f"[DEBUG] chat_id={msg.chat.id} ({msg.chat.type}): {msg.text}", flush=True)

# حذف تکراری‌ها در کانال
async def handle_channel_post(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.effective_message
    if not msg or not msg.text:
        return

    if msg.chat.id != CHANNEL_ID:
        return

    text = msg.text.strip()
    if is_duplicate(text):
        await context.bot.delete_message(chat_id=CHANNEL_ID, message_id=msg.message_id)
        print(f"❌ حذف تکراری: {text}", flush=True)
    else:
        save_message(text)
        print(f"✅ ثبت جدید: {text}", flush=True)

# ۲) بوت‌استرپ و لاگ‌های اولیه
print("=== BOOTSTRAP STARTED ===", flush=True)
print("🚀 Flask server starting…", flush=True)

# بارگذاری متغیرهای محیطی
load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = int(os.getenv("CHANNEL_ID"))
PORT = int(os.getenv("PORT", 8080))

# راه‌اندازی Flask برای پینگ
app_flask = Flask(__name__)
@app_flask.route("/")
def ping():
    return "I'm alive!"

def run_flask():
    app_flask.run(host="0.0.0.0", port=PORT)

if __name__ == "__main__":
    # استارت Flask
    threading.Thread(target=run_flask, daemon=True).start()
    print("🚀 Flask server started", flush=True)

    # ساخت اپ تلگرام
    app = ApplicationBuilder().token(TOKEN).build()

    # ثبت هندلرها
    app.add_handler(MessageHandler(filters.TEXT, debug_all_messages))
    app.add_handler(
        MessageHandler(filters.TEXT & filters.ChatType.CHANNEL, handle_channel_post)
    )

    print("🚀 Bot is running...", flush=True)
    app.run_polling()
