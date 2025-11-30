from flask import Flask, request
import telebot
from bot import bot, handle_site_code

app = Flask(__name__)

@app.route("/telegram", methods=["POST"])
def webhook():
    if request.is_json:
        update = request.json
        message = update.get("message")
        if message:
            chat_id = message["chat"]["id"]
            text = message.get("text", "").strip().upper()
            if text.startswith("/START"):
                bot.send_message(chat_id, "👋 Welcome! Send a SiteID (like BGO0001) to get info.")
            elif text.startswith("/HELP"):
                bot.send_message(chat_id, "Send a SiteID to get site information.\nExample: BGO0001")
            else:
                handle_site_code(chat_id, text)
    return "ok", 200
