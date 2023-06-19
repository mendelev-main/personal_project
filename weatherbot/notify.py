# Присылаем сводку погоды пользовотелям запросившим подписку

import time
from datetime import datetime, timedelta
import weatherbot
from weatherbot import bot
import models
import sqlalchemy
import sqlalchemy.orm


def main():
    while True:
        now = datetime.now()
        today_9 = datetime.today().replace(hour=9)
        wake_up_at = today_9 if today_9 > now else today_9 + timedelta(days=1)
        wake_up_at_ts = wake_up_at.timestamp()
        to_sleep = wake_up_at_ts - time.time()
        time.sleep(to_sleep)
        with sqlalchemy.orm.Session(bind=bot.engine) as session:
            users = (
                session.query(models.User)
                .filter(
                    models.User.preferred_location.is_(True),
                    models.User.preferred_location.is_not(None),
                )
                .all()
            )
        for user in users:
            weather = weatherbot.bot.get_weather(user.preferred_location)
            bot.bot.send_message(
                chat_id=user.telegram_id,
                text=f"hello weather today!\n"
                f"it's {weather.description} in {weather.name} "
                f"today {weather.temp:.0f} degrees "
                f"wind speed {weather.wind:.0f} m/s",
            )
