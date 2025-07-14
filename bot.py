import logging
from telegram.ext import (
    ApplicationBuilder,
    MessageHandler,
    filters
)
from handlers import debug_all_messages, handle_channel_post
from config import BOT_TOKEN, WEBHOOK_URL, PORT

# تنظیمات لاگ
logging.basicConfig(
    format="%(asctime)s %(levelname)s: %(message)s",
    level=logging.INFO
)

def main():
    # ساخت اپلیکیشن تلگرام با توکن
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # 1) هندلر لاگ تمام پیام‌های متنی (کاربر در گروه/دایرکت و پست‌های کانال)
    app.add_handler(
        MessageHandler(filters.TEXT, debug_all_messages)
    )

    # 2) هندلر اختصاصی پست‌های کانال
    app.add_handler(
        MessageHandler(
            filters.UpdateType.CHANNEL_POST & filters.TEXT,
            handle_channel_post
        )
    )

    # ست کردن وبهوک روی مسیر شامل توکن
    webhook_path = f"/{BOT_TOKEN}"
    full_webhook = f"{WEBHOOK_URL}{webhook_path}"
    logging.info(f"🔗 ست وبهوک روی {full_webhook}")

    # اجرای وبهوک (یک سرور Tornado روی پورت مشخص)
    app.run_webhook(
        listen="0.0.0.0",
        port=PORT,
        url_path=BOT_TOKEN,
        webhook_url=full_webhook
    )

if __name__ == "__main__":
    logging.info("🚀 بوت در حالت وبهوک شروع می‌شود…")
    main()
