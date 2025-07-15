import logging
from telegram import Update
from telegram.ext import ContextTypes
from config import CHANNEL_ID
from db import is_duplicate, save_message

async def handle_channel_post(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    """
    ۱) لاگ پست‌های کانال (+ فیلتر CHANNEL_ID)
    ۲) در صورت تکراری بودن حذف و در غیر این صورت ذخیره
    """
    post = update.channel_post
    if not post or not post.text or post.chat.id != CHANNEL_ID:
        return

    text = post.text.strip()
    logging.info(f"[DEBUG] chat_id={post.chat.id} (channel): {text}")

    if is_duplicate(text):
        await context.bot.delete_message(
            chat_id=CHANNEL_ID,
            message_id=post.message_id
        )
        logging.info(f"❌ حذف تکراری: {text}")
    else:
        save_message(text)
        logging.info(f"✅ ثبت جدید: {text}")

async def debug_messages(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    """
    لاگ همهٔ پیام‌های متنی (دایرکت/گروه/کانال)
    """
    msg = update.message or update.channel_post
    if msg and msg.text:
        logging.info(f"[DEBUG] chat_id={msg.chat.id} ({msg.chat.type}): {msg.text}")
