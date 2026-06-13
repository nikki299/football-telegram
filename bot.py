import requests
import os
import time
import feedparser
from bs4 import BeautifulSoup
from datetime import datetime

TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def send_telegram(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    data = {
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": "HTML"
    }
    requests.post(url, data=data)

# === 1. Transfer News (RSS) ===
def get_transfers():
    feeds = [
        "https://www.eyefootball.com/rss_news_transfers.xml",
        "https://talksport.com/rss/sports-news/football/transfer-rumours/feed/",
        # Add more if you want
    ]
    messages = []
    for url in feeds:
        try:
            feed = feedparser.parse(url)
            for entry in feed.entries[:2]:  # Limit to avoid spam
                title = entry.title
                link = entry.link
                msg = f"🚨 <b>TRANSFER UPDATE</b>\n\n{title}\n\n🔗 <a href='{link}'>Read more</a>\n\nHere we go! 🔥"
                messages.append(msg)
        except:
            pass
    return messages

# === 2. Quick Goals / Live Scores ===
def get_live_goals():
    # Using football-data.org (free, get token at football-data.org)
    # For now, simple fallback + Scorebat style
    messages = []
    try:
        # Public live matches example (expand later)
        msg = f"⚽ <b>LIVE MATCH CHECK</b>\nChecking current matches...\n(Goal alerts coming soon with free API key)\nHere we go! 🔥"
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
            title = item.get("title", "Goal Highlight")
            comp = item.get("competition", "")
            url = item.get("url", "")
            msg = f"🎥 <b>HIGHLIGHT</b>\n{title}\n{comp}\n\nWatch: {url}\n\nHere we go! 🔥"
            messages.append(msg)
        return messages
    except:
        return ["🎥 Highlights loading... (free API)"]

if name == "__main__":
    print("Starting football bot...")
    
    # Send Transfers
    for msg in get_transfers():
        send_telegram(msg)
        time.sleep(3)
    
    # Send Live Goals
    for msg in get_live_goals():
        send_telegram(msg)
        time.sleep(3)
    
    # Send Highlights
    for msg in get_highlights():
        send_telegram(msg)
        time.sleep(3)
    
    print("✅ Bot run completed")
