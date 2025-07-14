import os
import logging
from dotenv import load_dotenv
from flask import Flask
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    MessageHandler,
    filters
)
from db import is_duplicate, save_message

# تنظیم لاگ
logging.basicConfig(format="%(asctime)s %(levelname)s: %(message)s", level=logging.INFO)

# بارگذاری ENV
load_dotenv()
TOKEN       = os.getenv("BOT_TOKEN")
CHANNEL_ID  = int(os.getenv("CHANNEL_ID"))
WEBHOOK_URL = os.getenv("WEBHOOK_URL", "").rstrip("/")
PORT        = int(os.getenv("PORT", 8080))

if not WEBHOOK_URL:
    raise RuntimeError("Missing environment variable WEBHOOK_URL")

# هندلرها
async def debug_all_messages(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_message and update.effective_message.text:
        logging.info(f"[DEBUG] {update.effective_message.chat.id}: {update.effective_message.text}")

async def handle_channel_post(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.effective_message
    if not msg or not msg.text or msg.chat.id != CHANNEL_ID:
        return

    text = msg.text.strip()
    if is_duplicate(text):
        await context.bot.delete_message(chat_id=CHANNEL_ID, message_id=msg.message_id)
        logging.info(f"❌ حذف تکراری: {text}")
    else:
        save_message(text)
        logging.info(f"✅ ثبت جدید: {text}")

def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT, debug_all_messages))
    app.add_handler(
        MessageHandler(filters.TEXT & filters.ChatType.CHANNEL, handle_channel_post)
    )

    webhook_path = f"/{TOKEN}"
    full_webhook = f"{WEBHOOK_URL}{webhook_path}"
    logging.info(f"🔗 Setting webhook to {full_webhook}")

    app.run_webhook(
        listen="0.0.0.0",
        port=PORT,
        url_path=TOKEN,
        webhook_url=full_webhook
    )

if __name__ == "__main__":
    logging.info("🚀 Bot starting in webhook mode…")
    main()
