import telebot

TOKEN = "8505220046:AAE7hfD9aKU7drBVuQZHUIiZZAAuaJV5LMM"
bot = telebot.TeleBot(TOKEN, threaded=False)

@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(message.chat.id, "👋 Hello! Welcome to the bot.")

@bot.message_handler(commands=["help"])
def help(message):
    bot.send_message(message.chat.id, "📌 Available commands:\n/start\n/help\n/about")

@bot.message_handler(commands=["about"])
def about(message):
    bot.send_message(message.chat.id, "🤖 This bot is hosted on Vercel using webhook. I'm always online!")
