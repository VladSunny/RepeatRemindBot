import enum
# COMMANDS_NAMES: dict[str, str] = {
#     'settings': '/settings',
#     'create_new_module': '/new_module',
#     'change language': '/change_language',
#     'help': '/help'
# }


class CommandsNames:
    settings = 'settings'
    change_language = 'change_language'


LEXICON: dict[str, dict[str, str]] = {
    '/start': {
        'en': "Hello! I'm a RepeatRemindBot. I am ready to help you with repetition and reminders. What can I do for"
              " you today? /help",
        'ru': "Здравствуйте! Я RepeatRemindBot. Готов помочь вам с повторением и напоминаниями. Чем могу быть полезен"
              " сегодня? /help"
    },
    '/help': {
        'en': "The following commands are currently available:\n\n"
              "\t<b>/help</b> - a list of all commands and their description\n"
              f"\t<b>/{CommandsNames.settings}</b> - a list of available settings for the bot",
        'ru': "В данный момент доступны такие команды:\n\n"
              "\t<b>/help</b> - список всех команд и их описание\n"
              f"\t<b>/{CommandsNames.settings}</b> - список доступных настроек для бота"
    },
    CommandsNames.settings: {
        'en': "While the following settings are available in the bot:\n\n"
              f"\t<b>/{CommandsNames.change_language}</b> - change the language of the bot"
              "\n/help",
        'ru': "Пока в боте доступны такие настройки:\n\n"
              f"\t<b>/{CommandsNames.change_language}</b> - изменить язык бота"
              "\n/help"
    },
    CommandsNames.change_language: {
        'en': "choose your language: /help",
        'ru': "выберете нужный вам язык: /help"
    },
    'not_updated_user': {
        'en': "Hello! We have updated the structure of our bot, and your account has been successfully updated. Don't"
              " worry, you can continue using the bot as usual. /help",
        'ru': "Здравствуйте! Мы обновили структуру нашего бота, и ваш аккаунт был успешно обновлен. Не беспокойтесь, вы"
              " можете продолжать пользоваться ботом как обычно. /help"
    },
    'language': {
        'en': "🇺🇸",
        'ru': "🇷🇺",
    },
    'changed_language': {
        'en': "you have successfully changed your language to English!",
        'ru': "вы успешно сменили язык на русский!"
    },
    'default_response': {
        'en': "Sorry, I don't understand this command. Please use one of the available commands or ask me for help by"
              " sending /help.",
        'ru': "Извините, я не понимаю эту команду. Пожалуйста, используйте одну из доступных команд или спросите у меня"
              " о помощи, отправив /help."
    },
}

LEXICON_COMMANDS: dict[str, str] = {
    '/help': 'description of available commands',
    '/settings': 'your settings',
    '/new_module': 'create new module'
}
