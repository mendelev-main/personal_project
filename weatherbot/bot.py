import sqlalchemy.orm
import telebot
import requests
import config
from sqlalchemy import create_engine
import models

bot = telebot.TeleBot(config.BOT_TOKEN, parse_mode=None)
engine = create_engine(config.POSTGRES_URL, echo=True)
models.Base.metadata.create_all(bind=engine)


@bot.message_handler(commands=["start"])
def send_welcome(message):
    bot.reply_to(
        message,
        "Hi, I'm a bot 🤖\n"
        "I'll help you find out about the weather.\n"
        "More info -> [/help]",
    )


@bot.message_handler(commands=["help"])
def send_welcome(message):
    bot.reply_to(
        message,
        "📍I can help you find out the weather anywhere,\n"
        "just write the city\n \n"
        "✅You can subscribe to the weather \nforecast in your location,"
        "for this use the command [/pl your citi]",
    )


@bot.message_handler(commands=["pl"])
def send_welcome(message: telebot.types.Message) -> None:
    with sqlalchemy.orm.Session(bind=engine, expire_on_commit=False) as session:
        telegram_id = message.from_user.id
        user: models.User | None = (
            session.query(models.User)
            .filter(models.User.telegram_id == telegram_id)
            .first()
        )
        if user is None:
            user = models.User(
                username=message.from_user.username,
                telegram_id=message.from_user.id,
                first_name=message.from_user.first_name,
                preferred_location=message.text.split()[1].capitalize(),
            )
            session.add(user)
            session.commit()
            session.refresh(user)

    bot.reply_to(
        message,
        f"Hi {user.first_name}."
        f"I remembered your location for the daily\nforecast {message.text.split()[1].capitalize()}",
    )


@bot.message_handler(func=lambda location: True)
def get_weather(location):
    response = requests.get(
        f"https://api.openweathermap.org/data/2.5/weather?q={location.text}&lang=eng&appid={config.API_KEY}"
    )
    print(f"{location.text},{response.status_code=}")
    data = response.json()
    name = data["name"]
    temp = data["main"]["temp"] - 273.15
    wind = data["wind"]["speed"]
    description = data["weather"][0]["description"]

    bot.reply_to(
        location,
        f"Now in {name} {description} "
        f"{temp:.0f} degrees. Wind speed {wind:.0f} m/s",
    )
