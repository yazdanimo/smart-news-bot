import hashlib
import re
import string
import html

from telegram import Update
from telegram.ext import CallbackContext
from db import is_duplicate, add_item

def normalize_text(text: str) -> str:
    """
    پاک‌سازی عمیق برای حذف اجزای غیرمفید مثل لینک‌ها، ایموجی‌ها، علامت‌ها، فاصله‌ها
    هدف: استخراج هسته‌ی اصلی خبر برای تشخیص تکراری بودن
    """
    # تبدیل HTML entities مثل &quot; → "
    text = html.unescape(text)

    # حذف لینک‌ها و یوزرنیم‌ها
    text = re.sub(r'https?://\S+', '', text)
    text = re.sub(r'@\S+', '', text)

    # حذف ایموجی‌ها و کاراکترهای غیرقابل نمایش
    text = text.encode('ascii', 'ignore').decode('ascii')

    # حذف علامت‌های نگارشی
    text = text.translate(str.maketrans('', '', string.punctuation))

    # تبدیل همه‌ی حروف به کوچک
    text = text.lower()

    # حذف فاصله‌های اضافی
    text = ' '.join(text.split())

    return text.strip()


def extract_title_line(text: str) -> str:
    """
    فقط خط اول خبر بعد از نرمال‌سازی استخراج می‌شود (مثلاً تیتر خبر یا خلاصه)
    """
    lines = normalize_text(text).split('\n')
    return lines[0] if lines else ''


def hash_text(text: str) -> str:
    """
    تولید هش SHA256 بر اساس خط اول نرمال‌شده خبر
    """
    essence = extract_title_line(text)
    return hashlib.sha256(essence.encode('utf-8')).hexdigest()


def news_handler(update: Update, context: CallbackContext):
    """
    هندل‌کننده‌ی پیام‌ها:
    اگر خبر تکراری بود → حذف شود
    اگر جدید بود → ذخیره شود
    """
    msg = update.effective_message
    text = msg.text or ""
    chat_id = update.effective_chat.id

    if not text:
        return

    item_key = hash_text(text)

    if is_duplicate(item_key):
        context.bot.delete_message(chat_id=chat_id, message_id=msg.message_id)
    else:
        add_item(item_key)
