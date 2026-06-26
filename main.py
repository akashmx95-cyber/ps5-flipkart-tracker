import requests
from bs4 import BeautifulSoup
import time
from datetime import datetime
import os
from flask import Flask
from threading import Thread

PRODUCT_URL = "https://www.flipkart.com/sony-playstation5-console-slim-cfi-2008a01x-cfi-2116a01y-1-tb/p/itm89489e2adcd2c?pid=GMCGZCYPAFYBUNAR"
CHECK_INTERVAL = 300  # 5 minutes

app = Flask(__name__)

@app.route('/')
def home():
    return "✅ PS5 Flipkart Stock Tracker is running!"

def send_telegram(message):
    token = os.environ.get("BOT_TOKEN")
    chat_id = os.environ.get("CHAT_ID")
    if not token or not chat_id:
        print("❌ Telegram credentials missing")
        return
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {"chat_id": chat_id, "text": message, "parse_mode": "HTML"}
    try:
        requests.post(url, json=payload, timeout=10)
    except:
        pass

def check_stock():
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        resp = requests.get(PRODUCT_URL, headers=headers, timeout=15)
        soup = BeautifulSoup(resp.text, 'html.parser')
        
        title = soup.find('h1').get_text(strip=True)[:100] if soup.find('h1') else "PS5 Slim 1TB"
        page_lower = resp.text.lower()
        
        in_stock = any(word in page_lower for word in ["add to cart", "buy now"])
        
        if in_stock:
            msg = f"""<b>🎮 PS5 IN STOCK RIGHT NOW! 🎉</b>

{title}
🔗 {PRODUCT_URL}
🕒 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"""
            send_telegram(msg)
            print("✅ STOCK ALERT SENT!")
        else:
            print(f"[{datetime.now().strftime('%H:%M')}] Still out of stock")
    except Exception as e:
        print(f"Error: {e}")

def background_checker():
    print("🚀 Background stock checker started")
    while True:
        check_stock()
        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    Thread(target=background_checker, daemon=True).start()
    app.run(host='0.0.0.0', port=8080)
