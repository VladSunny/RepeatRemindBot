from __future__ import annotations

from collections import deque

from aiogram import Router, Dispatcher, Bot
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import CallbackQuery, Message, ReplyKeyboardRemove

from FSM.fsm import FSMRepeatingModule
from database.database import *
from filters.CallbackDataFactory import ConfirmRepeatingCF, AnswerWasCorrectCF, NextQuestionCF
from messages_keyboards.reapeating_module_kb import correct_answer_keyboard, incorrect_answer_keyboard
from lexicon.lexicon import REPEATING_MODULE_LEXICON, CommandsNames, system_lexicon
from services.repeating_module_service import get_current_questions, get_all_questions
from services.service import send_and_delete_message
from keyboards.keyboards import get_main_keyboard

storage = MemoryStorage()
dp = Dispatcher(storage=storage)

# Шаблон нужной информации для повторения модуля
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
    'cw_blocks': []
}

router = Router()


# Отмена повторения
@router.message(Command(commands=CommandsNames.cancel), StateFilter(FSMRepeatingModule.repeating_module,
                                                                    FSMRepeatingModule.wait_next_question))
async def process_cancel_command(message: Message, state: FSMContext, bot: Bot):
    user = get_user(message.from_user.id)
    await message.answer(
        text=REPEATING_MODULE_LEXICON['cancel_repeating_module'][user['lang']],
        reply_markup=get_main_keyboard(user['lang'])
    )

    data = await state.get_data()

    await bot.delete_message(chat_id=message.chat.id,
                             message_id=data['question_message_id'])

    await state.clear()


# Начало повторения
@router.callback_query(ConfirmRepeatingCF.filter(), StateFilter(default_state))
async def process_start_repeating_module(callback: CallbackQuery,
                                         callback_data: ConfirmRepeatingCF,
                                         state: FSMContext,
                                         bot: Bot):
    user = get_user(callback.from_user.id)

    data = await state.get_data()

    user_settings = get_settings(callback.from_user.id)
    module_id = callback_data.module_id
    module = get_module(module_id)
    learning_content = data['learning_content']
    current_questions = deque(get_current_questions(learning_content[f'block_{1}']))

    # Заполнение нужной информации
    new_user_data = deepcopy(user_data_template)
    new_user_data['header_message_id'] = callback.message.message_id
    new_user_data['module_id'] = module_id
    new_user_data['learning_content'] = learning_content
    new_user_data['current_questions'] = current_questions
    new_user_data['separator'] = module['separator']
    new_user_data['module_name'] = module['name']
    new_user_data['user_lang'] = user['lang']
    new_user_data['repetitions'] = user_settings['repetitions_for_block']
    new_user_data['cw_blocks'].append([0, 0])

    await send_and_delete_message(chat_id=callback.from_user.id,
                                  text=system_lexicon['delete_keyboard'][user['lang']],
                                  delete_after=0,
                                  reply_markup=ReplyKeyboardRemove())

    await bot.edit_message_text(chat_id=callback.from_user.id,
                                message_id=callback.message.message_id,
                                text=REPEATING_MODULE_LEXICON['repeating_module_header'][user['lang']].format(
                                    module_name=module['name'],
                                    current_repetitions=0,
                                    cur_block=1,
                                    repetitions=user_settings['repetitions_for_block'],
                                    blocks=len(learning_content)),
                                reply_markup=None
                                )

    question_message = await bot.send_message(chat_id=callback.from_user.id,
                                              text=f"{current_questions[0][0]} {module['separator']} ?")

    new_user_data['question_message_id'] = question_message.message_id

    await state.update_data(new_user_data)  # Сохраняем нужную информацию локально
    await state.set_state(FSMRepeatingModule.repeating_module)

    await callback.answer()


# Функция для следующего вопроса
async def next_question(data, chat_id, state, bot: Bot):
    # Проверка есть ли ещё вопросы
    if len(data['current_questions']) > 0:
        # Следующий вопрос
        question = data['current_questions'][0]

        await bot.edit_message_text(chat_id=chat_id,
                                    text="...",
                                    message_id=data['question_message_id'],
                                    reply_markup=None)

        await bot.edit_message_text(chat_id=chat_id,
                                    text=f"{question[0]} {data['separator']} ?",
                                    message_id=data['question_message_id'],
                                    reply_markup=None)

        await state.set_state(FSMRepeatingModule.repeating_module)

    # Вопросы закончились
    else:

        # Проверка нужно ли ещё раз повторить блок
        if data['current_repetitions'] == data['repetitions'] - 1:

            # Проверка повторены ли все блоки
            if data['current_block'] == len(data['learning_content']):

                # Провекра сделано ли финальное повторение (вопросы из всех блоков)
                if data['finish_learning_blocks']:
                    await bot.delete_message(chat_id=chat_id, message_id=data['question_message_id'])
                    await bot.send_message(chat_id=chat_id,
                                                text=REPEATING_MODULE_LEXICON['finish_all_repeating'][
                                                         data['user_lang']] +
                                                     REPEATING_MODULE_LEXICON['progress'][data['user_lang']].
                                                format(correct=data['cw_blocks'][-1][0],
                                                       questions=data['cw_blocks'][-1][1]),
                                                reply_markup=get_main_keyboard(data['user_lang']))

                    # Окончание повторения
                    await state.clear()

                else:
                    # Получение вопросов для финального повторения

                    data['finish_learning_blocks'] = True
                    data['current_questions'] = deque(get_all_questions(data['learning_content']))
                    data['cw_blocks'].append([0, 0])

                    await state.update_data(data)

                    await bot.edit_message_text(chat_id=chat_id,
                                                text=
                                                REPEATING_MODULE_LEXICON['repeating_all_module'][data['user_lang']] +
                                                REPEATING_MODULE_LEXICON['progress'][data['user_lang']].
                                                format(correct=data['cw_blocks'][-2][0],
                                                       questions=data['cw_blocks'][-2][1]),
                                                message_id=data['question_message_id'],
                                                reply_markup=correct_answer_keyboard(data['user_lang']))

                    await bot.edit_message_text(chat_id=chat_id,
                                                message_id=data['header_message_id'],
                                                reply_markup=None,
                                                text=REPEATING_MODULE_LEXICON['repeating_all_module_header'][
                                                    data['user_lang']]
                                                .format(module_name=data['module_name']))

                    await state.set_state(FSMRepeatingModule.wait_next_question)

            else:
                # Получение вопросов следующего блока

                data['current_block'] += 1
                data['current_repetitions'] = 0
                data['current_questions'] = deque(get_current_questions(data['learning_content']
                                                                        [f'block_{data["current_block"]}']))
                data['cw_blocks'].append([0, 0])

                await state.update_data(data)

                await bot.edit_message_text(chat_id=chat_id,
                                            text=REPEATING_MODULE_LEXICON['finish_block'][data['user_lang']] +
                                                 REPEATING_MODULE_LEXICON['progress'][data['user_lang']].
                                            format(correct=data['cw_blocks'][-2][0],
                                                   questions=data['cw_blocks'][-2][1]),
                                            message_id=data['question_message_id'],
                                            reply_markup=correct_answer_keyboard(data['user_lang']))

                await bot.edit_message_text(chat_id=chat_id,
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
            # Следующее повторение блока

            data['current_repetitions'] += 1
            data['current_questions'] = deque(get_current_questions(data['learning_content']
                                                                    [f'block_{data["current_block"]}']))
            data['cw_blocks'].append([0, 0])

            await state.update_data(data)

            await bot.edit_message_text(chat_id=chat_id,
                                        text=REPEATING_MODULE_LEXICON['finish_repetition'][data['user_lang']] +
                                             REPEATING_MODULE_LEXICON['progress'][data['user_lang']].
                                        format(correct=data['cw_blocks'][-2][0], questions=data['cw_blocks'][-2][1]),
                                        message_id=data['question_message_id'],
                                        reply_markup=correct_answer_keyboard(data['user_lang']))

            await bot.edit_message_text(chat_id=chat_id,
                                        message_id=data['header_message_id'],
                                        reply_markup=None,
                                        text=
                                        REPEATING_MODULE_LEXICON['repeating_module_header'][data['user_lang']]
                                        .format(module_name=data['module_name'],
                                                current_repetitions=data['current_repetitions'],
                                                cur_block=data['current_block'],
                                                repetitions=data['repetitions'],
                                                blocks=len(data['learning_content'])
                                                )
                                        )

            await state.set_state(FSMRepeatingModule.wait_next_question)


# Ответ получен
@router.message(StateFilter(FSMRepeatingModule.repeating_module))
async def process_got_answer(message: Message, state: FSMContext, bot: Bot):
    data = await state.get_data()
    current_pair = data['current_questions'][0]
    data['cw_blocks'][-1][1] += 1  # Прибавляем 1 к количеству вопросов в этом повторении

    if message.text is None or current_pair[1].lower().strip() != message.text.lower().strip():
        # Ответ неверный

        await bot.edit_message_text(chat_id=message.from_user.id,
                                    text=REPEATING_MODULE_LEXICON['incorrect_answer'][data['user_lang']].format(
                                        correct_answer=f"{current_pair[0]} {data['separator']} {current_pair[1]}"
                                    ),
                                    message_id=data['question_message_id'],
                                    reply_markup=incorrect_answer_keyboard(data['user_lang']))

        data['current_questions'].append(data['current_questions'][0])
        data['current_questions'].popleft()

        await state.set_state(FSMRepeatingModule.wait_next_question)
        await state.update_data(data)
        await message.delete()

    else:
        # Ответ правильный

        data['current_questions'].popleft()
        data['cw_blocks'][-1][0] += 1  # Прибавляем 1 к количеству правильных ответов в этом повторении

        await state.update_data(data)

        await next_question(data=data, chat_id=message.from_user.id, state=state, bot=bot)

        await message.delete()


# Пользователь выбрал, что ответ был все же верным
@router.callback_query(AnswerWasCorrectCF.filter(), StateFilter(FSMRepeatingModule.wait_next_question))
async def process_answer_was_correct(callback: CallbackQuery,
                                     callback_data: AnswerWasCorrectCF,
                                     state: FSMContext,
                                     bot: Bot):
    data = await state.get_data()

    question = data['current_questions'][-1]

    data['current_questions'].pop()
    data['cw_blocks'][-1][0] += 1  # Прибавляем 1 к количеству правильных ответов в этом повторении

    await bot.edit_message_text(chat_id=callback.from_user.id,
                                text=REPEATING_MODULE_LEXICON['answer_was_correct_pressed'][data['user_lang']].format(
                                    correct_answer=f"{question[0]} {data['separator']} {question[1]}"
                                ),
                                message_id=data['question_message_id'],
                                reply_markup=correct_answer_keyboard(data['user_lang']))

    await state.update_data(data)
    await callback.answer()


# Следующий вопрос
@router.callback_query(NextQuestionCF.filter(), StateFilter(FSMRepeatingModule.wait_next_question))
async def process_next_question(callback: CallbackQuery,
                                callback_data: NextQuestionCF,
                                state: FSMContext,
                                bot: Bot):
    data = await state.get_data()

    await next_question(data=data, chat_id=callback.from_user.id, state=state, bot=bot)

    await callback.answer()
