from aiogram.fsm.state import State, StatesGroup


# Состояния при создании модуля
class FSMCreatingModule(StatesGroup):
    fill_name = State()
    fill_separator = State()
    fill_content = State()
    change_name = State()
    change_separator = State()


# creating_module_states = [
#     FSMCreatingModule.fill_name,
#     FSMCreatingModule.fill_content,
#     FSMCreatingModule.fill_separator,
#     FSMCreatingModule.change_name,
#     FSMCreatingModule.change_separator
# ]

creating_module_states = [state.state for state in FSMCreatingModule.__states__]


# Состояния при повторении модуля
class FSMRepeatingModule(StatesGroup):
    repeating_module = State()
    wait_next_question = State()


repeating_module_states = [state.state for state in FSMRepeatingModule.__states__]


# Состояния при изменении настроек
class FSMChangeSettings(StatesGroup):
    change_words_in_block = State()
    change_repetitions_for_block = State()


# settings_states = [
#     FSMChangeSettings.change_words_in_block,
#     FSMChangeSettings.change_repetitions_for_block
# ]

settings_states = [state.state for state in FSMChangeSettings.__states__]


# Состояние при получении модуля по id
class FSMGetModuleById(StatesGroup):
    send_module_id = State()

get_module_by_id_states = [state.state for state in FSMGetModuleById.__states__]


# Состояние при отправке отзыва
class FSMFeedback(StatesGroup):
    send_feedback = State()
