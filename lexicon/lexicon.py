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
    }
}

LEXICON_COMMANDS: dict[str, str] = {
    '/help': 'list of available commands',
}
