import os
import logging
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    MessageHandler,
    filters
)
from db import is_duplicate, save_message

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(message)s")
load_dotenv()

TOKEN       = os.environ["BOT_TOKEN"]
CHANNEL_ID  = int(os.environ["CHANNEL_ID"])
WEBHOOK_URL = os.environ["WEBHOOK_URL"].rstrip("/")
PORT        = int(os.environ.get("PORT", 8080))

# هندلرها (کم نکنید)
async def debug_all_messages(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.effective_message
    if msg and msg.text:
        logging.info(f"[DEBUG] chat_id={msg.chat.id}: {msg.text}")

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
    app.add_handler(MessageHandler(filters.TEXT & filters.ChatType.CHANNEL, handle_channel_post))

    # ست‌کردن Webhook
    webhook_path  = f"/{TOKEN}"
    full_webhook  = f"{WEBHOOK_URL}{webhook_path}"
    app.bot.set_webhook(full_webhook)
    logging.info(f"🔗 Webhook set to {full_webhook}")

    # اجرای Webhook server
    app.run_webhook(
        listen="0.0.0.0",
        port=PORT,
        url_path=TOKEN
    )

if __name__ == "__main__":
    logging.info("🚀 Bot starting in webhook mode…")
    main()
