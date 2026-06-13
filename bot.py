import requests
import os
import time
import feedparser
from bs4 import BeautifulSoup

TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def send_telegram(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    data = {
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": "HTML"
    }
    response = requests.post(url, data=data)
    print("Telegram response:", response.status_code)

# === 1. Transfer News ===
def get_transfers():
    feeds = [
        "https://www.eyefootball.com/rss_news_transfers.xml",
        "https://talksport.com/rss/sports-news/football/transfer-rumours/feed/",
    ]
    messages = []
    for url in feeds:
        try:
            feed = feedparser.parse(url)
            for entry in feed.entries[:2]:
                title = entry.title
                link = entry.link
                msg = f"🚨 <b>TRANSFER UPDATE</b>\n\n{title}\n\n🔗 <a href='{link}'>Read more</a>\n\nHere we go! 🔥"
                messages.append(msg)
        except:
            pass
    return messages

# === 2. Live Goals (basic for now) ===
def get_live_goals():
    messages = []
    try:
        msg = "⚽ <b>LIVE GOAL ALERTS</b>\n\n(We'll add real-time goals soon with a free API key)\nHere we go! 🔥"
        messages.append(msg)
    except:
        pass
    return messages

# === 3. Highlights ===
def get_highlights():
    try:
        resp = requests.get("https://www.scorebat.com/video-api/v3/", timeout=15)
        data = resp.json()
        messages = []
        for item in data.get("response", [])[:3]:
            title = item.get("title", "Highlight")
            comp = item.get("competition", "")
            url = item.get("url", "")
            msg = f"🎥 <b>HIGHLIGHT</b>\n{title}\n{comp}\n\nWatch: {url}\n\nHere we go! 🔥"
            messages.append(msg)
        return messages
    except:
        return ["🎥 <b>HIGHLIGHTS</b>\nLoading latest goals..."]

if name == "__main__":
    print("Starting football bot...")
    
    # Transfers
    for msg in get_transfers():
        send_telegram(msg)
        time.sleep(3)
    
    # Live Goals
    for msg in get_live_goals():
        send_telegram(msg)
        time.sleep(3)
    
    # Highlights
    for msg in get_highlights():
        send_telegram(msg)
        time.sleep(3)
    
    print("✅ Bot run completed")
