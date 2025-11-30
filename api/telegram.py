
from flask import Flask, request
import telebot
from bot import bot

app = Flask(__name__)

@app.route("/telegram", methods=["POST"])
def webhook():
    if request.is_json:
        update = request.json
        bot.process_new_updates([telebot.types.Update.de_json(update)])
    return "ok", 200
