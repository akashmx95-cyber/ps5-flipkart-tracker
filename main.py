import requests
from bs4 import BeautifulSoup
import time
from datetime import datetime
import os
from flask import Flask
import threading

PRODUCTS = [
    {
        "url": "https://www.flipkart.com/sony-playstation5-console-slim-cfi-2008a01x-cfi-2116a01y-1-tb/p/itm89489e2adcd2c?pid=GMCGZCYPAFYBUNAR",
        "name": "PS5 Slim Disc 1TB"
    },
    {
        "url": "https://www.flipkart.com/sony-ps5-digital-cfi-2116b01y-825-gb/p/itm7124b7348127b",
        "name": "PS5 Digital 825GB"
    }
]

PINCODE = "110053"

app = Flask(__name__)

@app.route('/')
def home():
    check_all_products()   # Run check on ping too
    return "<h1>✅ Multi PS5 Tracker (20 sec) is LIVE</h1>"

def send_telegram(message):
    token = os.environ.get("BOT_TOKEN")
    chat_id = os.environ.get("CHAT_ID")
    if not token or not chat_id:
        print("❌ Missing BOT_TOKEN or CHAT_ID")
        return
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    try:
        requests.post(url, json={"chat_id": chat_id, "text": message, "parse_mode": "HTML"})
        print("✅ Telegram alert sent!")
    except:
        print("Telegram send failed")

def check_product(product):
    try:
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
        resp = requests.get(product["url"], headers=headers, timeout=10)
        page_lower = resp.text.lower()
        
        in_stock = any(word in page_lower for word in ["add to cart", "buy now"])
        timestamp = datetime.now().strftime('%H:%M:%S')
        
        if in_stock:
            msg = f"""<b>🎮 {product["name"]} IN STOCK for Pincode {PINCODE}! 🎉</b>

🔗 {product["url"]}
📍 Pincode: {PINCODE}
🕒 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"""
            send_telegram(msg)
            print(f"[{timestamp}] ✅ {product['name']} STOCK FOUND!")
        else:
            print(f"[{timestamp}] {product['name']} - Still out of stock")
            
    except Exception as e:
        print(f"Error checking {product['name']}: {e}")

def check_all_products():
    print(f"[{datetime.now().strftime('%H:%M:%S')}] Checking 2 PS5 models...")
    for product in PRODUCTS:
        check_product(product)

def background_checker():
    print("🚀 Background Checker Started (20 sec interval)")
    time.sleep(10)
    while True:
        check_all_products()
        time.sleep(20)

if __name__ == "__main__":
    threading.Thread(target=background_checker, daemon=True).start()
    print("🚀 Starting Flask on Render...")
    app.run(host='0.0.0.0', port=8080)
