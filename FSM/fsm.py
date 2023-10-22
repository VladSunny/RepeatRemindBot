from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup


class FSMUser(StatesGroup):
    creating_module = State()

