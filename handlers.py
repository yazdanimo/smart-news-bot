# handlers.py
import hashlib
from telegram import Update
from telegram.ext import CallbackContext

from db import is_duplicate, add_item

def hash_text(text: str) -> str:
    return hashlib.sha256(text.strip().encode('utf-8')).hexdigest()

def news_handler(update: Update, context: CallbackContext):
    msg = update.effective_message
    text = msg.text or ""
    chat_id = update.effective_chat.id

    if not text:
        return

    key = hash_text(text)
    if is_duplicate(key):
        context.bot.delete_message(chat_id=chat_id, message_id=msg.message_id)
    else:
        add_item(key)
