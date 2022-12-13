def bot_error_stop(bot, message, bot_admin_id_telegram, e, db_budget):
    """Stop program execution when an error occurs"""
    # send an error message
    bot.send_message(
        message.chat.id,
        f"Извините! Произошла неожиданная ошибка, поэтому бот пока не работает!",
        parse_mode='html'
    )
    bot.send_message(
        bot_admin_id_telegram,
        f"Произошла ошибка! Бот остановлен!\n"
        f"Текст ошибки: {e}",
        parse_mode='html'
    )
    # stop the program
    bot.stop_polling()
    db_budget.close()
