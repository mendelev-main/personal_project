import typer


cla = typer.Typer()


@cla.command()
def bot():
    from weatherbot.bot import bot

    bot.infinity_polling()
    print("launch bot")


@cla.command()
def notify():
    print('launch notify')


cla()
