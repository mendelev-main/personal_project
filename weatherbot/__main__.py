import typer


cla = typer.Typer()


@cla.command()
def bot():
    from weatherbot.bot import bot

    bot.infinity_polling()
    print("launch bot")


@cla.command()
def notify():
    from weatherbot.notify import main

    main()
    print("launch notify")


cla()
