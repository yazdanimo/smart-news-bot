import sqlite3

# اتصال به پایگاه داده‌ی SQLite
conn = sqlite3.connect("messages.db", check_same_thread=False)
cursor = conn.cursor()

# ایجاد جدول در صورت نبودن
cursor.execute("""
    CREATE TABLE IF NOT EXISTS messages (
        text TEXT PRIMARY KEY
    )
""")
conn.commit()

def is_duplicate(text: str) -> bool:
    cursor.execute("SELECT 1 FROM messages WHERE text = ?", (text,))
    return cursor.fetchone() is not None

def save_message(text: str):
    cursor.execute("INSERT INTO messages (text) VALUES (?)", (text,))
    conn.commit()
    print(f"[DB] saved -> {text}", flush=True)
