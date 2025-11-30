import telebot
import json
import os

# -----------------------------
# Telegram Bot Token
# -----------------------------
TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"
bot = telebot.TeleBot(TOKEN)  # synchronous, works in serverless

# -----------------------------
# Load JSON database (absolute path)
# -----------------------------
BASE_DIR = os.path.dirname(__file__)
DATA_PATH = os.path.join(BASE_DIR, "data.json")

with open(DATA_PATH, "r", encoding="utf-8") as f:
    site_data = json.load(f)

# -----------------------------
# Function to handle SiteID lookup
# -----------------------------
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
            f"Coordinates: {site['Lat']}, {site['Long']}"
        )
    else:
        reply = "❌ SiteID not found. Please try again."
    bot.send_message(chat_id, reply)
