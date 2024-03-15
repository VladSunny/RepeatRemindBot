from aiogram.fsm.state import State, StatesGroup


# Состояния при создании модуля
class FSMCreatingModule(StatesGroup):
    fill_name = State()
    fill_separator = State()
    fill_content = State()
    change_name = State()
    change_separator = State()


creating_module_states = [
    FSMCreatingModule.fill_name,
    FSMCreatingModule.fill_content,
    FSMCreatingModule.fill_separator,
    FSMCreatingModule.change_name,
    FSMCreatingModule.change_separator
]


# Состояния при повторении модуля
class FSMRepeatingModule(StatesGroup):
    repeating_module = State()
    wait_next_question = State()


# Состояния при изменении настроек
class FSMChangeSettings(StatesGroup):
    change_words_in_block = State()
    change_repetitions_for_block = State()


settings_states = [
    FSMChangeSettings.change_words_in_block,
    FSMChangeSettings.change_repetitions_for_block
]


# Состояние при получении модуля по id
class FSMGetModuleById(StatesGroup):
    send_module_id = State()


# Состояние при отправке отзыва
class FSMFeedback(StatesGroup):
    send_feedback = State()
