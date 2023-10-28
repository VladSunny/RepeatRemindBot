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
              f"\t<b>/{CommandsNames.settings}</b> - a list of available settings for the bot\n"
              f"\t<b>/{CommandsNames.create_new_module}</b> - allows you to create a module for further study.",
        'ru': "В данный момент доступны такие команды:\n\n"
              "\t<b>/help</b> - список всех команд и их описание.\n"
              f"\t<b>/{CommandsNames.settings}</b> - список доступных настроек для бота.\n"
              f"\t<b>/{CommandsNames.create_new_module}</b> - позволяет создать модуль для последующего изучения."
    },
    CommandsNames.settings: {
        'en': "While the following settings are available in the bot:\n\n"
              f"\t<b>/{CommandsNames.change_language}</b> - change the language of the bot"
              "\n\n/help",
        'ru': "Пока в боте доступны такие настройки:\n\n"
              f"\t<b>/{CommandsNames.change_language}</b> - изменить язык бота"
              "\n\n/help"
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

SETTINGS_LEXICON: dict[str, dict[str, str]] = {
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
}

CREATING_MODULE_LEXICON: dict[str, dict[str, str]] = {
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
    'not_valid_name': {
        'en': "The module name must contain from 5 to 20 characters."
              "\n\nModule can include only the following characters: "
              "\n - Latin letters (in any case)."
              "\n - Digits."
              "\n - Character '_'."
              "\n\nPlease make sure that the module name meets these conditions before entering."
              f"\n\n/{CommandsNames.cancel} - to cancel the module creation",
        'ru': "Название модуля должно содержать от 5 до 20 символов."
              "\n\nМодуль может включать только следующие символы:"
              "\n - Латинские буквы (в любом регистре)."
              "\n - Цифры."
              "\n - Символ '_'."
              "\n\nПожалуйста, убедитесь, что название модуля соответствует этим условиям перед вводом."
              f"\n\n/{CommandsNames.cancel} - чтобы отменить создание модуля"
    },
    'rename_module_button': {
        'en': "Change the module name ✏️",
        'ru': "Изменить название модуля ✏️"
    },
    'fill_separator': {
        'en': "Great! Now, please enter one character that will be a convenient separator for you."
              " This character will be used to separate words in your module by adding spaces in the text."
              "\n\n Please enter one character (for example, '/', '|', ',', etc.),"
              " which you want to use as a separator."
              "\n\n Most often used for example - = :"
              f"\n\n/{CommandsNames.cancel} - to cancel the module creation",
        'ru': "Отлично! Теперь, пожалуйста, введите один символ, который будет удобным для вас разделителем."
              " Этот символ будет использоваться для разделения слов в вашем модуле, добавляя пробелы в тексте."
              "\n\nПожалуйста, введите один символ (например, '/', '|', ',', и т. д.),"
              " который вы хотите использовать в качестве разделителя."
              "\n\nЧаще всего используются например - = :"
              f"\n\n/{CommandsNames.cancel} - чтобы отменить создание модуля",
    },
    'not_valid_separator': {
        'en': "Please enter one character (for example, '/', '|', ',', etc.),"
              " which you want to use as a separator."
              f"\n\n/{CommandsNames.cancel} - to cancel the module creation",
        'ru': "\n\nПожалуйста, введите один символ (например, '/', '|', ',', и т. д.),"
              " который вы хотите использовать в качестве разделителя."
              f"\n\n/{CommandsNames.cancel} - чтобы отменить создание модуля"
    },
    'edit_module_separator_button': {
        'en': "Change the separator✏️",
        'ru': "Изменить разделитель✏️"
    },
    'rename_new_module': {
        'en': "<b>!!!Changing module name!!!</b>\n\n"
              "Please enter the name of the new module."
              "\nThe module name must contain from 5 to 20 characters."
              "\n\nModule can include only the following characters: "
              "\n - Latin letters (in any case)."
              "\n - Digits."
              "\n - Character '_'."
              "\n\nPlease make sure that the new module name meets these conditions before entering."
              f"\n\n/{CommandsNames.cancel} - to cancel the module creation",
        'ru': "<b>!!!Изменение названия модуля!!!</b>"
              "Пожалуйста, введите новое название модуля."
              "\nНазвание модуля должно содержать от 5 до 20 символов."
              "\n\nМодуль может включать только следующие символы:"
              "\n - Латинские буквы (в любом регистре)."
              "\n - Цифры."
              "\n - Символ '_'."
              "\n\nПожалуйста, убедитесь, что новое название модуля соответствует этим условиям перед вводом."
              f"\n\n/{CommandsNames.cancel} - чтобы отменить создание модуля"
    },
    'edit_separator': {
        'en': "<b>!!!Changing separator!!!</b>\n\n"
              "Please enter one character that will be a new convenient separator for you."
              " This character will be used to separate words in your module by adding spaces in the text."
              "\n\n Please enter one character (for example, '/', '|', ',', etc.),"
              " which you want to use as a separator."
              "\n\n Most often used for example - = :"
              f"\n\n/{CommandsNames.cancel} - to cancel the module creation",
        'ru': "<b>!!!Изменение разделителя!!!</b>\n\n"
              "Пожалуйста, введите один символ, который будет удобным для вас разделителем."
              " Этот символ будет использоваться для разделения слов в вашем модуле, добавляя пробелы в тексте."
              "\n\nПожалуйста, введите один символ (например, '/', '|', ',', и т. д.),"
              " который вы хотите использовать в качестве разделителя."
              "\n\nЧаще всего используются например - = :"
              f"\n\n/{CommandsNames.cancel} - чтобы отменить создание модуля"
    },
    'new_module_was_renamed': {
      'en': "Module successfully renamed!",
      'ru': "Изменение имени прошло успешно!"
    },
    'seperator_was_changed': {
        'en': "Separator successfully changed!",
        'ru': "Разделитель успешно изменён!"
    },
    'fill_content': {
        'en': "Now enter pairs of values separated by your chosen delimiter:"
              "\nkey {separator} value \n"
              "\nYour pairs will be added to the message keyboard below this."
              "\n\nYou can also send multiple pairs of values at once, each on the next line:"
              "\nkey1 {separator} value"
              "\nkey2 {separator} value"
              f"\n\n/{CommandsNames.cancel} - to cancel module creation",
        'ru': "Теперь вводите пары значений, разделенных выбранным вам разделителем:"
              "\nключ {разделитель} значение \n"
              "\nВаши пары будут добавляться в клавиатуру сообщения под этим."
              "\n\nТакже вы можете сразу отправить несколько пар значений, каждая из которых на следующей строке:"
              "\nключ1 {разделитель} значение"
              "\nключ2 {разделитель} значение"
              f"\n\n/{CommandsNames.cancel} - чтобы отменить создание модуля"
    },
    'incorrect_pair': {
        'en': "Incorrect format!"
              "\n\nExample:"
              "\nfruit {separator} apple"
              f"\n\n/{CommandsNames.cancel} - to cancel module creation",
        'ru': "Неправильный формат!"
              "\n\nПример:"
              "\nфрукт {separator} яблоко"
              f"\n\n/{CommandsNames.cancel} - чтобы отменить создание модуля"
    },
    'new_module_info': {
        'en': "Module name - '{module_name}', separator - '{separator}'"
              "\n-----------------------------------------------------------------------------------------------------",
        'ru': "Название модуля - '{module_name}', разделитель - '{separator}'"
              "\n-----------------------------------------------------------------------------------------------------"
    },
    'deleted_pair_from_new_model': {
        'en': "pair {deleted_pair} was deleted",
        'ru': "пара {deleted_pair} была удалена"
    },
    'finish_module_button': {
        'en': "Save ✅",
        'ru': "Сохранить ✅"
    },
    'module_saved': {
        'en': "You successfully saved module!",
        'ru': "Вы успешно сохранили модуль!"
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
        'ru': "Ваше сообщение не предусмотренно ботом в текущем состоянии."
              f"\n/{CommandsNames.cancel} - чтобы отменить создание модуля"
    },
}

LEXICON_COMMANDS: dict[str, str] = {
    '/help': 'description of available commands',
    f'/{CommandsNames.settings}': 'your settings',
    f'/{CommandsNames.create_new_module}': 'create new module',
}
