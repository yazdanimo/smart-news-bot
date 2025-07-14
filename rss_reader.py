import feedparser
from db import is_duplicate, save_message
from config import BOT_TOKEN, CHANNEL_ID
from telegram import Bot

FEEDS = [
    "https://example.com/rss",
    # URL‌های دیگر...
]

def fetch_and_send():
    bot = Bot(BOT_TOKEN)
    for url in FEEDS:
        feed = feedparser.parse(url)
        for entry in feed.entries:
            text = f"{entry.title}\n{entry.link}"
            if not is_duplicate(text):
                bot.send_message(chat_id=CHANNEL_ID, text=text)
                save_message(text)
