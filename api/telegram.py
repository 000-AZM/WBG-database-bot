from flask import Flask, request
import json
import os
import requests
from datetime import datetime

# -----------------------------
# Telegram Bot Token
# -----------------------------
TOKEN = "8505220046:AAE7hfD9aKU7drBVuQZHUIiZZAAuaJV5LMM"
BASE_URL = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

# -----------------------------
# Google Sheet Webhook (Apps Script URL)
# -----------------------------
GOOGLE_SHEET_WEBHOOK = "https://script.google.com/macros/s/AKfycbzmKuH0QLyMuAK-EyiXk6uQNw4w1jnF5SAIOaJfoA9gmkSYk9Ot338SUHI5nB3HynYPPQ/exec"

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
    try:
        requests.post(BASE_URL, json=payload)
    except Exception as e:
        print("Error sending message:", e)

def handle_site_code(chat_id, code):
    site = next((s for s in site_data if s["SiteID"].upper() == code.upper()), None)
    if site:
        reply = (
            f"📌 SiteID: {site['SiteID']}\n"
            f"Branch: {site['Branch']}\n"
            f"Township: {site['Township']}\n"
            f"Site Type: {site['Site Type']}\n"
            f"Owner: {site['Owner']}\n"
            f"Power Status: {site['Power Status']}\n"
            f"DG NR: {site['DG NR']}\n"
            f"Manager: {site['Manager']}\n"
            f"Team: {site['Team']}\n"
            f"Coordinates: {site['Lat']}, {site['Long']}\n"
            f"Site Status: {site['Site Status']}\n\n"
            f"WBG database bot by Alua (https://t.me/aluaxeliana)"
        )
    else:
        reply = "❌ SiteID not found. Please try again."
    send_message(chat_id, reply)

def log_user_to_sheet(message):
    chat_id = message["chat"]["id"]
    user = message.get("from", {})
    username = user.get("username", "")
    first_name = user.get("first_name", "")
    last_name = user.get("last_name", "")
    time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    payload = {
        "chat_id": chat_id,
        "username": username,
        "first_name": first_name,
        "last_name": last_name,
        "time": time
    }
    try:
        requests.post(GOOGLE_SHEET_WEBHOOK, data=payload)
    except Exception as e:
        print("Error logging user:", e)

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
            # Log user to Google Sheet
            log_user_to_sheet(message)

            chat_id = message["chat"]["id"]
            text = message.get("text", "").strip()

            if text.lower().startswith("/start"):
                send_message(chat_id, "👋 Welcome! Send a SiteID (like BGO0001) to get info.")
            elif text.lower().startswith("/help"):
                send_message(chat_id, "Send a SiteID to get site information.\nExample: BGO0001")
            elif text.lower().startswith("/stats"):
                # Optional: show number of users (fetch from Google Sheet)
                send_message(chat_id, "📊 Check your Google Sheet for total users.")
            else:
                handle_site_code(chat_id, text)

    except Exception as e:
        print("ERROR:", e)

    return "ok", 200
