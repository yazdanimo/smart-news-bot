# handlers.py
import logging
from telegram import Update
from telegram.ext import ContextTypes, MessageHandler, filters
from config import CHANNEL_ID, MODE
from db import save_message, create_answer

# پیکربندی لاگر
logger = logging.getLogger(__name__)
logging.basicConfig(
    format="%(asctime)s %(levelname)s: %(message)s",
    level=logging.DEBUG,
)

async def debug_all(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    چاپ تمام آپدیت‌های دریافتی برای دیباگ
    """
    logger.debug("GOT UPDATE: %s", update.to_dict())

async def handle_all(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    پردازش پست‌های کانال (یا پیام‌های خصوصی اگر خواستید)
    """
    # پست کانال یا پیام عادی
    msg = update.channel_post or update.message
    if not msg or msg.chat.id != CHANNEL_ID:
        return

    text = msg.text or msg.caption or ""
    logger.debug(f"{CHANNEL_ID} (raw): {text}")

    # ذخیره در دیتابیس
    if save_message(text):
        logger.info(f"✅ ثبت جدید: {text}")
    else:
        logger.info(f"❌ حذف تکراری: {text}")

    # Polling: حذف پیام اصلی
    if MODE == "polling":
        try:
            await context.bot.delete_message(
                chat_id=CHANNEL_ID,
                message_id=msg.message_id
            )
        except Exception as e:
            logger.error(f"delete_message failed: {e}")

    # Webhook: ارسال پاسخ
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
