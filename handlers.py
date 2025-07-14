import logging
from telegram import Update
from telegram.ext import ContextTypes
from db import is_duplicate, save_message
from config import CHANNEL_ID

async def debug_all_messages(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    """
    لاگ همهٔ پیام‌های متنی (کاربران در گروه/دایرکت)
    """
    msg = update.message or update.channel_post
    if msg and msg.text:
        logging.info(f"[DEBUG] chat_id={msg.chat.id} ({msg.chat.type}): {msg.text}")

async def handle_channel_post(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    """
    پردازش پست‌های کانال:
    - اگر تکراری بود، حذف شود
    - در غیر این صورت، در DB ذخیره شود
    """
    post = update.channel_post
    if not post or not post.text or post.chat.id != CHANNEL_ID:
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
