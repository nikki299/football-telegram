import requests
import os
import time

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
    print("✅ Sent:", response.status_code)

if __name__ == "__main__":
    print("🚀 Starting simple test...")
    
    test_msg = "🧪 <b>Test Message from your Football Bot</b>\n\nThis is a test.\n\nHere we go! 🔥"
    send_telegram(test_msg)
    
    print("✅ Test completed!")
