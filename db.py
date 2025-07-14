import sqlite3

# اتصال به دیتابیس (اگر وجود نداشته باشد، ساخته می‌شود)
conn = sqlite3.connect("messages.db", check_same_thread=False)
c = conn.cursor()

# جدول پیام‌ها
c.execute("""
    CREATE TABLE IF NOT EXISTS messages (
        text TEXT PRIMARY KEY
    )
""")
conn.commit()

def is_duplicate(text: str) -> bool:
    """بررسی اینکه آیا متن پیام قبلا ثبت شده یا نه."""
    c.execute("SELECT 1 FROM messages WHERE text=?", (text,))
    return c.fetchone() is not None

def save_message(text: str):
    """ثبت متن پیام در دیتابیس."""
    c.execute("INSERT INTO messages (text) VALUES (?)", (text,))
    conn.commit()
    print(f"[DB] saved -> {text}", flush=True)
