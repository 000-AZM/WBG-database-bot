from flask import Flask, request
import json
import os
import requests

# -----------------------------
# Telegram Bot Token
# -----------------------------
TOKEN = "8505220046:AAE7hfD9aKU7drBVuQZHUIiZZAAuaJV5LMM"
BASE_URL = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

# -----------------------------
# Load JSON database
# -----------------------------
BASE_DIR = os.path.dirname(__file__)
DATA_PATH = os.path.join(BASE_DIR, "data.json")

with open(DATA_PATH, "r", encoding="utf-8") as f:
    site_data = json.load(f)

# -----------------------------
# Flask app
# -----------------------------
app = Flask(__name__)

# -----------------------------
# Helper functions
# -----------------------------
def send_message(chat_id, text):
    payload = {"chat_id": chat_id, "text": text}
    requests.post(BASE_URL, json=payload)

def handle_site_code(chat_id, code):
    site = next((s for s in site_data if s["SiteID"].upper() == code.upper()), None)
    if site:
        reply = (
            f"📌 SiteID: {site['SiteID']}\n"
            f"Branch: {site['Branch']}\n"
            f"Township: {site['Township']}\n"
            f"On-Aired day: {site['On-Aired day']}\n"
            f"Site type: {site['Site type']}\n"
            f"Owner: {site['Owner']}\n"
            f"Team: {site['Team']}\n"
            f"Staff: {site['Staff']}\n"
            f"VCM code: {site['VCM code']}\n"
            f"Coordinates: {site['Lat']}, {site['Long']}\n\n"
            f"WBG database bot by Alua (https://t.me/aluaxeliana)"
        )
    else:
        reply = "❌ SiteID not found. Please try again."
    send_message(chat_id, reply)

# -----------------------------
# Webhook endpoint
# -----------------------------
@app.route("/telegram", methods=["POST"])
def webhook():
    try:
        update = request.get_json()
        print("Update received:", update)

        message = update.get("message")
        if message:
            chat_id = message["chat"]["id"]
            text = message.get("text", "").strip()

            if text.lower().startswith("/start"):
                send_message(chat_id, "👋 Welcome! Send a SiteID (like BGO0001) to get info.")
            elif text.lower().startswith("/help"):
                send_message(chat_id, "Send a SiteID to get site information.\nExample: BGO0001")
            else:
                handle_site_code(chat_id, text)

    except Exception as e:
        print("ERROR:", e)

    return "ok", 200
