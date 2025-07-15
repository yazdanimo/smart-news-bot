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
    # ساخت اپلیکیشن با توکن
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # 1) لاگ همه آپدیت‌ها برای دیباگ
    app.add_handler(
        MessageHandler(filters.ALL, debug_all),
        group=0
    )

    # 2) فیلتر برای پست‌های کانال
    channel_filter = filters.Chat(CHANNEL_ID) & (
        filters.TEXT | filters.UpdateType.CHANNEL_POST
    )
    app.add_handler(
        MessageHandler(channel_filter, handle_all)
    )

    # 3) انتخاب حالت اجرا
    if MODE == "polling":
        logger.info("🔄 در حالت polling اجرا می‌شود")
        app.run_polling()
    else:
        # محاسبه و لاگ دقیق webhook_url برای اطمینان از عدم وجود سمی‌کالن اضافی
        webhook_url = f"{WEBHOOK_URL.rstrip(';/')}/{BOT_TOKEN}"
        logger.info(f"🔗 Setting webhook_url: {webhook_url!r}")

        logger.info("🚀 در حالت webhook اجرا می‌شود")
        app.run_webhook(
            listen="0.0.0.0",
            port=int(PORT),
            webhook_url=webhook_url
        )

if __name__ == "__main__":
    main()
