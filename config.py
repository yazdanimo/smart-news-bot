import os

# توکن ربات را از متغیر محیطی دریافت کنید
TOKEN = os.getenv('TELEGRAM_TOKEN', 'YOUR_TELEGRAM_BOT_TOKEN')

# آدرس پایه اپ شما (مثلا Railway)
BASE_URL = os.getenv('BASE_URL', 'https://web-production-3eaab.up.railway.app')

# مسیر ذخیره‌سازی دیتابیس SQLite
DB_PATH = os.getenv('DB_PATH', 'news.db')

# پورت پیش‌فرض برای وب‌هوک
PORT = int(os.getenv('PORT', 8443))
