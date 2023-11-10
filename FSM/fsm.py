from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup


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


class FSMRepeatingModule(StatesGroup):
    repeating_module = State()
    wait_next_question = State()


class FSMChangeSettings(StatesGroup):
    change_words_in_block = State()
    change_repetitions_for_block = State()


settings_states = [
    FSMChangeSettings.change_words_in_block,
    FSMChangeSettings.change_repetitions_for_block
]
