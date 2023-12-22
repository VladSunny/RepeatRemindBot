from config_data.user_restrictions import *
from config_data.donates_config import *


class CommandsNames:
    settings = 'settings'
    change_language = 'change_language'
    create_new_module = 'new_module'
    saved_modules = 'saved_modules'
    cancel = 'cancel'
    change_words_in_block = 'change_words_in_block'
    change_repetitions_for_block = 'change_repetitions_for_block'
    get_module_by_id = 'get_module_by_id'
    donate = 'donate'


LEXICON: dict[str, dict[str, str]] = {
    # Base Commands
    '/start': {
        'en': "Hello! I'm RepeatRemindBot, your assistant for learning and repetition. How can I assist you today?"
              "\nType /help for guidance.",
        'ru': "Привет! Я RepeatRemindBot, ваш помощник в изучении и запоминании. Чем могу помочь сегодня?"
              "\nНапишите /help, чтобы узнать больше."

    },
    '/help': {
        'en': "You can use these commands:\n"
              "\t<b>/help</b> - List of commands and explanations\n"
              f"\t<b>/{CommandsNames.settings}</b> - Configure bot settings\n"
              f"\t<b>/{CommandsNames.create_new_module}</b> - Create a module for study\n"
              f"\t<b>/{CommandsNames.saved_modules}</b> - Show your saved modules\n"
              f"\t<b>/{CommandsNames.get_module_by_id}</b> - Retrieve a module using its ID"
              f" (e.g., for student-teacher shared modules)\n"
              f"\t<b>/{CommandsNames.donate}</b> - Support the project",

        'ru': "Вы можете использовать эти команды:\n"
              "\t<b>/help</b> - Список команд и их описание\n"
              f"\t<b>/{CommandsNames.settings}</b> - Настройки бота\n"
              f"\t<b>/{CommandsNames.create_new_module}</b> - Создание модуля для изучения\n"
              f"\t<b>/{CommandsNames.saved_modules}</b> - Просмотр сохраненных модулей\n"
              f"\t<b>/{CommandsNames.get_module_by_id}</b> - Получение модуля по ID"
              f" (например, для общего использования с учителем)\n"
              f"\t<b>/{CommandsNames.donate}</b> - Поддержать проект"

    },
    CommandsNames.settings: {
        'en': "Configure bot settings:\n"
              f"\t<b>/{CommandsNames.change_language}</b> - Change bot language\n"
              f"\t<b>/{CommandsNames.change_words_in_block}</b> - Set number of items per block"
              " ({words_in_block_number})\n"
              f"\t<b>/{CommandsNames.change_repetitions_for_block}</b> - Set repetitions per block"
              " ({repetitions_for_block_number})\n"
              "\n/help for more commands.",

        'ru': "Настройки бота:\n"
              f"\t<b>/{CommandsNames.change_language}</b> - Сменить язык бота\n"
              f"\t<b>/{CommandsNames.change_words_in_block}</b> - Количество элементов в блоке"
              " (текущее: {words_in_block_number})\n"
              f"\t<b>/{CommandsNames.change_repetitions_for_block}</b> - Количество повторений блока"
              " (текущее: {repetitions_for_block_number})\n"
              "\n/help - список команд."

    },
    CommandsNames.create_new_module: {
        'en': f"Enter a module name (1-{max_name_length} characters):\n"
              "- Use Latin letters, numbers, spaces.\n"
              "- Avoid special characters.\n"
              f"\n/{CommandsNames.cancel} to cancel creation.",

        'ru': f"Введите название модуля (1-{max_name_length} символов):\n"
              "- Используйте латинские буквы, цифры, пробелы.\n"
              "- Избегайте специальных символов.\n"
              f"\n/{CommandsNames.cancel} для отмены создания."

    },

    # Donate

    '/donate': {
        'en': "https://donate.stream/repeatreminddonate",
        'ru': "https://donate.stream/repeatreminddonate"
    },

    # Other

    'maximum_number_of_modules': {
        'en': "<b>You have reached the maximum number of saved modules!</b>\n"
              "This is due to the project still being in development and using a free subscription"
              " to a database service.",
        'ru': "<b>Вы достигли максимального возможного количества сохраненных модулей!</b>\n"
              "Это связано с тем, что проект развивается и использует бесплатную подписку"
              " сервиса для базы данных."
    },
    'not_updated_user': {
        'en': "Welcome back! We've upgraded our bot's structure, and your account is now up to date."
              " Everything is set, so you can use the bot like you always have. Need help? /help",
        'ru': "Добро пожаловать обратно! Мы обновили структуру нашего бота,"
              " и ваш аккаунт теперь в актуальном состоянии. Всё готово, и вы можете использовать бота как раньше."
              " Нужна помощь? /help"

    },
    'default_response': {
        'en': "I didn't catch that. Please try one of the commands I understand, or type /help for assistance.",
        'ru': "Я не смог это распознать. Попробуйте одну из команд, которые я знаю, или напишите /help для помощи."

    },
    'nothing_to_cancel': {
        'en': "There's currently nothing to cancel. You're all set in the standard mode."
              " Feel free to reach out if you have any questions or need support! /help",
        'ru': "Сейчас отменять нечего. Вы уже в стандартном режиме."
              " Обращайтесь, если у вас есть вопросы или нужна помощь! /help"
    },

    # Forwarded posts

    'forwarded_post': {
        'en': "<b>An update has been released in the bot!</b>\n\n"
              "To change the setting of update notifications, write /settings",
        'ru': "<b>В боте вышло обновление!</b>\n\n"
              "Чтобы изменить настройку уведомлений об обновлениях, напишите /settings"
    }
}

DONATE_LEXICON: dict[str, dict[str, str]] = {
    'title': {
        'en': "Bot Support",
        'ru': "Поддержка бота"
    },
    'description': {
        'en': "If you liked the project,"
              " the author would be very pleased to receive your support for further development!\n",
        'ru': "Если проект вам понравился,"
              " автору было бы очень приятно получить от вас поддержку для дальнейшего развития!\n"
    },
    'donate_label': {
        'en': "Bot Support ☕",
        'ru': "Поддержка бота ☕"
    },
    'thanks_for_support': {
        'en': "Thank you so much for your support! RepeatRemindBot remembered your kindness)",
        'ru': "Большое спасибо за поддержку! RepeatRemindBot запомнил вашу доброту)"
    },
    'choose_value': {
        'en': "How much do you want to donate to the bot?",
        'ru': "Сколько вы хотите пожертвовать боту?"
    },
}

SETTINGS_LEXICON: dict[str, dict[str, str]] = {
    CommandsNames.change_language: {
        'en': "Сhoose your language:\n🇺🇸 English\n🇷🇺 Русский",
        'ru': "Выберите язык:\n🇺🇸 English\n🇷🇺 Русский"
    },
    'language': {
        'en': "🇺🇸",
        'ru': "🇷🇺",
    },
    'changed_language': {
        'en': "You have changed the language to English 🇺🇸",
        'ru': "Вы сменили язык на русский 🇷🇺"
    },
    'cancel_input': {
        'en': "Input was canceled.",
        'ru': "Ввод был отменен."
    },
    CommandsNames.change_words_in_block: {
        'en': "Choose the block size to split the module (from 5 to 15 elements)."
              f"\n/{CommandsNames.cancel} - for cancel input.",
        'ru': "Выберите размер блока для разделения модуля (от 5 до 15 элементов)."
              f"\n/{CommandsNames.cancel} - для отмены ввода."

    },
    CommandsNames.change_repetitions_for_block: {
        'en': "Set your desired number from 1 to 10 of repetitions for each block"
              f"\n/{CommandsNames.cancel} - for cancel input.",
        'ru': "Задайте желаемое количество повторений блока от 1 до 10."
              f"\n/{CommandsNames.cancel} - для отмены ввода."
    },
    'not_valid_words_in_block': {
        'en': "The number should be between 5 and 15.",
        'ru': "Число должно быть от 5 до 15."
    },
    'not_valid_repetitions_for_block': {
        'en': "The number should be between 1 and 10.",
        'ru': "Число должно быть от 1 до 10."
    },
    'sent_new_words_in_block': {
        'en': "The number of items per block has been updated to {number} ✅",
        'ru': "Количество элементов в блоке обновлено до {number} ✅"
    },
    'sent_new_repetitions_for_block': {
        'en': "The number of repetitions per block has been updated to {number} ✅",
        'ru': "Количество повторений блока обновлено до {number} ✅"
    },
    'get_updates': {
        'en': "Receive notifications about updates: ",
        'ru': "Получать уведомления об обновлениях: "
    }
}

CREATING_MODULE_LEXICON = {
    'not_valid_name': {
        'en': "The module name is limited to 1-20 characters and may include:"
              "\n- Latin letters (any case)"
              "\n- Digits"
              "\n- Spaces"
              "\nEnsure it meets these criteria.",
        'ru': "Название модуля должно быть от 1 до 20 символов и может включать:"
              "\n- Латинские буквы (любой регистр)"
              "\n- Цифры"
              "\n- Пробелы"
              "\nПроверьте соответствие этим критериям."

    },
    'rename_module_button': {
        'en': "Rename Module ✏️",
        'ru': "Переименовать Модуль ✏️"
    },
    'fill_separator': {
        'en': "enter character- to separate words (for example, '/', '|')."
              f"\n\n/{CommandsNames.cancel} - to cancel the module creation",
        'ru': "Введите символ-разделитель слов (например, '/', '|', ',').\n\n"
              f"/{CommandsNames.cancel} - чтобы отменить создание модуля",
    },
    'not_valid_separator': {
        'en': "enter a character to use as a separator.\n"
              f"\n/{CommandsNames.cancel} - to cancel module creation",
        'ru': "введите символ-разделитель.\n"
              f"\n/{CommandsNames.cancel} - чтобы отменить создание модуля"
    },
    'edit_module_separator_button': {
        'en': "Change the separator✏️",
        'ru': "Изменить разделитель✏️"
    },
    'rename_new_module': {
        'en': "<b>Change of Module Name</b>"
              f"\n\nEnter a new name for the module. It should be 1-{max_name_length} characters "
              "long and can include:"
              "\n- Latin letters (any case)"
              "\n- Digits"
              "\n- Spaces"
              "\n\nCheck that the name meets these conditions before entering."
              f"\n\n/{CommandsNames.cancel} - to cancel module creation",
        'ru': "<b>Изменение названия модуля</b>\n\nВведите новое название модуля. Оно должно быть от 1 до "
              f"{max_name_length} символов и может содержать:"
              "\n- Латинские буквы (любой регистр)"
              "\n- Цифры"
              "\n- Пробелы'\n\n"
              "Убедитесь, что название соответствует этим условиям перед вводом."
              f"\n\n/{CommandsNames.cancel} - чтобы отменить создание модуля"
    },
    'edit_separator': {
        'en': "<b>Change of Separator</b>\n\nEnter a new separator character"
              "(e.g., '/', '|', ',').\n\n"
              f"/{CommandsNames.cancel} - to cancel module creation",
        'ru': "<b>Изменение разделителя</b>\n\nВведите новый символ-разделитель(например, '/', '|', ',').\n\n"
              f"/{CommandsNames.cancel} - чтобы отменить создание модуля"
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
        'en': ("Now enter pairs of values separated by your delimiter:"
               "\nkey {separator} value"
               "\n\nYour pairs will be added under the message."
               "\nYou can also send multiple pairs at once, each on the next line:"
               "\nkey1 {separator} value"
               "\nkey2 {separator} value"
               f"\n\n/{CommandsNames.cancel} - to cancel module creation"),
        'ru': ("Теперь вводите пары значений, разделенных выбранным разделителем:"
               "\nключ {разделитель} значение "
               "\n\nВаши пары будут добавляться под сообщением."
               "\nТакже вы можете сразу отправить несколько пар, каждая из которых на отдельной строке:"
               "\nключ1 {разделитель} значение"
               "\nключ2 {разделитель} значение\n\n"
               f"/{CommandsNames.cancel} - чтобы отменить создание модуля")
    },
    'incorrect_pair': {
        'en': ("❌ <b>Incorrect format / reached maximum size of element!</b>"
               "\n\nExample:\nfruit {separator} apple\n\n"
               f"<b>Maximum size of element (sum of key size and value size) - {max_element_length}</b>"
               f"/{CommandsNames.cancel} - to cancel module "
               "creation"),
        'ru': ("❌ <b>Неправильный формат / слишком большой размер элемента!</b>"
               "\n\nПример:\nфрукт {separator} яблоко\n\n"
               f"<b>Максимальный размер элемента (сумма размеров ключа и значения) - {max_element_length}</b>\n\n"
               f"/{CommandsNames.cancel} - чтобы отменить "
               "создание модуля")
    },
    'new_module_info': {
        'en': ("Module name - '{module_name}'."
               "\nSeparator - '{separator}'\n"
               "Number of items - {size}\n"
               f"<b>The number of items must not exceed {max_items_in_module}!</b>\n"
               "-----------------------------------------------------------------------------------------------------"),
        'ru': ("Название модуля - '{module_name}'."
               "\nРазделитель - '{separator}'\n"
               "Количество элементов - {size}\n"
               f"<b>Количество элементов должно быть не больше {max_items_in_module}!</b>\n"
               "-----------------------------------------------------------------------------------------------------")
    },
    'max_items_in_module': {
        'en': f"<b>The maximum number of elements in the module has been reached - {max_items_in_module};"
              " you will not be able to save this module!</b>"
              "\nThis is due to the fact that the project is still in development and is using a free subscription"
              " to the database service.",
        'ru': f"<b>Превышено максимально возможное количество элементов в модуле - {max_items_in_module},"
              " вы не сможете сохранить данный модуль!</b>"
              "\nЭто связано с тем, что проект развивается и использует бесплатную подписку"
              " сервиса для базы данных."
    },
    'max_local_items_in_module': {
        'en': "<b>The maximum number of elements for module creation has been exceeded!"
              " This is because the project is still in development. This limitation"
              " was made to prevent server lag</b>",
        'ru': "<b>Превышено максимально возможное количество элементов при создании модуля!"
              " Это связано с тем, что проект в стадии развития. Это ограничение"
              " было сделано чтобы сервер не тормозил</b>"
    },
    'deleted_pair_from_new_model': {
        'en': "pair {deleted_pair} was deleted",
        'ru': "пара {deleted_pair} была удалена"
    },
    'cant_save_module_qz_max_elements': {
        'en': f"Sorry, your module cannot be saved because it contains more than {max_items_in_module} items."
              "\nThis is due to the project still being in development and using a free subscription service"
              " for the database.",
        'ru': f"Извините, ваш модуль нельзя сохранить, т.к. в нём больше {max_items_in_module} элементов."
              "\nЭто связано с тем, что проект ещё на стадии развития и использует бесплатную подписку сервиса"
              " для базы данных."
    },

    # photo

    'sent_first_photo': {
        'en': "We have uploaded your photo ✅\nWhat is the delimiter for the words in the photo?",
        'ru': "Мы загрузили ваше фото ✅\nКакой разделитель у слов на фотографии?"
    },

    'comma_button': {
        'en': "',' - comma",
        'ru': "',' - запятая"
    },
    'n_button': {
        'en': r"'\n' - each word on a new line",
        'ru': r"'\n' - каждое слово на новой строке"
    },
    'got_text_from_photo': {
        'en': "Text has been extracted.\nFound phrases:\n\n"
              "{phrases}\n\n"
              "Please check the accuracy of the phrases. If something has been misread, ensure that:\n"
              "<b>1. The text in the photo is aligned properly\n"
              "2. There is no extraneous text in the photo\n"
              "3. The lighting in the photo is even\n"
              "4. You have chosen the correct delimiter</b>"
              f"\n\n<b>Note, the maximum number of elements in a module is {max_items_in_module}!</b>",
        'ru': "Текст был считан.\nНайденные фразы:\n\n"
              "{phrases}\n\n"
              "Пожалуйста проверьте корректность фраз, если что-то считалось неправильно, убедитесь что:\n"
              "<b>1. Текст на фото расположен ровно\n"
              "2. На фото нет лишнего текста\n"
              "3. Свет на фото равномерный\n"
              "4. Вы выбрали правильный разделитель</b>"
              f"\n\n<b>Учтите, максимальное количество элементов в модуле - {max_items_in_module}!</b>"
    },
    'translated_text': {
        'en': "Here is the translated text:\n\n"
              "{content}",
        'ru': "Вот переведенный текст:\n\n"
              "{content}"
    },
    'cancel_getting_text_from_photo_button': {
        'en': "Cancel extracting phrases from this photo ❌",
        'ru': "Отменить считывание фраз с данного фото ❌",
    },
    'cancel_translating_photo_button': {
        'en': "Cancel translating phrases from this photo ❌",
        'ru': "Отменить перевод фраз с данного фото ❌"
    },
    'cancel_adding_phrases_from_photo_button': {
        'en': "Cancel adding phrases from this photo ❌",
        'ru': "Отменить добавление фраз с данного фото ❌"
    },
    'auto_translate_photo_button': {
        'en': "Automatic phrase translation 🌐",
        'ru': "Автоматический перевод фраз 🌐"
    },
    'add_phrases_from_photo_button': {
        'en': "Add phrases and their translations ✅",
        'ru': "Добавить фразы и их переводы ✅"
    },

    # other

    'finish_module_button': {
        'en': "Save ✅",
        'ru': "Сохранить ✅"
    },
    'module_saved': {
        'en': "You saved module {module_name}. It has ID: {module_id}",
        'ru': "Вы сохранили модуль {module_name}. Его ID: {module_id}"
    },
    'cancel_creating_module': {
        'en': "You have exited the module creation mode. Now you can perform other actions.\n/help",
        'ru': "Вы вышли из режима создания модуля. Теперь вы можете выполнить другие действия.\n/help"
    },
    'cancel_editing_module': {
        'en': "You have exited the module editing mode. Now you can perform other actions.\n/help",
        'ru': "Вы вышли из режима редактирования модуля. Теперь вы можете выполнить другие действия.\n/help"
    },
    'unintended_creating_module': {
        'en': ("Your message is not provided by the bot in the current state."
               f"\n/{CommandsNames.cancel} - to cancel the "
               "module creation"),
        'ru': ("Ваше сообщение не предусмотрено ботом в текущем состоянии."
               f"\n/{CommandsNames.cancel} - чтобы отменить "
               "создание модуля")
    },
}

SAVED_MODULES_LEXICON: dict[str, dict[str, str]] = {
    'list_of_saved_modules': {
        'en': "Your saved modules:"
              "\n\n/help",
        'ru': "Ваши сохраненные модули:"
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
        'en': "Such module does not exist.",
        'ru': "Такого модуля не существует."
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
        'en': "Modify the module following the same rules used for its creation.",
        'ru': "Изменяйте модуль по тем же правилам, по которым вы его создавали."
    },
    'cancel_to_over_editing': {
        'en': f"/{CommandsNames.cancel} - to cancel editing the module.",
        'ru': f"/{CommandsNames.cancel} - чтобы отменить изменение модуля."
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
        'en': "Great! Let's review the module {module_name}!"
              "\n\n<b>Repeat Settings:</b>\n"
              "\t<b>Number of blocks</b> - {blocks_num}\n"
              "\t<b>Items per block</b> - {words_in_block_num}\n"
              "\t<b>Repetitions per block</b> - {repetitions_num}"
              "\n\n<b>Change these settings in /settings.</b>"
              "\n\n<b>Module Breakdown:</b>\n"
              "{content}\n"
              "\nFor help, use /help",

        'ru': "Отлично! Повторим модуль {module_name}!"
              "\n\n<b>Настройки повторения:</b>\n"
              "\t<b>Количество блоков</b> - {blocks_num}\n"
              "\t<b>Элементов в блоке</b> - {words_in_block_num}\n"
              "\t<b>Повторений в блоке</b> - {repetitions_num}"
              "\n\n<b>Изменение настроек доступно в /settings.</b>"
              "\n\n<b>Разбивка модуля на блоки:</b>\n"
              "{content}\n"
              "\nДля помощи используйте /help"

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
              f"\n\n/{CommandsNames.cancel} - to stop the review",
        'ru': "Сейчас вы повторяете модуль {module_name}.\n"
              "Блок - {cur_block}/{blocks}\n"
              "Завершенных повторений этого блока - {current_repetitions}/{repetitions}"
              f"\n\n/{CommandsNames.cancel} - чтобы остановить повторение модуля"
    },
    'cancel_repeating_module': {
        'en': "The review has been canceled.\n"
              "\n/help",
        'ru': "Повторение было отменено.\n"
              "\n/help"
    },
    'cancel_editing_module': {
        'en': "Module editing has been canceled.\n"
              "\n/help",
        'ru': "Изменение модуля было отменено.\n"
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
              "Consider taking a 1-3 minute break before continuing."
              f"\n\n/{CommandsNames.cancel} - to stop the review",
        'ru': "Вы закончили одно из повторений блока! 🎉\n"
              "Советуем отдохнуть 1-3 минуты перед продолжением."
              f"\n\n/{CommandsNames.cancel} - чтобы остановить повторение модуля"
    },
    'finish_block': {
        'en': "You've finished reviewing the entire block! 🎉🎉\n"
              "Consider taking a 1-3 minute break before starting the next block."
              f"\n\n/{CommandsNames.cancel} - to stop the review",
        'ru': "Вы закончили повторять целый блок! 🎉🎉\n"
              "Советуем отдохнуть 1-3 минуты перед началом следующего блока!"
              f"\n\n/{CommandsNames.cancel} - чтобы остановить повторение модуля"
    },
    'repeating_all_module': {
        'en': "You've repeated all blocks! 🎉🎉🎉\n"
              "Consider taking a 1-3 minute break before the final review of the entire module."
              f"\n\n/{CommandsNames.cancel} - to stop the review",
        'ru': "Вы повторили все блоки! 🎉🎉🎉\n"
              "Советуем отдохнуть 1-3 минуты перед финальным повторением всего модуля."
              f"\n\n/{CommandsNames.cancel} - чтобы остановить повторение модуля"
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

GET_MODULE_BY_ID_LEXICON: dict[str, dict[str, str]] = {
    'get_module_by_id': {
        'en': "EnterID of the module you wish to retrieve.\n"
              "You can find the module ID next to its name in the list of saved modules."
              f"\n\n/{CommandsNames.cancel} - to cancel sending the module ID.",
        'ru': "Введите ID модуля, который вы хотите получить.\n"
              "ID модуля можно увидеть рядом с названием в списке сохраненных модулей."
              f"\n\n/{CommandsNames.cancel} - чтобы отменить отправку ID модуля."
    },
    'incorrect_type': {
        'en': "The ID must be a positive integer!",
        'ru': "ID должен быть натуральным числом!"
    },
    'cant_find_module': {
        'en': "❌ The module with the specified ID was not found.",
        'ru': "❌ Модуль с указанным ID не был найден."
    },
    'module_was_saved': {
        'en': "✅ The module {module_name} was successfully found and saved! Your copy has the ID: {module_id}.",
        'ru': "✅ Модуль {module_name} был успешно найден и сохранён! Его копия у вас имеет ID: {module_id}."
    },
    'cancel': {
        'en': "Saving the module by its ID has been cancelled.",
        'ru': "Сохранение модуля по его ID было отменено."
    }

}

LEXICON_COMMANDS: dict[str, str] = {
    '/help': 'Description of available commands.',
    f'/{CommandsNames.settings}': 'Your settings.',
    f'/{CommandsNames.create_new_module}': 'Create a new module.',
    f'/{CommandsNames.saved_modules}': 'Your saved modules.',
    f'/{CommandsNames.get_module_by_id}': "Save someone else's module using ID.",
    f'/{CommandsNames.donate}': "Support the project"
}
