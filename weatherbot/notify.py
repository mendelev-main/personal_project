# # Присылаем сводку погоды пользовотелям запросившим подписку

import time
from datetime import datetime, timedelta

import sqlalchemy.orm

from weatherbot import bot, models


def main():
    while True:
        print('launch notify')
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
                    models.User.telegram_id.is_(True),
                    models.User.preferred_location.is_(True),
                )
                .all()
            )

            for user in users:
                weather = bot.get_weather(user.preferred_location)
                bot.bot.send_message(chat_id=user.telegram_id, text=f"{weather.temp}")
