class CommandsNames:
    settings = 'settings'
    change_language = 'change_language'
    create_new_module = 'new_module'
    saved_modules = 'saved_modules'
    cancel = 'cancel'
    change_words_in_block = 'change_words_in_block'
    change_repetitions_for_block = 'change_repetitions_for_block'


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
              f"\t<b>/{CommandsNames.create_new_module}</b> - allows you to create a module for further study.\n"
              f"\t<b>/{CommandsNames.saved_modules}</b> - saved modules.",
        'ru': "В данный момент доступны такие команды:\n\n"
              "\t<b>/help</b> - список всех команд и их описание.\n"
              f"\t<b>/{CommandsNames.settings}</b> - список доступных настроек для бота.\n"
              f"\t<b>/{CommandsNames.create_new_module}</b> - позволяет создать модуль для последующего изучения.\n"
              f"\t<b>/{CommandsNames.saved_modules}</b> - сохраненные модули"
    },
    CommandsNames.settings: {
        'en': "While the following settings are available in the bot:\n\n"
              f"\t<b>/{CommandsNames.change_language}</b> - change the language of the bot\n"
              f"\t<b>/{CommandsNames.change_words_in_block}</b> - change the number of repeated words in the block"
              " (now its {words_in_block_number})\n"
              f"\t<b>/{CommandsNames.change_repetitions_for_block}</b> - change the number of repetitions"
              " in the repeated block (now its {repetitions_for_block_number})"
              "\n\n/help",
        'ru': "Пока в боте доступны такие настройки:\n\n"
              f"\t<b>/{CommandsNames.change_language}</b> - изменить язык бота\n"
              f"\t<b>/{CommandsNames.change_words_in_block}</b> - поменять количество повторяемых"
              " слов в блоке (сейчас их {words_in_block_number})\n"
              f"\t<b>/{CommandsNames.change_repetitions_for_block}</b> - поменять количество повторений"
              " в повторяемом блоке (сейчас их {repetitions_for_block_number})"
              "\n\n/help"
    },
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
    CommandsNames.change_words_in_block: {
        'en': "Enter the number of words that will be convenient for you to repeat in one block."
              "\nThe number should be from 5 to 20",
        'ru': "Введите число слов, которое вам будет удобно повторять в одном блоке."
              "\nЧисло должно быть от 5 до 20"
    },
    CommandsNames.change_repetitions_for_block: {
        'en': "Enter the number of repetitions for each block of words"
              " that will be convenient for you to repeat the block."
              "\nThe nuber should be from 1 to 10",
        'ru': "Введите число повторений для каждого блока, которое вам будет удобно для повторения блока."
              "\nЧисло должно быть от 1 до 10"
    },
    'not_valid_words_in_block': {
        'en': "The number should be from 5 to 20",
        'ru': "Число должно быть от 5 до 20"
    },
    'not_valid_repetitions_for_block': {
        'en': "The number should be from 1 to 10",
        'ru': "Число должно быть от 1 до 10"
    },
    'sent_new_words_in_block': {
        'en': "The number of words that will be convenient for you to repeat in one block was"
              " successfully updated to {number} ✅",
        'ru': "Число слов, которое вам будет удобно повторять в одном блоке, было успешно обновлено на {number} ✅"
    },
    'sent_new_repetitions_for_block': {
        'en': "The number of repetitions of each block"
              " that will be convenient for you to repeat the block was successfully updated to {number} ✅",
        'ru': "Число повторений для каждого модуля,"
              " которое вам будет удобно для повторения, было успешно обновлено на {number} ✅"
    }
}

CREATING_MODULE_LEXICON: dict[str, dict[str, str]] = {
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
        'en': "You successfully saved module {module_name}! It has ID: {module_id}",
        'ru': "Вы успешно сохранили модуль {module_name}! Его ID: {module_id}"
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

SAVED_MODULES_LEXICON: dict[str, dict[str, str]] = {
    'list_of_saved_modules': {
        'en': "Here is your saved modules:"
              "\n\n/help",
        'ru': "Вот ваши сохраненные модули:"
              "\n\n/help"
    },
    'module_info': {
        'en': "Name: {name}\n"
              "ID: {id}\n"
              "Separator: {separator}\n"
              "Number of elements: {number_of_elements}\n"
              "\nElements:\n{elements}",
        'ru': "Название: {name}\n"
              "ID: {id}\n"
              "Разделитель: {separator}\n"
              "Количество элементов: {number_of_elements}\n"
              "\nЭлементы:\n{elements}"
    },
    'module_not_found': {
        'en': "It seems that this module does not exist",
        'ru': "Кажется этого модуля не существует"
    },
    'repeat_module': {
        'en': "Repeat module 🤓",
        'ru': "Повторить модуль 🤓"
    },
    'edit_saved_module': {
        'en': "Edit ✏",
        'ru': "Изменить ✏"
    },
    'delete_module': {
        'en': "Delete 🗑",
        'ru': "Удалить 🗑"
    },
    'back_to_saved_modules': {
        'en': "⬅️Back to saved modules",
        'ru': "⬅️Вернуться к сохраненным модулям"
    },
    'module_has_been_deleted': {
        'en': "Module {module_name} has been deleted 🗑",
        'ru': "Модуль {module_name} был удалён 🗑"
    },
    'edit_instruction': {
        'en': "Modify the module according to the same rules as you created it."
              "\nAfter saving, you will have the modified module.\n"
              "(the old one will also remain, then you can delete it)",
        'ru': "Изменяйте модуль по тем же правилам, по которым вы его создавали."
              "\nПосле сохранения у вас появится измененный модуль.\n"
              "(старый тоже останется, потом вы сможете его удалить)"
    },
    'unintended_editing_module': {
        'en': "Your message is not provided by the bot in the current state."
              f"\n/{CommandsNames.cancel} - to cancel the module creation",
        'ru': "Ваше сообщение не предусмотренно ботом в текущем состоянии."
              f"\n/{CommandsNames.cancel} - чтобы отменить создание модуля"
    },
}

REPEATING_MODULE_LEXICON: dict[str, dict[str, str]] = {
    'ask_to_repeating': {
        'en': "Great! Now you will be reviewing the module {module_name}!"
              "\n\nThe words in the module will be divided into {blocks_num} blocks,"
              " each containing {words_in_block_num} words"
              " (in your module, there are {words_num} words)."
              "\nYou will repeat each block {repetitions_num} times.\n"
              "\n<b>In /settings, you can change the number of blocks or their repetitions.</b>"
              "\n\nHere's how the module you selected was divided into blocks:\n"
              "{content}\n"
              "/help",
        'ru': "Отлично! Сейчас вы будете повторять модуль {module_name}!"
              "\n\nСлова в модуле будут разделены на {blocks_num} блоков по {words_in_block_num} слов"
              " (в вашем модуле {words_num} слов)."
              "\nКаждый блок вы будете вы будете повторять {repetitions_num} раз.\n"
              "\n<b>В /settings вы можете изменить количество блоков или их повторений.</b>"
              "\n\nВот как был разделен на блоки выбранный вами модуль:\n"
              "\n{content}\n"
              "/help"
    },
    'confirm_repeating': {
        'en': "Start repeating ✅",
        'ru': "Начать повторять ✅"
    },
    'mix_words': {
        'en': "Shuffle differently 🔄",
        'ru': "Перемешать по-другому 🔄"
    },
    'words_were_mixed': {
        'en': "The words have been shuffled 🔄",
        'ru': "Слова были перемешаны 🔄"
    },
    'cancel_repeating_module': {
        # edit it
        'en': "Repeating was canceled.",
        'ru': "Повторение было отменено."
    }
}

LEXICON_COMMANDS: dict[str, str] = {
    '/help': 'description of available commands',
    f'/{CommandsNames.settings}': 'your settings',
    f'/{CommandsNames.create_new_module}': 'create new module',
    f'/{CommandsNames.saved_modules}': 'your saved modules'
}
