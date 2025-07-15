import sqlite3
from config import DB_PATH

def init_db():
    """ایجاد جدول news اگر وجود نداشته باشد."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        """
        CREATE TABLE IF NOT EXISTS news (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            item_hash TEXT UNIQUE,
            added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
    )
    conn.commit()
    conn.close()

def is_duplicate(item_hash: str) -> bool:
    """بررسی می‌کند آیا شناسه خبر قبلاً ذخیره شده یا خیر."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT 1 FROM news WHERE item_hash = ?", (item_hash,))
    exists = c.fetchone() is not None
    conn.close()
    return exists

def add_item(item_hash: str):
    """اضافه کردن شناسه خبر جدید به دیتابیس."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT OR IGNORE INTO news (item_hash) VALUES (?)", (item_hash,))
    conn.commit()
    conn.close()
