import hashlib
from telegram import Update
from telegram.ext import CallbackContext, MessageHandler, Filters
from db import is_duplicate, add_item

def hash_text(text: str) -> str:
    """از SHA256 برای تولید شناسه یکتا از متن خبر استفاده می‌کنیم."""
    return hashlib.sha256(text.strip().encode('utf-8')).hexdigest()

def news_handler(update: Update, context: CallbackContext):
    text = update.effective_message.text or ""
    message_id = update.effective_message.message_id
    chat_id = update.effective_chat.id

    # اگر پیام متنی نیست از آن صرف‌نظر می‌کنیم
    if not text:
        return

    item_hash = hash_text(text)
    if is_duplicate(item_hash):
        # خبر تکراریست؛ پیام را حذف می‌کنیم
        context.bot.delete_message(chat_id=chat_id, message_id=message_id)
    else:
        # خبر جدید است؛ در بانک ذخیره می‌کنیم
        add_item(item_hash)
