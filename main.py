import requests
from bs4 import BeautifulSoup
import time
from datetime import datetime
import os
from flask import Flask
import threading

PRODUCT_URL = "https://www.flipkart.com/sony-playstation5-console-slim-cfi-2008a01x-cfi-2116a01y-1-tb/p/itm89489e2adcd2c?pid=GMCGZCYPAFYBUNAR"
PINCODE = "110053"

app = Flask(__name__)

@app.route('/')
def home():
    return "<h1>✅ PS5 Tracker (Fast Mode - Every 2 min) is LIVE</h1>"

def send_telegram(message):
    token = os.environ.get("BOT_TOKEN")
    chat_id = os.environ.get("CHAT_ID")
    if not token or not chat_id:
        print("❌ Missing credentials")
        return
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    try:
        requests.post(url, json={"chat_id": chat_id, "text": message, "parse_mode": "HTML"})
        print("✅ Telegram alert sent!")
    except:
        print("Telegram send failed")

def check_stock():
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        resp = requests.get(PRODUCT_URL, headers=headers, timeout=15)
        page_lower = resp.text.lower()
        
        title = "Sony PlayStation 5 Slim 1TB"
        timestamp = datetime.now().strftime('%H:%M:%S')
        
        in_stock = any(word in page_lower for word in ["add to cart", "buy now"])
        
        if in_stock:
            msg = f"""<b>🎮 PS5 IN STOCK for Pincode {PINCODE}! 🎉</b>

{title}
🔗 {PRODUCT_URL}
📍 Pincode: {PINCODE}
🕒 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"""
            send_telegram(msg)
            print(f"[{timestamp}] ✅ STOCK FOUND!")
        else:
            print(f"[{timestamp}] Still out of stock")
            
    except Exception as e:
        print(f"Error: {e}")

def background_checker():
    print("🚀 Fast Background Checker Started (2 min interval)")
    time.sleep(5)
    while True:
        check_stock()
        time.sleep(120)  # 2 minutes - faster checks

if __name__ == "__main__":
    threading.Thread(target=background_checker, daemon=True).start()
    print("🚀 Starting on Railway...")
    app.run(host='0.0.0.0', port=os.environ.get("PORT", 8080))
