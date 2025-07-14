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

# تنظیم لاگ
logging.basicConfig(
  format="%(asctime)s %(levelname)s: %(message)s",
  level=logging.INFO
)

# بارگذاری ENV
load_dotenv()
TOKEN       = os.getenv("BOT_TOKEN")
CHANNEL_ID  = int(os.getenv("CHANNEL_ID", 0))
WEBHOOK_URL = os.getenv("WEBHOOK_URL", "").rstrip("/")
PORT        = int(os.getenv("PORT", 8080))

if not all([TOKEN, CHANNEL_ID, WEBHOOK_URL]):
    raise RuntimeError("Missing BOT_TOKEN, CHANNEL_ID or WEBHOOK_URL")

# لاگ همه‌ی پیام‌های متنی
async def debug_all_messages(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.effective_message
    if msg and msg.text:
        logging.info(f"[DEBUG] {msg.chat.id} ({msg.chat.type}): {msg.text}")

# حذف یا ثبت پیام‌های کانال
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

    # ثبت هندلرها
    app.add_handler(MessageHandler(filters.TEXT, debug_all_messages))
    app.add_handler(
      MessageHandler(filters.TEXT & filters.ChatType.CHANNEL, handle_channel_post)
    )

    # ستِ وبهوک
    path     = f"/{TOKEN}"
    full_url = f"{WEBHOOK_URL}{path}"
    logging.info(f"🔗 Setting webhook to {full_url}")

    # فقط وبهوک؛ هیچ Flaskی اینجا نیست
    app.run_webhook(
      listen="0.0.0.0",
      port=PORT,
      url_path=TOKEN,
      webhook_url=full_url
    )

if __name__ == "__main__":
    logging.info("🚀 Bot starting in webhook mode…")
    main()
