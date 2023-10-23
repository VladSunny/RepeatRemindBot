class CommandsNames:
    settings = 'settings'
    change_language = 'change_language'
    create_new_module = 'new_module'
    cancel = "cancel"


LEXICON: dict[str, dict[str, str]] = {

    # Base Commands

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
              "\n\n/help",
        'ru': "Пока в боте доступны такие настройки:\n\n"
              f"\t<b>/{CommandsNames.change_language}</b> - изменить язык бота"
              "\n\n/help"
    },

    # - Settings
    # -- Change Language
    CommandsNames.change_language: {
        'en': "choose your language: /help",
        'ru': "выберете нужный вам язык: /help"
    },
    'language': {
        'en': "🇺🇸",
        'ru': "🇷🇺",
    },
    'changed_language': {
        'en': "you have successfully changed your language to English!",
        'ru': "вы успешно сменили язык на русский!"
    },

    # - Creating New Module

    CommandsNames.create_new_module: {
        'en': "Please enter the name of the module."
              "\nThe module name must contain from 5 to 20 characters."
              "\n\nModule can include only the following characters: "
              "\n - Latin letters (in any case)."
              "\n - Digits."
              "\n - Character '_'."
              "\n\nPlease make sure that the module name meets these conditions before entering."
              f"\n\n/{CommandsNames.cancel} - to cancel the module creation",
        'ru': "Пожалуйста, введите название модуля."
              "\nНазвание модуля должно содержать от 5 до 20 символов."
              "\n\nМодуль может включать только следующие символы:"
              "\n - Латинские буквы (в любом регистре)."
              "\n - Цифры."
              "\n - Символ '_'."
              "\n\nПожалуйста, убедитесь, что название модуля соответствует этим условиям перед вводом."
              f"\n\n/{CommandsNames.cancel} - чтобы отменить создание модуля"
    },
    'cancel_creating_module': {
        'en': "You have exited the module creation mode. Now you can perform other actions."
              "\n/help",
        'ru': "Вы вышли из режима создания модуля. Теперь вы можете выполнить другие действия."
              "\n/help"
    },
    'unintended_creating_module': {
        'en': "Your message is not provided by the bot in the current state."
              f"\n/{CommandsNames.cancel} - to cancel the module creation",
        'ru': "Ваше сообщение не предоставлено ботом в текущем состоянии."
              f"\n/{CommandsNames.cancel} - чтобы отменить создание модуля"
    },

    # Other
    'not_updated_user': {
        'en': "Hello! We have updated the structure of our bot, and your account has been successfully updated. Don't"
              " worry, you can continue using the bot as usual. /help",
        'ru': "Здравствуйте! Мы обновили структуру нашего бота, и ваш аккаунт был успешно обновлен. Не беспокойтесь, вы"
              " можете продолжать пользоваться ботом как обычно. /help"
    },
    'default_response': {
        'en': "Sorry, I don't understand this command. Please use one of the available commands or ask me for help by"
              " sending /help.",
        'ru': "Извините, я не понимаю эту команду. Пожалуйста, используйте одну из доступных команд или спросите у меня"
              " о помощи, отправив /help."
    },
    'nothing_to_cancel': {
        'en': "Sorry, the /cancel command doesn't make sense in this context, since you are in standard mode."
              " If you have any questions or requests, please clarify them and I will try to help you."
              "\n/help",
        'ru': "Извините, команда /cancel не имеет смысла в данном контексте,"
              " так как вы находитесь в стандартном режиме. Если у вас есть какие-либо вопросы или запросы, пожалуйста,"
              " уточните их, и я постараюсь вам помочь."
              "\n/help"
    },
}

LEXICON_COMMANDS: dict[str, str] = {
    '/help': 'description of available commands',
    f'/{CommandsNames.settings}': 'your settings',
    f'/{CommandsNames.create_new_module}': 'create new module'
}
