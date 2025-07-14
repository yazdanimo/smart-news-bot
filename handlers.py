# handlers.py

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
    Log every incoming text (messages & channel posts) for debugging.
    """
    msg = update.effective_message
    if msg and msg.text:
        logging.info(f"[DEBUG] chat_id={msg.chat.id} ({msg.chat.type}): {msg.text}")

async def handle_channel_post(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    """
    Process posts that appear in the configured channel:
    - If text is duplicate, delete it.
    - Otherwise, save it to the DB.
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
