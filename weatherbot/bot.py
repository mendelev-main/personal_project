import requests
import sqlalchemy.orm
import telebot
from sqlalchemy import create_engine

from weatherbot import config, models


bot = telebot.TeleBot(config.BOT_TOKEN, parse_mode=None)
engine = create_engine(config.POSTGRES_URL, echo=True)
models.Base.metadata.create_all(bind=engine)


@bot.message_handler(commands=["start"])
def send_welcome(message):
    bot.reply_to(
        message,
        "Привет, я БОТ 🤖\n"
        "Я помогу тебе узнать о погоде.\n"
        "Больше информации -> [/help]",
    )


@bot.message_handler(commands=["help"])
def send_help(message):
    bot.reply_to(
        message,
        "📍Если хочешь узнать о погоде просто напиши локацию в чат\n"
        "✅Если хочешь получать ежедневный прогноз нажми сюда -> [/your_location]",
    )


@bot.message_handler(commands=["your_location"])
def add_preferred_location(message: telebot.types.Message) -> None:
    bot.reply_to(message, 'По какой локации ты хочешь получать прогноз?')
    bot.register_next_step_handler_by_chat_id(chat_id=message.chat.id, callback=add_db)


def add_db(message: telebot.types.Message) -> None:
    location = message.text
    response = requests.get(
        f"https://api.openweathermap.org/data/2.5/weather?q={location}&lang=eng&appid={config.API_KEY}"
    )
    if response.status_code == 200:
        with sqlalchemy.orm.Session(bind=engine) as session:
            user = (
                session.query(models.User)
                .filter(models.User.telegram_id == message.chat.id)
                .first()
            )
            if user is None:
                user = models.User(
                    telegram_id=message.from_user.id,
                    username=message.from_user.username,
                    first_name=message.from_user.first_name,
                    preferred_location=location,
                )
            else:
                user.preferred_location = location
            session.add(user)
            session.commit()
            session.refresh(user)

        bot.reply_to(message, f"Ок, теперь твоя токация {location}")
    else:
        bot.reply_to(message, 'Не нашел такую локацию (')


@bot.message_handler(func=lambda location: True)
def get_weather(location):
    response = requests.get(
        f"https://api.openweathermap.org/data/2.5/weather?q={location.text}&lang=ru&appid={config.API_KEY}"
    )
    print(f"{location.text},{response.status_code=}")
    data = response.json()
    name = data["name"]
    temp = data["main"]["temp"] - 273.15
    wind = data["wind"]["speed"]
    description = data["weather"][0]["description"]

    bot.reply_to(
        location,
        f"{name} -> {description} "
        f"{temp:.0f} градусов, Скорость ветра {wind:.0f} м/с",
    )
