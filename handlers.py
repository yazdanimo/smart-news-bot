import logging
from telegram import Update
from telegram.ext import ContextTypes
from config import CHANNEL_ID
from db import is_duplicate, save_message

async def debug_and_handle(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    """
    1) لاگ همهٔ پیام‌های متنی (دایرکت/گروه/کانال)
    2) اگر پست کانال بود، تکرار را چک و حذف/ذخیره کند
    """
    msg = update.message or update.channel_post
    if not msg or not msg.text:
        return

    logging.info(f"[DEBUG] chat_id={msg.chat.id} ({msg.chat.type}): {msg.text}")

    if update.channel_post and msg.chat.id == CHANNEL_ID:
        text = msg.text.strip()
        if is_duplicate(text):
            await context.bot.delete_message(
                chat_id=CHANNEL_ID,
                message_id=msg.message_id
            )
            logging.info(f"❌ حذف تکراری: {text}")
        else:
            save_message(text)
            logging.info(f"✅ ثبت جدید: {text}")
