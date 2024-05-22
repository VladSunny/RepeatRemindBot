from aiogram import Router
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from FSM.fsm import FSMCreatingModule
from config_data.user_restrictions import *
from database.database import *
from messages_keyboards.new_module_kb import gpt_module_keyboard
from services.creating_module_service import elements_to_text
from services.yandexgpt_service import ai_generate_module

router = Router()


@router.message(StateFilter(FSMCreatingModule.fill_content), Command(commands='prompt'))
async def generate_module_by_prompt(message: Message, state: FSMContext):
    user = get_user(message.from_user.id)
    data = await state.get_data()

    module = await ai_generate_module(message.text[6:], )
    await message.answer(
        text=elements_to_text(module, data['separator']),
        reply_markup=gpt_module_keyboard(user['lang'])
    )
