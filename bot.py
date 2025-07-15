# bot.py
import logging
from telegram.ext import ApplicationBuilder, MessageHandler, filters
from config import BOT_TOKEN, CHANNEL_ID, MODE, WEBHOOK_URL, PORT
from handlers import debug_all, handle_all

logging.basicConfig(
    format="%(asctime)s %(levelname)s: %(message)s",
    level=logging.DEBUG,
)
logger = logging.getLogger(__name__)

def main():
    # لاگ برای اطمینان از تمیز بودن آدرس‌ها
    logger.debug(f"Clean BOT_TOKEN   = {BOT_TOKEN!r}")
    logger.debug(f"Clean WEBHOOK_URL = {WEBHOOK_URL!r}")

    # ترکیب نهایی آدرس وبهوک
    webhook_url = f"{WEBHOOK_URL}/{BOT_TOKEN}"
    logger.info(f"🔗 Setting webhook_url: {webhook_url!r}")

    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.ALL, debug_all), group=0)

    channel_filter = filters.Chat(CHANNEL_ID) & (
        filters.TEXT | filters.UpdateType.CHANNEL_POST
    )
    app.add_handler(MessageHandler(channel_filter, handle_all))

    if MODE == "polling":
        logger.info("🔄 در حالت polling اجرا می‌شود")
        app.run_polling()
    else:
        logger.info("🚀 در حالت webhook اجرا می‌شود")
        app.run_webhook(
            listen="0.0.0.0",
            port=int(PORT),
            webhook_url=webhook_url
        )

if __name__ == "__main__":
    main()
