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
        'en': "The following commands are currently available:\n\n"
              "\t<b>/help</b> - a list of all commands and their description\n"
              "\t<b>/settings</b> - a list of available settings for the bot",
        'ru': "В данный момент доступны такие команды:\n\n"
              "\t<b>/help</b> - список всех команд и их описание\n"
              "\t<b>/settings</b> - список доступных настроек для бота"
    },
    'not_updated_user': {
        'en': "Hello! We have updated the structure of our bot, and your account has been successfully updated. Don't"
              " worry, you can continue using the bot as usual.",
        'ru': "Здравствуйте! Мы обновили структуру нашего бота, и ваш аккаунт был успешно обновлен. Не беспокойтесь, вы"
              " можете продолжать пользоваться ботом как обычно."
    },
    '/settings': {
        'en': "While the following settings are available in the bot:\n\n"
              "\t<b>/change_lang</b> - change the language of the bot",
        'ru': "Пока в боте доступны такие настройки:\n\n"
              "\t<b>/change_lang</b> - изменить язык бота"
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
