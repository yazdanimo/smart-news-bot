import logging
from telegram.ext import ApplicationBuilder, MessageHandler, filters
from handlers import debug_and_handle
from config import BOT_TOKEN, CHANNEL_ID, WEBHOOK_URL, PORT

# اینجا اول basicConfig
logging.basicConfig(
    format="%(asctime)s %(levelname)s: %(message)s",
    level=logging.INFO
)

# حالا می‌شود INFOها را دید
logging.info(
    f"Loaded config → BOT_TOKEN(len)={len(BOT_TOKEN)}, "
    f"CHANNEL_ID={CHANNEL_ID}, "
    f"WEBHOOK_URL={WEBHOOK_URL}, "
    f"PORT={PORT}"
)

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT, debug_and_handle))

    webhook_url = f"{WEBHOOK_URL}/{BOT_TOKEN}"
    logging.info(f"🔗 ست وبهوک روی {webhook_url}")

    app.run_webhook(
        listen="0.0.0.0",
        port=PORT,
        url_path=BOT_TOKEN,
        webhook_url=webhook_url
    )

if __name__ == "__main__":
    logging.info("🚀 بوت در حالت وبهوک شروع می‌شود…")
    main()
