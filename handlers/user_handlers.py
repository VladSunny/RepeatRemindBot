from aiogram import F, Router
from aiogram.filters import Command, CommandStart
from aiogram.types import CallbackQuery, Message
from database.database import *
from filters.CallbackDataFactory import LanguageSelectionCF

from keyboards.change_language_kb import create_change_language_keyboard

from lexicon.lexicon import LEXICON

router = Router()


