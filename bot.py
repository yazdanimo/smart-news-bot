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
    # ساخت اپلیکیشن
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # 1) لاگ همهٔ پیام‌های متنی
    app.add_handler(
        MessageHandler(filters.TEXT, debug_all_messages)
    )

    # 2) هندل کردن پست‌های کانال
    app.add_handler(
        MessageHandler(
            filters.UpdateType.CHANNEL_POST & filters.TEXT,
            handle_channel_post
        )
    )

    # ست‌کردن وبهوک
    path       = f"/{BOT_TOKEN}"
    full_url   = f"{WEBHOOK_URL}{path}"
    logging.info(f"🔗 ست وبهوک روی {full_url}")

    # اجرای وبهوک (تک‌سرور Tornado روی پورت مشخص)
    app.run_webhook(
        listen="0.0.0.0",
        port=PORT,
        url_path=BOT_TOKEN,
        webhook_url=full_url
    )

if __name__ == "__main__":
    logging.info("🚀 بوت در حالت وبهوک شروع می‌شود…")
    main()
