# bot.py
import logging
from telegram.ext import ApplicationBuilder, MessageHandler, filters
from config import BOT_TOKEN, CHANNEL_ID, MODE, WEBHOOK_URL, PORT
from handlers import debug_all, handle_all

# پیکربندی لاگر
logging.basicConfig(
    format="%(asctime)s %(levelname)s: %(message)s",
    level=logging.DEBUG,
)
logger = logging.getLogger(__name__)

def main():
    # لاگ تمیزسازی‌شده برای اطمینان
    logger.debug(f"Clean BOT_TOKEN   = {BOT_TOKEN!r}")
    logger.debug(f"Clean WEBHOOK_URL = {WEBHOOK_URL!r}")

    # ساخت URL نهایی وبهوک (بدون سمی‌کالن)
    webhook_url = f"{WEBHOOK_URL}/{BOT_TOKEN}"
    # ← اینجا **سمی‌کالن** بعد از لگ را حذف کنید
    logger.info(f"🔗 Setting webhook_url: {webhook_url!r}")

    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # هندلر لاگ همه آپدیت‌ها
    app.add_handler(MessageHandler(filters.ALL, debug_all), group=0)

    # هندلر پست‌های کانال
    channel_filter = filters.Chat(CHANNEL_ID) & (
        filters.TEXT | filters.UpdateType.CHANNEL_POST
    )
    app.add_handler(MessageHandler(channel_filter, handle_all))

    if MODE == "polling":
        logger.info("🔄 در حالت polling اجرا می‌شود")
        app.run_polling()
    else:
        logger.info("🚀 در حالت webhook اجرا می‌شود")
        # پارامتر webhook_url هم بدون سمی‌کالن است
        app.run_webhook(
            listen="0.0.0.0",
            port=int(PORT),
            webhook_url=webhook_url
        )

if __name__ == "__main__":
    main()
