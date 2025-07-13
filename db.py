import sqlite3

conn = sqlite3.connect("messages.db", check_same_thread=False)
c = conn.cursor()

c.execute("""
    CREATE TABLE IF NOT EXISTS messages (
        text TEXT PRIMARY KEY
    )
""")
conn.commit()

def is_duplicate(text: str) -> bool:
    c.execute("SELECT 1 FROM messages WHERE text=?", (text,))
    return c.fetchone() is not None

def save_message(text: str):
    c.execute("INSERT INTO messages (text) VALUES (?)", (text,))
    conn.commit()
