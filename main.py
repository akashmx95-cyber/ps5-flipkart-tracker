import requests
from bs4 import BeautifulSoup
import time
from datetime import datetime
import os
from flask import Flask
import threading

PRODUCT_URL = "https://www.flipkart.com/sony-playstation5-console-slim-cfi-2008a01x-cfi-2116a01y-1-tb/p/itm89489e2adcd2c?pid=GMCGZCYPAFYBUNAR"
CHECK_INTERVAL = 300

app = Flask(__name__)

@app.route('/')
def home():
    return "<h1>✅ PS5 Stock Tracker is RUNNING on Render</h1>"

def send_telegram(message):
    token = os.environ.get("BOT_TOKEN")
    chat_id = os.environ.get("CHAT_ID")
    if not token or not chat_id:
        print("❌ Missing BOT_TOKEN or CHAT_ID")
        return
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    try:
        requests.post(url, json={"chat_id": chat_id, "text": message, "parse_mode": "HTML"})
        print("✅ Telegram message sent successfully")
    except Exception as e:
        print(f"Telegram error: {e}")

def check_stock():
    try:
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
        resp = requests.get(PRODUCT_URL, headers=headers, timeout=15)
        page_lower = resp.text.lower()
        title = "Sony PlayStation 5 Slim 1TB"
        
        in_stock = any(word in page_lower for word in ["add to cart", "buy now"])
        timestamp = datetime.now().strftime('%H:%M:%S')
        
        if in_stock:
            msg = f"""<b>🎮 PS5 IN STOCK RIGHT NOW! 🎉</b>

{title}
🔗 {PRODUCT_URL}
🕒 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"""
            send_telegram(msg)
            print(f"[{timestamp}] ✅ STOCK FOUND & ALERT SENT!")
        else:
            print(f"[{timestamp}] Still Notify Me / Out of stock")
    except Exception as e:
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Error: {e}")

def run_checker():
    print("🚀 Background Stock Checker Started")
    time.sleep(8)   # Wait for server to fully start
    while True:
        check_stock()
        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    # Start background checker
    threading.Thread(target=run_checker, daemon=True).start()
    print("🚀 Flask Server Starting...")
    
    # Let Flask/gunicorn handle the rest
    app.run(host='0.0.0.0', port=8080)
