import telebot
import requests

bot = telebot.TeleBot("5998702901:AAFGOpuvytYEWFKbU6I5TydhQwLnAbXS43o", parse_mode=None)
api_key = "595edbf624f93725e127cde22f92b67e"


@bot.message_handler(commands=["start", "help"])
def send_welcome(message):
    bot.reply_to(message, "Howdy, how are you doing?")


@bot.message_handler(func=lambda massage: True)
def get_weather(message):
    print("Done")
    response = requests.get(
        f"https://api.openweathermap.org/data/2.5/weather?q={message.text}&lang=eng&appid={api_key}"
    )
    data = response.json()
    name = data["name"]
    temp = data["main"]["temp"] - 273.15
    wind = data["wind"]["speed"]
    description = data["weather"][0]["description"]

    bot.reply_to(
        message,
        f"Now in {name} {description} {temp:.0f} degrees. Wind speed {wind:.0f} m/s",
    )


bot.infinity_polling()
