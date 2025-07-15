import hashlib
from telegram import Update
from telegram.ext import CallbackContext, MessageHandler, Filters
from db import is_duplicate, add_item

def hash_text(text: str) -> str:
    """
    از SHA256 برای تولید شناسه یکتا از متن خبر استفاده می‌کنیم.
    strip() و encode() برای یکسان‌سازی ورودی‌ها است.
    """
    return hashlib.sha256(text.strip().encode('utf-8')).hexdigest()

def news_handler(update: Update, context: CallbackContext):
    """
    این handler برای هر پیام متنی اجرا می‌شود.
    اگر خبر تکراری باشد، پیام حذف می‌گردد.
    در غیر این صورت شناسه ذخیره می‌شود.
    """
    message = update.effective_message
    text = message.text or ""
    chat_id = update.effective_chat.id

    if not text:
        return

    item_hash = hash_text(text)
    if is_duplicate(item_hash):
        context.bot.delete_message(chat_id=chat_id, message_id=message.message_id)
    else:
        add_item(item_hash)
