class CommandsNames:
    settings = 'settings'
    change_language = 'change_language'
    create_new_module = 'new_module'
    saved_modules = 'saved_modules'
    cancel = 'cancel'
    change_words_in_block = 'change_words_in_block'
    change_repetitions_for_block = 'change_repetitions_for_block',
    get_module_by_id = 'get_module_by_id'


LEXICON: dict[str, dict[str, str]] = {
    # Base Commands
    '/start': {
        'en': "Hello! I'm RepeatRemindBot. I'm here to help you with repetition and reminders. What can I do for"
              " you today? /help",
        'ru': "Здравствуйте! Я RepeatRemindBot. Я готов помочь вам с повторениями и напоминаниями. Чем могу"
              " помочь вам сегодня? /help"
    },
    '/help': {
        'en': "The following commands are currently available:\n\n"
              "\t<b>/help</b> - Shows a list of all commands and their description\n"
              f"\t<b>/{CommandsNames.settings}</b> - Displays a list of available settings for the bot\n"
              f"\t<b>/{CommandsNames.create_new_module}</b> - Allows you to create a module for further study\n"
              f"\t<b>/{CommandsNames.saved_modules}</b> - Saved modules",
        'ru': "В данный момент доступны следующие команды:\n\n"
              "\t<b>/help</b> - Показывает список всех команд и их описание\n"
              f"\t<b>/{CommandsNames.settings}</b> - Показывает список доступных настроек для бота\n"
              f"\t<b>/{CommandsNames.create_new_module}</b> - Позволяет создать модуль для дальнейшего изучения\n"
              f"\t<b>/{CommandsNames.saved_modules}</b> - Сохраненные модули\n"
    },
    CommandsNames.settings: {
        'en': "You can adjust the following settings in the bot:\n\n"
              f"\t<b>/{CommandsNames.change_language}</b> - Change the language of the bot\n"
              f"\t<b>/{CommandsNames.change_words_in_block}</b> - Change the number of words per block"
              " (currently set to {words_in_block_number})\n"
              f"\t<b>/{CommandsNames.change_repetitions_for_block}</b> - Change the number of repetitions"
              " per block (currently set to {repetitions_for_block_number})"
              "\n\n/help",
        'ru': "Вы можете настроить следующие параметры в боте:\n\n"
              f"\t<b>/{CommandsNames.change_language}</b> - Изменить язык бота\n"
              f"\t<b>/{CommandsNames.change_words_in_block}</b> - Изменить количество слов в блоке"
              " (сейчас установлено {words_in_block_number})\n"
              f"\t<b>/{CommandsNames.change_repetitions_for_block}</b> - Изменить количество повторений"
              " в блоке (сейчас установлено {repetitions_for_block_number})"
              "\n\n/help"
    },
    CommandsNames.create_new_module: {
        'en': "Please enter the name of the module."
              "\nThe module name should be between 5 and 20 characters long."
              "\n\nThe module can include only the following characters:"
              "\n - Latin letters (either uppercase or lowercase)."
              "\n - Numbers."
              "\n - The underscore character '_'."
              "\n\nEnsure the module name meets these requirements before entering."
              f"\n\n/{CommandsNames.cancel} - To cancel module creation",
        'ru': "Пожалуйста, введите название модуля."
              "\nНазвание модуля должно быть длиной от 5 до 20 символов."
              "\n\nМодуль может содержать только следующие символы:"
              "\n - Латинские буквы (верхнего или нижнего регистра)."
              "\n - Цифры."
              "\n - Символ подчеркивания '_'."
              "\n\nПроверьте, что название модуля соответствует этим требованиям, прежде чем вводить его."
              f"\n\n/{CommandsNames.cancel} - Для отмены создания модуля"
    },

    # Other
    'not_updated_user': {
        'en': "Hello! We've updated the structure of our bot, and your account has been updated successfully. Don't"
              " worry, you can continue using the bot as usual. /help",
        'ru': "Здравствуйте! Мы обновили структуру нашего бота, и ваш аккаунт был успешно обновлен. Не беспокойтесь,"
              " вы можете продолжать использовать бота как обычно. /help"
    },
    'default_response': {
        'en': "Sorry, I didn't understand that. Please use one of the available commands or ask for help by"
              " sending /help.",
        'ru': "Извините, я не понял эту команду. Пожалуйста, используйте одну из доступных команд или попросите помощи,"
              " отправив /help."
    },
    'nothing_to_cancel': {
        'en': "Sorry, there's nothing to cancel at the moment as you're in the standard mode."
              " If you have any questions or requests, please let me know, and I'll be happy to assist."
              "\n/help",
        'ru': "Извините, отменить сейчас нечего, так как вы находитесь в стандартном режиме."
              " Если у вас есть вопросы или предложения, сообщите мне, и я с радостью помогу."
              "\n/help"
    },
}


SETTINGS_LEXICON: dict[str, dict[str, str]] = {
    CommandsNames.change_language: {
        'en': "Please choose your language:\n🇺🇸 English\n🇷🇺 Русский",
        'ru': "Пожалуйста, выберите язык:\n🇺🇸 English\n🇷🇺 Русский"
    },
    'language': {
        'en': "🇺🇸",
        'ru': "🇷🇺",
    },
    'changed_language': {
        'en': "You have successfully changed the language to English! 🇺🇸",
        'ru': "Вы успешно сменили язык на русский! 🇷🇺"
    },
    CommandsNames.change_words_in_block: {
        'en': "Enter the number of words per block that you find convenient to repeat (e.g., 10)."
              "\nThe number should be between 5 and 20.",
        'ru': "Введите количество слов в блоке, которое вам удобно повторять (например, 10)."
              "\nЧисло должно быть от 5 до 20."
    },
    CommandsNames.change_repetitions_for_block: {
        'en': "Enter the number of repetitions per block that you find convenient (e.g., 3)."
              "\nThe number should be between 1 and 10.",
        'ru': "Введите количество повторений на блок, которое вам удобно (например, 3)."
              "\nЧисло должно быть от 1 до 10."
    },
    'not_valid_words_in_block': {
        'en': "The number should be between 5 and 20.",
        'ru': "Число должно быть от 5 до 20."
    },
    'not_valid_repetitions_for_block': {
        'en': "The number should be between 1 and 10.",
        'ru': "Число должно быть от 1 до 10."
    },
    'sent_new_words_in_block': {
        'en': "The number of words per block has been successfully updated to {number} ✅",
        'ru': "Количество слов в блоке успешно обновлено до {number} ✅"
    },
    'sent_new_repetitions_for_block': {
        'en': "The number of repetitions per block has been successfully updated to {number} ✅",
        'ru': "Количество повторений за блок успешно обновлено до {number} ✅"
    }
}


CREATING_MODULE_LEXICON = {
    'not_valid_name': {
        'en': ("The module name must contain from 5 to 20 characters.\n\nModule can include only the "
               "following characters:\n - Latin letters (in any case).\n - Digits.\n - Character '_'.\n\nPlease make "
               "sure that the module name meets these conditions before entering.\n\n"
               f"/{CommandsNames.cancel} - to cancel the module creation"),
        'ru': ("Название модуля должно содержать от 5 до 20 символов.\n\nМодуль может включать только "
               "следующие символы:\n - Латинские буквы (в любом регистре).\n - Цифры.\n - Символ '_'.\n\nПожалуйста, "
               "убедитесь, что название модуля соответствует этим условиям перед вводом.\n\n"
               f"/{CommandsNames.cancel} - чтобы отменить создание модуля")
    },
    'rename_module_button': {
        'en': "Change the module name ✏️",
        'ru': "Изменить название модуля ✏️"
    },
    'fill_separator': {
        'en': ("Great! Now, please enter one character that will be a convenient separator for you. This character will"
               " be used to separate words in your module by adding spaces in the text.\n\n Please enter one character "
               "(for example, '/', '|', ',', etc.), which you want to use as a separator.\n\n Most often used for "
               f"example - = :\n\n/{CommandsNames.cancel} - to cancel the module creation"),
        'ru': ("Отлично! Теперь, пожалуйста, введите один символ, который будет удобным для вас разделителем. Этот "
               "символ будет использоваться для разделения слов в вашем модуле, добавляя пробелы в тексте.\n\n"
               "Пожалуйста, введите один символ (например, '/', '|', ',', и т. д.), который вы хотите использовать "
               "в качестве разделителя.\n\nЧаще всего используются например - = :\n\n"
               f"/{CommandsNames.cancel} - чтобы отменить создание модуля"),
    },
    'not_valid_separator': {
        'en': ("Please enter one character (for example, '/', '|', ',', etc.), which you want to use as a separator.\n"
               f"\n/{CommandsNames.cancel} - to cancel the module creation"),
        'ru': ("Пожалуйста, введите один символ (например, '/', '|', ',', и т. д.), который вы хотите использовать в "
               f"качестве разделителя.\n\n/{CommandsNames.cancel} - чтобы отменить создание модуля")
    },
    'edit_module_separator_button': {
        'en': "Change the separator✏️",
        'ru': "Изменить разделитель✏️"
    },
    'rename_new_module': {
        'en': ("<b>!!!Changing module name!!!</b>\n\nPlease enter the name of the new module.\nThe module name must "
               "contain from 5 to 20 characters.\n\nModule can include only the following characters:\n - Latin "
               "letters (in any case).\n - Digits.\n - Character '_'.\n\nPlease make sure that the new module name "
               f"meets these conditions before entering.\n\n/{CommandsNames.cancel} - to cancel the module creation"),
        'ru': ("<b>!!!Изменение названия модуля!!!</b>Пожалуйста, введите новое название модуля.\nНазвание модуля "
               "должно содержать от 5 до 20 символов.\n\nМодуль может включать только следующие символы:\n - Латинские "
               "буквы (в любом регистре).\n - Цифры.\n - Символ '_'.\n\nПожалуйста, убедитесь, что новое название "
               f"модуля соответствует этим условиям перед вводом.\n\n/{CommandsNames.cancel} - чтобы отменить создание "
               "модуля")
    },
    'edit_separator': {
        'en': ("<b>!!!Changing separator!!!</b>\n\nPlease enter one character that will be a new convenient separator "
               "for you. This character will be used to separate words in your module by adding spaces in the text.\n\n"
               " Please enter one character (for example, '/', '|', ',', etc.), which you want to use as a "
               "separator.\n\n Most often used for example - = :\n\n"
               f"/{CommandsNames.cancel} - to cancel the module "
               "creation"),
        'ru': ("<b>!!!Изменение разделителя!!!</b>\n\nПожалуйста, введите один символ, который будет удобным для вас "
               "разделителем. Этот символ будет использоваться для разделения слов в вашем модуле, добавляя пробелы в "
               "тексте.\n\nПожалуйста, введите один символ (например, '/', '|', ',', и т. д.), который вы хотите "
               "использовать в качестве разделителя.\n\nЧаще всего используются например - = :\n\n"
               f"/{CommandsNames.cancel} - чтобы отменить создание модуля")
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
        'en': ("Now enter pairs of values separated by your chosen delimiter:\nkey {separator} value \n\nYour pairs "
               "will be added to the message keyboard below this.\n\nYou can also send multiple pairs of values at once"
               ", each on the next line:\nkey1 {separator} value\nkey2 {separator} value\n\n"
               f"/{CommandsNames.cancel} - to cancel module creation"),
        'ru': ("Теперь вводите пары значений, разделенных выбранным вам разделителем:\nключ {разделитель} значение "
               "\n\nВаши пары будут добавляться в клавиатуру сообщения под этим.\n\nТакже вы можете сразу отправить "
               "несколько пар значений, каждая из которых на следующей строке:\nключ1 {разделитель} значение\nключ2 "
               "{разделитель} значение\n\n"
               f"/{CommandsNames.cancel} - чтобы отменить создание модуля")
    },
    'incorrect_pair': {
        'en': ("Incorrect format!\n\nExample:\nfruit {separator} apple\n\n/{CommandsNames.cancel} - to cancel module "
               "creation"),
        'ru': ("Неправильный формат!\n\nПример:\nфрукт {separator} яблоко\n\n/{CommandsNames.cancel} - чтобы отменить "
               "создание модуля")
    },
    'new_module_info': {
        'en': ("Module name - '{module_name}', separator - '{separator}'\n"
               "-----------------------------------------------------------------------------------------------------"),
        'ru': ("Название модуля - '{module_name}', разделитель - '{separator}'\n"
               "-----------------------------------------------------------------------------------------------------")
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
        'en': "You have exited the module creation mode. Now you can perform other actions.\n/help",
        'ru': "Вы вышли из режима создания модуля. Теперь вы можете выполнить другие действия.\n/help"
    },
    'unintended_creating_module': {
        'en': ("Your message is not provided by the bot in the current state.\n/{CommandsNames.cancel} - to cancel the "
               "module creation"),
        'ru': ("Ваше сообщение не предусмотренно ботом в текущем состоянии.\n/{CommandsNames.cancel} - чтобы отменить "
               "создание модуля")
    },
}


SAVED_MODULES_LEXICON: dict[str, dict[str, str]] = {
    'list_of_saved_modules': {
        'en': "Here are your saved modules:"
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
        'en': "It seems that this module does not exist.",
        'ru': "Кажется, этого модуля не существует."
    },
    'repeat_module': {
        'en': "Repeat module 🤓",
        'ru': "Повторить модуль 🤓"
    },
    'edit_saved_module': {
        'en': "Edit ✏️",
        'ru': "Изменить ✏️"
    },
    'delete_module': {
        'en': "Delete 🗑️",
        'ru': "Удалить 🗑️"
    },
    'back_to_saved_modules': {
        'en': "⬅️ Back to saved modules",
        'ru': "⬅️ Вернуться к сохраненным модулям"
    },
    'module_has_been_deleted': {
        'en': "The module {module_name} has been deleted 🗑️",
        'ru': "Модуль {module_name} был удалён 🗑️"
    },
    'edit_instruction': {
        'en': "Modify the module following the same rules used for its creation."
              "\nAfter saving, you will have an updated module.\n"
              "(the original will be preserved until you choose to delete it)",
        'ru': "Изменяйте модуль по тем же правилам, по которым вы его создавали."
              "\nПосле сохранения у вас появится измененный модуль.\n"
              "(старый также останется, потом вы сможете его удалить)"
    },
    'unintended_editing_module': {
        'en': "Your message does not correspond with any expected inputs in the current state of the bot."
              f"\n/{CommandsNames.cancel} - to cancel module editing",
        'ru': "Ваше сообщение не предусмотрено ботом в текущем состоянии."
              f"\n/{CommandsNames.cancel} - чтобы отменить редактирование модуля"
    },
}


REPEATING_MODULE_LEXICON: dict[str, dict[str, str]] = {
    'ask_to_repeating': {
        'en': "Great! Now you will review the module {module_name}!"
              "\n\nRepeat settings:\n"
              "\t<b>Number of blocks</b> - {blocks_num}\n"
              "\t<b>Words per block</b> - {words_in_block_num}\n"
              "\t<b>Repetitions per block</b> - {repetitions_num}"
              "\n\n<b>In /settings, you can change the number of blocks or repetitions.</b>"
              "\n\nHere's how the selected module has been divided into blocks:\n"
              "\n{content}\n"
              "/help",
        'ru': "Отлично! Сейчас вы будете повторять модуль {module_name}!"
              "\n\nНастройки повторения:\n"
              "\t<b>Количество блоков</b> - {blocks_num}\n"
              "\t<b>Слов в каждом блоке</b> - {words_in_block_num}\n"
              "\t<b>Количество повторений на каждый блок</b> - {repetitions_num}"
              "\n\n<b>В /settings вы можете изменить количество блоков или их повторений.</b>"
              "\n\nВот как был разделен на блоки выбранный вами модуль:\n"
              "\n{content}\n"
              "/help"
    },
    'confirm_repeating': {
        'en': "Start review ✅",
        'ru': "Начать повторять ✅"
    },
    'mix_words': {
        'en': "Shuffle words differently 🔄",
        'ru': "Перемешать по-другому 🔄"
    },
    'words_were_mixed': {
        'en': "The words have been shuffled 🔄",
        'ru': "Слова были перемешаны 🔄"
    },
    'repeating_module_header': {
        'en': "You are currently reviewing the module {module_name}.\n"
              "Block - {cur_block}/{blocks}\n"
              "Repetitions completed for this block - {current_repetitions}/{repetitions}"
              f"\n\n//{CommandsNames.cancel} - to stop the review",
        'ru': "Сейчас вы повторяете модуль {module_name}.\n"
              "Блок - {cur_block}/{blocks}\n"
              "Завершенных повторений для этого блока - {current_repetitions}/{repetitions}"
              f"\n\n/{CommandsNames.cancel} - чтобы остановить повторение модуля"
    },
    'cancel_repeating_module': {
        'en': "The review has been canceled.\n"
              "\n/help",
        'ru': "Повторение было отменено.\n"
              "\n/help"
    },
    'next_question': {
        'en': "Next question ➡️",
        'ru': "Следующий вопрос ➡️"
    },
    'answer_was_correct': {
        'en': "The answer was correct 😤",
        'ru': "Ответ был верный 😤"
    },
    'incorrect_answer': {
        'en': "❌ Incorrect answer!\nCorrect: {correct_answer}",
        'ru': "❌ Неверный ответ!\nПравильный: {correct_answer}"
    },
    'correct_answer': {
        'en': "✅ Nice! Correct, the answer is {correct_answer}!",
        'ru': "✅ Отлично! Верно, ответ — {correct_answer}!"
    },
    'answer_was_correct_pressed': {
        'en': "✅ Okay, {correct_answer}, is correct",
        'ru': "✅ Хорошо, {correct_answer}, это правильный ответ"
    },
    'finish_repetition': {
        'en': "You've finished this repetition block! 🎉\n"
              "Consider taking a 1-3 minute break before continuing.",
        'ru': "Вы закончили одно из повторений блока! 🎉\n"
              "Советуем вам отдохнуть 1-3 минуты перед продолжением."
    },
    'finish_block': {
        'en': "You've finished reviewing the entire block! 🎉🎉\n"
              "Consider taking a 1-3 minute break before starting the next block.",
        'ru': "Вы закончили повторять целый блок! 🎉🎉\n"
              "Советуем вам отдохнуть 1-3 минуты перед началом следующего блока!"
    },
    'repeating_all_module': {
        'en': "You've repeated all blocks! 🎉🎉🎉\n"
              "Consider taking a 1-3 minute break before the final review of the entire module.",
        'ru': "Вы повторили все блоки! 🎉🎉🎉\n"
              "Советуем вам отдохнуть 1-3 минуты перед финальным повторением всего модуля."
    },
    'repeating_all_module_header': {
        'en': "You are reviewing all elements of the module {module_name}.",
        'ru': "Сейчас вы повторяете все элементы модуля {module_name}."
    },
    'finish_all_repeating': {
        'en': "You have successfully finished reviewing the module! 🎉🎉🎉🎉\n"
              "\n/help",
        'ru': "Вы успешно повторили весь модуль! 🎉🎉🎉🎉\n"
              "\n/help"
    }
}


LEXICON_COMMANDS: dict[str, str] = {
    '/help': 'Description of available commands.',
    f'/{CommandsNames.settings}': 'Your settings.',
    f'/{CommandsNames.create_new_module}': 'Create a new module.',
    f'/{CommandsNames.saved_modules}': 'Your saved modules.',
    #f'/{CommandsNames.get_module_by_id}': 'Save a module by its ID.'
}
