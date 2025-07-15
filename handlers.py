# handlers.py
import logging
from telegram import Update
from telegram.ext import ContextTypes, MessageHandler, filters
from config import CHANNEL_ID, MODE
from db import save_message, create_answer

# تنظیم لاگر
logging.basicConfig(
    format="%(asctime)s %(levelname)s: %(message)s",
    level=logging.DEBUG,
)
logger = logging.getLogger(__name__)

async def debug_all(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    لاگ تمام بروزرسانی‌ها برای دیباگ
    (باید گروه 0 در bot.py با این هندلر رجیستر شده باشد)
    """
    logger.debug("GOT UPDATE: %s", update.to_dict())

async def handle_all(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    رسیدگی به پیام‌های کانال:
    - ذخیره‌ی متن جدید
    - حذف تکراری یا ارسال پاسخ
    """
    # در حالت وبهوک پیام در update.channel_post قرار می‌گیرد
    msg = update.channel_post or update.message
    if not msg or msg.chat.id != CHANNEL_ID:
        return

    text = msg.text or msg.caption or ""
    logger.debug(f"{CHANNEL_ID} raw text: {text}")

    if save_message(text):
        logger.info(f"✅ ثبت جدید: {text}")
    else:
        logger.info(f"❌ حذف تکراری: {text}")

    # اگر حالت polling باشد، پیام اصلی حذف شود
    if MODE == "polling":
        try:
            await context.bot.delete_message(
                chat_id=CHANNEL_ID,
                message_id=msg.message_id
            )
        except Exception as e:
            logger.error(f"delete_message failed: {e}")
    # در حالت webhook پاسخ ارسال می‌شود
    else:
        try:
            answer = create_answer(text)
            await context.bot.send_message(
                chat_id=CHANNEL_ID,
                text=answer,
                reply_to_message_id=msg.message_id
            )
        except Exception as e:
            logger.error(f"send_message failed: {e}")
