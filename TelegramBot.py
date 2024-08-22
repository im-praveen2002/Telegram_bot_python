from flask import Flask
import telebot
import requests

# Initialize Flask app
app = Flask(__name__)

# Your existing bot code
BOT_TOKEN = "7394994583:AAFA_vXDZA19BtRSYNuEzSXFbXoecKRIVLs"
bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start', 'hello'])
def send_welcome(message):
    bot.reply_to(message, "Howdy, how are you doing?")

@bot.message_handler(commands=['command1'])
def command1(message):
    bot.reply_to(message, "WELCOME TO PRAVEEN's BOT!!!")

def get_daily_horoscope(sign: str, day: str) -> dict:
    url = "https://horoscope-app-api.vercel.app/api/v1/get-horoscope/daily"
    params = {"sign": sign, "day": day}
    response = requests.get(url, params=params)
    return response.json()

@bot.message_handler(commands=['Local'])
def send_welcome(message):
    url = "https://localhost:7081/api/Test/public"
    response = requests.get(url)
    value = response.json()
    response_text = value["result"]
    bot.reply_to(message, response_text)

@bot.message_handler(commands=['horoscope'])
def sign_handler(message):
    text = "What's your zodiac sign?\nChoose one: Aries, Taurus, Gemini, Cancer, Leo, Virgo, Libra, Scorpio, Sagittarius, Capricorn, Aquarius, and *Pisces*."
    sent_msg = bot.send_message(message.chat.id, text, parse_mode="Markdown")
    bot.register_next_step_handler(sent_msg, day_handler)

def day_handler(message):
    sign = message.text
    text = "What day do you want to know?\nChoose one: TODAY, TOMORROW, YESTERDAY, or a date in format YYYY-MM-DD."
    sent_msg = bot.send_message(message.chat.id, text, parse_mode="Markdown")
    bot.register_next_step_handler(sent_msg, fetch_horoscope, sign.capitalize())

def fetch_horoscope(message, sign):
    day = message.text
    horoscope = get_daily_horoscope(sign, day)
    data = horoscope["data"]
    horoscope_message = f'*Horoscope:* {data["horoscope_data"]}\n*Sign:* {sign}\n*Day:* {data["date"]}'
    bot.send_message(message.chat.id, "Here's your horoscope!")
    bot.send_message(message.chat.id, horoscope_message, parse_mode="Markdown")

@bot.message_handler(func=lambda msg: True)
def echo_all(message):
    bot.reply_to(message, message.text)


# Flask route
@app.route('/')
def index():
    return "Flask app with Telegram bot is running!"

if __name__ == "__main__":
    # Start bot thread
    # bot.infinity_polling()
    # Start Flask app
    bot.infinity_polling()
    app.run(debug=True)

