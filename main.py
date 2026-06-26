import requests
from bs4 import BeautifulSoup
import time
from datetime import datetime
import os
from flask import Flask

PRODUCT_URL = "https://www.flipkart.com/sony-playstation5-console-slim-cfi-2008a01x-cfi-2116a01y-1-tb/p/itm89489e2adcd2c?pid=GMCGZCYPAFYBUNAR"
CHECK_INTERVAL = 300

app = Flask(__name__)

@app.route('/')
def home():
    return "<h1>✅ PS5 Stock Tracker is RUNNING</h1><p>Check Logs for status</p>"

def send_telegram(message):
    token = os.environ.get("BOT_TOKEN")
    chat_id = os.environ.get("CHAT_ID")
    if not token or not chat_id:
        print("❌ BOT_TOKEN or CHAT_ID missing!")
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
        
        title = "PS5 Slim 1TB"
        in_stock = any(word in page_lower for word in ["add to cart", "buy now"])
        
        timestamp = datetime.now().strftime('%H:%M:%S')
        
        if in_stock:
            msg = f"""<b>🎮 PS5 IN STOCK RIGHT NOW! 🎉</b>

{title}
🔗 {PRODUCT_URL}
🕒 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"""
            send_telegram(msg)
            print(f"[{timestamp}] ✅ STOCK FOUND!")
        else:
            print(f"[{timestamp}] Still Notify Me / Out of stock")
            
    except Exception as e:
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Error: {e}")

print("🚀 PS5 Tracker Starting...")

if __name__ == "__main__":
    # Run one check immediately
    print("Running first stock check...")
    check_stock()
    
    # Then run continuously
    while True:
        check_stock()
        time.sleep(CHECK_INTERVAL)
