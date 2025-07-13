import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    MessageHandler,
    filters,
    ContextTypes
)
from db import is_duplicate, save_message

# بارگذاری متغیرهای محیطی
load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = int(os.getenv("CHANNEL_ID"))

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message
    # فقط متن‌ها
    if not msg or not msg.text:
        return

    # فقط از کانال/گروه مورد نظر پردازش کن
    if msg.chat.id != CHANNEL_ID:
        return

    text = msg.text.strip()
    # اگر تکراری بود، حذفش کن
    if is_duplicate(text):
        await context.bot.delete_message(chat_id=CHANNEL_ID, message_id=msg.message_id)
        print(f"❌ پیام تکراری حذف شد: {text}")
    else:
        save_message(text)
        print(f"✅ پیام جدید ثبت شد: {text}")

if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    # فقط پیام‌های متنی اونو اضافه کن
    app.add_handler(
        MessageHandler(
            filters.TEXT & filters.Chat(chat_id=CHANNEL_ID),
            handle_message
        )
    )
    print("🚀 ربات در حال اجراست...")
    app.run_polling()
