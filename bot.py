import os
import sys
import threading
from dotenv import load_dotenv
from flask import Flask
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters
from db import is_duplicate, save_message
import logging

# این خط را قبلاً اضافه کردید
print("=== BOOTSTRAP STARTED ===", flush=True)

# این دو خط را بلافاصله بعدش اضافه کنید
print("🚀 Flask server starting…", flush=True)
load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = int(os.getenv("CHANNEL_ID"))
PORT = int(os.getenv("PORT", 8080))

# راه‌اندازی Flask
app_flask = Flask(__name__)
@app_flask.route("/")
def ping():
    return "I'm alive!"

def run_flask():
    app_flask.run(host="0.0.0.0", port=PORT)

if __name__ == "__main__":
    # استارت Flask در ترد جداگانه
    threading.Thread(target=run_flask, daemon=True).start()
    
    # حتماً این print را ببینید
    print("🚀 Flask server started", flush=True)

    # ساخت اپلیکیشن تلگرام
    app = ApplicationBuilder().token(TOKEN).build()

    # ثبت هندلرها
    app.add_handler(MessageHandler(filters.TEXT, debug_all_messages))
    app.add_handler(MessageHandler(filters.TEXT & filters.ChatType.CHANNEL, handle_channel_post))

    # و این هم حتما باید لاگ شود
    print("🚀 Bot is running...", flush=True)

    # شروع پُلیینگ
    app.run_polling()
