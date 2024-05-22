from aiogram import Router, Bot
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from FSM.fsm import FSMCreatingModule
from config_data.user_restrictions import *
from database.database import *
from messages_keyboards.new_module_kb import gpt_module_keyboard
from services.creating_module_service import elements_to_text, add_new_pairs
from services.yandexgpt_service import ai_generate_module
from filters.CallbackDataFactory import AddGPTModuleCF, CancelGPTModuleCF

router = Router()


@router.message(StateFilter(FSMCreatingModule.fill_content), Command(commands='prompt'))
async def generate_module_by_prompt(message: Message, state: FSMContext):
    user = get_user(message.from_user.id)
    data = await state.get_data()

    if (data["gpt_module"] != None):
        return

    module = await ai_generate_module(message.text[6:], )

    gpt_module_message = await message.answer(
        text=elements_to_text(module, data['separator']),
        reply_markup=gpt_module_keyboard(user['lang'])
    )

    await state.update_data(gpt_module=module)
    await state.update_data(gpt_module_id=gpt_module_message.message_id)
    await state.update_data(prompt_message_id=message.message_id)


@router.callback_query(AddGPTModuleCF.filter(), StateFilter(FSMCreatingModule.fill_content))
async def process_cancel_voice(callback: CallbackQuery,
                                state: FSMContext,
                                bot: Bot):
    data = await state.get_data()

    new_pairs = data['gpt_module']

    await bot.delete_message(callback.from_user.id, data['gpt_module_id'])
    await bot.delete_message(callback.from_user.id, data['prompt_message_id'])
    await state.update_data(gpt_module=None)

    await add_new_pairs(state=state, valid_pairs=new_pairs, chat_id=callback.from_user.id, bot=bot)

    await callback.answer()


@router.callback_query(CancelGPTModuleCF.filter(), StateFilter(FSMCreatingModule.fill_content))
async def process_cancel_voice(callback: CallbackQuery,
                                state: FSMContext,
                                bot: Bot):
    data = await state.get_data()

    await bot.delete_message(callback.from_user.id, data['gpt_module_id'])
    await bot.delete_message(callback.from_user.id, data['prompt_message_id'])
    await state.update_data(gpt_module=None)

    await callback.answer()
