import logging
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    MessageHandler,
    filters
)
from handlers import debug_all_messages, handle_channel_post
from config import BOT_TOKEN, CHANNEL_ID, WEBHOOK_URL, PORT

# تنظیم لاگ
logging.basicConfig(
    format="%(asctime)s %(levelname)s: %(message)s",
    level=logging.INFO
)

# هندلرها و وبهوک
def main():
    application = ApplicationBuilder().token(BOT_TOKEN).build()

    # لاگ همهٔ پیام‌های متنی
    application.add_handler(MessageHandler(filters.TEXT, debug_all_messages))

    # حذف/ثبت پیام‌های کانال
    application.add_handler(
        MessageHandler(
            filters.TEXT & filters.ChatType.CHANNEL,
            handle_channel_post
        )
    )

    # ست‌کردن Webhook
    path     = f"/{BOT_TOKEN}"
    full_url = f"{WEBHOOK_URL}{path}"
    logging.info(f"🔗 Setting webhook to {full_url}")

    application.run_webhook(
        listen="0.0.0.0",
        port=PORT,
        url_path=BOT_TOKEN,
        webhook_url=full_url
    )

if __name__ == "__main__":
    logging.info("🚀 Bot starting in webhook mode…")
    main()
