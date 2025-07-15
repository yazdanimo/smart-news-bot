import logging
from telegram.ext import ApplicationBuilder, MessageHandler, filters
from handlers import handle_channel_post, debug_messages
from config import BOT_TOKEN, CHANNEL_ID, WEBHOOK_URL, PORT

# تنظیم لاگ
logging.basicConfig(
    format="%(asctime)s %(levelname)s: %(message)s",
    level=logging.INFO
)
logging.info(
    f"Loaded config → BOT_TOKEN(len)={len(BOT_TOKEN)}, "
    f"CHANNEL_ID={CHANNEL_ID}, "
    f"WEBHOOK_URL={WEBHOOK_URL}, "
    f"PORT={PORT}"
)

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # 1) هندلر اختصاصی پست‌های کانال
    app.add_handler(
        MessageHandler(
            filters.UpdateType.CHANNEL_POST & filters.TEXT,
            handle_channel_post
        )
    )

    # 2) هندلر لاگ تمام پیام‌های متنی
    app.add_handler(
        MessageHandler(filters.TEXT, debug_messages)
    )

    # ست کردن وبهوک
    webhook_url = f"{WEBHOOK_URL}/{BOT_TOKEN}"
    logging.info(f"🔗 Set webhook → {webhook_url}")

    app.run_webhook(
        listen="0.0.0.0",
        port=PORT,
        url_path=BOT_TOKEN,
        webhook_url=webhook_url
    )

if __name__ == "__main__":
    logging.info("🚀 Starting webhook…")
    main()
