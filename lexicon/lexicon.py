LEXICON: dict[str, dict[str, str]] = {
    'default_response': {
        'en': "Sorry, I don't understand this command. Please use one of the available commands or ask me for help by"
              " sending /help.",
        'ru': "Извините, я не понимаю эту команду. Пожалуйста, используйте одну из доступных команд или спросите у меня"
              " о помощи, отправив /help."
    },
    '/start': {
        'en': "Hello! I'm a RepeatRemindBot. I am ready to help you with repetition and reminders. What can I do for"
              " you today?",
        'ru': "Здравствуйте! Я RepeatRemindBot. Готов помочь вам с повторением и напоминаниями. Чем могу быть полезен"
              " сегодня?"
    },
    '/help': {
        'en': "Commands",
        'ru': "Команды"
    },
    'not_updated_user': {
        'en': "Hello! We have updated the structure of our bot, and your account has been successfully updated. Don't"
              " worry, you can continue using the bot as usual.",
        'ru': "Здравствуйте! Мы обновили структуру нашего бота, и ваш аккаунт был успешно обновлен. Не беспокойтесь, вы"
              " можете продолжать пользоваться ботом как обычно."
    },
    '/settings': {
        'en': '''/change_lang - change bot language''',
        'ru': '''/change_lang - изменить язык бота'''
    },
    '/change_lang': {
        'en': "choose your language:",
        'ru': "выберете нужный вам язык:"
    },
    'language': {
        'en': "🇺🇸",
        'ru': "🇷🇺",
    },
    'change_language': {
        'en': "you have successfully changed your language to English!",
        'ru': "вы успешно сменили язык на русский!"
    }
}

LEXICON_COMMANDS: dict[str, str] = {
    '/help': 'description of available commands',
    '/settings': 'your settings'
}
