import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import (
    ApplicationBuilder, MessageHandler,
    filters, ContextTypes
)
from db import is_duplicate, save_message

load_dotenv()
TOKEN = os.getenv("8029865209:AAGsg6GSv6fFOxe9xsnRiBnay8UHiL8tALU")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text:
        return
    
    text = update.message.text.strip()
    chat = update.effective_chat
    message_id = update.message.message_id

    if is_duplicate(text):
        await context.bot.delete_message(chat_id=chat.id, message_id=message_id)
        print(f"❌ پیام تکراری حذف شد: {text}")
    else:
        save_message(text)
        print(f"✅ پیام جدید ذخیره شد: {text}")

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT & filters.ChatType.CHANNEL, handle_message))

if __name__ == "__main__":
    print("✅ ربات در حال اجراست...")
    app.run_polling()
