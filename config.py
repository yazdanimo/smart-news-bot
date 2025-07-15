import os

# توکن بات
BOT_TOKEN = os.getenv("BOT_TOKEN", "YOUR_TELEGRAM_BOT_TOKEN")

# URL کامل وب‌هوک (مثلاً https://<app>.up.railway.app/<BOT_TOKEN>)
WEBHOOK_URL = os.getenv("WEBHOOK_URL", "")

# پورت اجرا (برای حالت وب‌هوک)
PORT = int(os.getenv("PORT", "8443"))

# شناسه‌ی ثابت چت (برای ارسال پیام‌های سیستمی اگر لازم باشد)
CHAT_ID = os.getenv("CHAT_ID", "")

# مسیر دیتابیس SQLite
DB_PATH = os.getenv("DB_PATH", "news.db")

# حالت اجرا: "webhook" یا "polling"
MODE = os.getenv("MODE", "webhook")
