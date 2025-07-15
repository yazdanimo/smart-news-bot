# db.py
import sqlite3
from config import DB_PATH

# ایجاد جدول در صورت عدم وجود
def init_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            text TEXT PRIMARY KEY,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

# ذخیرهٔ پیام؛ برمی‌گرداند True اگر جدید بوده، False اگر تکراری
def save_message(text: str) -> bool:
    init_db()
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    try:
        cur.execute("INSERT INTO messages (text) VALUES (?)", (text,))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

# ساخت پاسخ ساده (این تابع را به دلخواه توسعه دهید)
def create_answer(text: str) -> str:
    return f"✅ دریافت شد: «{text}»"
