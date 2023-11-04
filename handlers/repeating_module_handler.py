from __future__ import annotations

from aiogram import F, Router, Dispatcher
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.types import CallbackQuery, Message, Update
from aiogram.fsm.state import default_state, State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage

from database.database import *
from keyboards.saved_modules_kb import list_of_saved_modules_keyboard, module_info_keyboard
from keyboards.new_module_kb import create_new_module_keyboard

from lexicon.lexicon import CommandsNames, CREATING_MODULE_LEXICON, SAVED_MODULES_LEXICON

from FSM.fsm import FSMRepeatingModule

from services.creating_module_service import is_valid_name, is_valid_separator, get_valid_pairs
from services.service import send_and_delete_message, change_message, delete_message

from filters.CallbackDataFactory import RepeatModuleCF

router = Router()

router.message.filter(StateFilter(FSMRepeatingModule.repeating_module))
