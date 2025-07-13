import sqlite3

conn = sqlite3.connect("messages.db", check_same_thread=False)
c = conn.cursor()

c.execute("""
    CREATE TABLE IF NOT EXISTS messages (
        text TEXT PRIMARY KEY
    )
""")
conn.commit()

def is_duplicate(text):
    c.execute("SELECT text FROM messages WHERE text=?", (text,))
    return c.fetchone() is not None

def save_message(text):
    c.execute("INSERT INTO messages (text) VALUES (?)", (text,))
    conn.commit()
