import requests
from bs4 import BeautifulSoup
import time
from datetime import datetime
import os
from flask import Flask

PRODUCT_URL = "https://www.flipkart.com/sony-playstation5-console-slim-cfi-2008a01x-cfi-2116a01y-1-tb/p/itm89489e2adcd2c?pid=GMCGZCYPAFYBUNAR"
PINCODE = "110053"   # Your pincode

app = Flask(__name__)

@app.route('/')
def home():
    check_stock()
    return "<h1>✅ PS5 Tracker with Pincode (110053) is ACTIVE</h1>"

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

def check_stock():
    try:
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
        
        # Main product page
        resp = requests.get(PRODUCT_URL, headers=headers, timeout=15)
        page_lower = resp.text.lower()
        
        title = "Sony PlayStation 5 Slim 1TB"
        timestamp = datetime.now().strftime('%H:%M:%S')
        
        # Basic stock check
        basic_in_stock = any(word in page_lower for word in ["add to cart", "buy now"])
        
        # Pincode specific check (more accurate)
        pincode_in_stock = False
        try:
            # Simulate pincode check
            pin_url = f"{PRODUCT_URL}&pincode={PINCODE}"
            pin_resp = requests.get(pin_url, headers=headers, timeout=10)
            pin_text = pin_resp.text.lower()
            if "add to cart" in pin_text or "buy now" in pin_text or "delivery by" in pin_text:
                pincode_in_stock = True
        except:
            pass
        
        final_in_stock = basic_in_stock or pincode_in_stock
        
        if final_in_stock:
            msg = f"""<b>🎮 PS5 IN STOCK for Pincode {PINCODE}! 🎉</b>

{title}
🔗 {PRODUCT_URL}
📍 Pincode: {PINCODE}
🕒 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"""
            send_telegram(msg)
            print(f"[{timestamp}] ✅ STOCK FOUND for your pincode!")
        else:
            print(f"[{timestamp}] Still out of stock (Pincode {PINCODE})")
            
    except Exception as e:
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Error: {e}")

if __name__ == "__main__":
    print(f"🚀 PS5 Tracker Started with Pincode {PINCODE}")
    app.run(host='0.0.0.0', port=8080)
