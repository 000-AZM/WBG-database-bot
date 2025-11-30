import telebot
import json

TOKEN = "8505220046:AAE7hfD9aKU7drBVuQZHUIiZZAAuaJV5LMM"
bot = telebot.TeleBot(TOKEN)

# Load JSON database
with open("data.json", "r", encoding="utf-8") as f:
    site_data = json.load(f)

# Command handlers
@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(message.chat.id, "👋 Welcome! Send a SiteID (like BGO0001) to get info.")

@bot.message_handler(commands=["help"])
def help(message):
    bot.send_message(message.chat.id, "Send a SiteID to get site information.\nExample: BGO0001")

# SiteID handler
@bot.message_handler(func=lambda m: True)
def handle_site_id(message):
    code = message.text.strip().upper()
    # Search for matching site
    site = next((s for s in site_data if s["SiteID"].upper() == code), None)
    
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
        bot.send_message(message.chat.id, reply)
    else:
        bot.send_message(message.chat.id, "❌ SiteID not found. Please try again.")
