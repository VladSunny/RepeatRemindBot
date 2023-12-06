from __future__ import annotations

from aiogram import F, Router, Dispatcher
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.types import CallbackQuery, Message, Update, ReplyKeyboardRemove
from aiogram.fsm.state import default_state, State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage

from database.database import *
from keyboards.reapeating_module_kb import correct_answer_keyboard, incorrect_answer_keyboard

from lexicon.lexicon import REPEATING_MODULE_LEXICON, CommandsNames

from FSM.fsm import FSMRepeatingModule

from services.service import send_and_delete_message, change_message, delete_message, send_message
from services.repeating_module_service import get_current_questions, get_all_questions

from filters.CallbackDataFactory import RepeatModuleCF, ConfirmRepeatingCF, AnswerWasCorrectCF, NextQuestionCF

import json
import random
from collections import deque

storage = MemoryStorage()
dp = Dispatcher(storage=storage)

user_data_template = {
    'current_block': 1,
    'current_repetitions': 0,
    'header_message_id': 0,
    'module_id': 0,
    'learning_content': {},
    'current_questions': deque(),
    'question_message_id': 0,
    'separator': '',
    'module_name': "",
    'user_lang': "en",
    'repetitions': 0,
    'finish_learning_blocks': False,
}

router = Router()


@router.message(Command(commands=CommandsNames.cancel), StateFilter(FSMRepeatingModule.repeating_module,
                                                                    FSMRepeatingModule.wait_next_question))
async def process_cancel_command(message: Message, state: FSMContext):
    user = get_user(message.from_user.id)
    await message.answer(
        text=REPEATING_MODULE_LEXICON['cancel_repeating_module'][user['lang']],
        reply_markup=ReplyKeyboardRemove()
    )

    data = await state.get_data()

    await delete_message(chat_id=message.chat.id, message_id=data['question_message_id'])

    await state.clear()


@router.callback_query(ConfirmRepeatingCF.filter(), StateFilter(default_state))
async def process_start_repeating_module(callback: CallbackQuery,
                                         callback_data: ConfirmRepeatingCF,
                                         state: FSMContext):
    user = get_user(callback.from_user.id)

    data = await state.get_data()

    user_settings = get_settings(callback.from_user.id)
    module_id = callback_data.module_id
    module = get_module(module_id)
    learning_content = data['learning_content']
    current_questions = deque(get_current_questions(learning_content[f'block_{1}']))

    new_user_data = deepcopy(user_data_template)
    new_user_data['header_message_id'] = callback.message.message_id
    new_user_data['module_id'] = module_id
    new_user_data['learning_content'] = learning_content
    new_user_data['current_questions'] = current_questions
    new_user_data['separator'] = module['separator']
    new_user_data['module_name'] = module['name']
    new_user_data['user_lang'] = user['lang']
    new_user_data['repetitions'] = user_settings['repetitions_for_block']

    await change_message(chat_id=callback.from_user.id,
                         message_id=callback.message.message_id,
                         reply_markup=None,
                         text=REPEATING_MODULE_LEXICON['repeating_module_header'][user['lang']]
                         .format(module_name=module['name'],
                                 current_repetitions=0,
                                 cur_block=1,
                                 repetitions=user_settings['repetitions_for_block'],
                                 blocks=len(learning_content))
                         )

    question_message = await send_message(chat_id=callback.from_user.id,
                                          text=f"{current_questions[0][0]} {module['separator']} ?")

    new_user_data['question_message_id'] = question_message.message_id

    await state.update_data(new_user_data)
    await state.set_state(FSMRepeatingModule.repeating_module)

    await callback.answer()


@router.message(StateFilter(FSMRepeatingModule.repeating_module))
async def process_got_answer(message: Message, state: FSMContext):
    data = await state.get_data()
    current_pair = data['current_questions'][0]

    await message.delete()

    current_pair

    if message.text is None or current_pair[1].lower().strip() != message.text.lower().strip():
        await change_message(chat_id=message.from_user.id,
                             text=REPEATING_MODULE_LEXICON['incorrect_answer'][data['user_lang']].format(
                                 correct_answer=f"{current_pair[0]} {data['separator']} {current_pair[1]}"
                             ),
                             message_id=data['question_message_id'],
                             reply_markup=incorrect_answer_keyboard(data['user_lang']))

        data['current_questions'].append(data['current_questions'][0])
        data['current_questions'].popleft()

        await state.set_state(FSMRepeatingModule.wait_next_question)
        await state.update_data(data)

    else:
        data['current_questions'].popleft()

        await state.update_data(data)

        await next_question(data=data, chat_id=message.from_user.id, state=state)

        await send_and_delete_message(chat_id=message.from_user.id,
                                      text=REPEATING_MODULE_LEXICON['correct_answer'][data['user_lang']].format(
                                          correct_answer=f"{current_pair[0]} {data['separator']} {current_pair[1]}"
                                      ), delete_after=3)


@router.callback_query(AnswerWasCorrectCF.filter(), StateFilter(FSMRepeatingModule.wait_next_question))
async def process_answer_was_correct(callback: CallbackQuery,
                                     callback_data: AnswerWasCorrectCF,
                                     state: FSMContext):
    data = await state.get_data()

    question = data['current_questions'][-1]

    data['current_questions'].pop()

    await change_message(chat_id=callback.from_user.id,
                         text=REPEATING_MODULE_LEXICON['answer_was_correct_pressed'][data['user_lang']].format(
                             correct_answer=f"{question[0]} {data['separator']} {question[1]}"
                         ),
                         message_id=data['question_message_id'],
                         reply_markup=correct_answer_keyboard(data['user_lang']))

    await state.update_data(data)
    await callback.answer()


async def next_question(data, chat_id, state):
    if len(data['current_questions']) > 0:
        question = data['current_questions'][0]

        await change_message(chat_id=chat_id,
                             text=f"{question[0]} {data['separator']} ?",
                             message_id=data['question_message_id'],
                             reply_markup=None,
                             can_repeat=True)

        await state.set_state(FSMRepeatingModule.repeating_module)

    else:
        if data['current_repetitions'] == data['repetitions'] - 1:
            if data['current_block'] == len(data['learning_content']):
                if data['finish_learning_blocks']:
                    await change_message(chat_id=chat_id,
                                         text=REPEATING_MODULE_LEXICON['finish_all_repeating'][data['user_lang']],
                                         message_id=data['question_message_id'],
                                         reply_markup=None)

                    await state.clear()

                else:
                    data['finish_learning_blocks'] = True
                    data['current_questions'] = deque(get_all_questions(data['learning_content']))
                    await state.update_data(data)

                    await change_message(chat_id=chat_id,
                                         text=REPEATING_MODULE_LEXICON['repeating_all_module'][data['user_lang']],
                                         message_id=data['question_message_id'],
                                         reply_markup=correct_answer_keyboard(data['user_lang']))

                    await change_message(chat_id=chat_id,
                                         message_id=data['header_message_id'],
                                         reply_markup=None,
                                         text=REPEATING_MODULE_LEXICON['repeating_all_module_header'][data['user_lang']]
                                         .format(module_name=data['module_name']))

                    await state.set_state(FSMRepeatingModule.wait_next_question)

            else:
                data['current_block'] += 1
                data['current_repetitions'] = 0
                data['current_questions'] = deque(get_current_questions(data['learning_content']
                                                                        [f'block_{data["current_block"]}']))
                await state.update_data(data)

                await change_message(chat_id=chat_id,
                                     text=REPEATING_MODULE_LEXICON['finish_block'][data['user_lang']],
                                     message_id=data['question_message_id'],
                                     reply_markup=correct_answer_keyboard(data['user_lang']))

                await change_message(chat_id=chat_id,
                                     message_id=data['header_message_id'],
                                     reply_markup=None,
                                     text=REPEATING_MODULE_LEXICON['repeating_module_header'][data['user_lang']]
                                     .format(module_name=data['module_name'],
                                             current_repetitions=data['current_repetitions'],
                                             cur_block=data['current_block'],
                                             repetitions=data['repetitions'],
                                             blocks=len(data['learning_content'])
                                             )
                                     )

                await state.set_state(FSMRepeatingModule.wait_next_question)

        else:
            data['current_repetitions'] += 1
            data['current_questions'] = deque(get_current_questions(data['learning_content']
                                                                    [f'block_{data["current_block"]}']))
            await state.update_data(data)

            await change_message(chat_id=chat_id,
                                 text=REPEATING_MODULE_LEXICON['finish_repetition'][data['user_lang']],
                                 message_id=data['question_message_id'],
                                 reply_markup=correct_answer_keyboard(data['user_lang']))

            await change_message(chat_id=chat_id,
                                 message_id=data['header_message_id'],
                                 reply_markup=None,
                                 text=REPEATING_MODULE_LEXICON['repeating_module_header'][data['user_lang']]
                                 .format(module_name=data['module_name'],
                                         current_repetitions=data['current_repetitions'],
                                         cur_block=data['current_block'],
                                         repetitions=data['repetitions'],
                                         blocks=len(data['learning_content'])
                                         )
                                 )

            await state.set_state(FSMRepeatingModule.wait_next_question)


@router.callback_query(NextQuestionCF.filter(), StateFilter(FSMRepeatingModule.wait_next_question))
async def process_next_question(callback: CallbackQuery,
                                callback_data: NextQuestionCF,
                                state: FSMContext):
    data = await state.get_data()

    await next_question(data=data, chat_id=callback.from_user.id, state=state)

    await callback.answer()
