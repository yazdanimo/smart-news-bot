# handlers.py

import hashlib
import re
import html
import unicodedata

from telegram import Update
from telegram.ext import CallbackContext
from db import is_duplicate, add_item

def normalize_text(text: str) -> str:
    """
    - تبدیل HTML entities (مثلاً &quot; → ")
    - حذف لینک‌ها و یوزرنیم‌ها
    - حذف علائم نگارشی و نمادها (اموجی و …) با استفاده از دسته‌بندی یونیکد
    - حذف فاصله‌های اضافی
    """
    # Decode HTML entities
    text = html.unescape(text)

    # Remove URLs and usernames
    text = re.sub(r'https?://\S+', '', text)
    text = re.sub(r'@\S+', '', text)

    # Keep only letters/numbers/spaces, drop punctuation, symbols, control chars
    chars = []
    for ch in text:
        cat = unicodedata.category(ch)
        if cat.startswith(('P', 'S', 'C')):   # P=punctuation, S=symbol, C=control
            continue
        chars.append(ch)
    text = ''.join(chars)

    # Normalize whitespace
    text = ' '.join(text.split())

    return text.strip()

def hash_text(text: str) -> str:
    """
    تولید هش SHA256 از کل متن نرمال‌شده
    """
    cleaned = normalize_text(text)
    return hashlib.sha256(cleaned.encode('utf-8')).hexdigest()

def news_handler(update: Update, context: CallbackContext):
    """
    اگر متن خبر (بعد از نرمال‌سازی) تکراری باشد → حذف
    در غیر این صورت → ذخیره در دیتابیس
    """
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
