import os.path
import random

from aiogram import Bot, Dispatcher, Router, types, F
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command, StateFilter
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, FSInputFile
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from markups import *
from data import *
from state import *
from main import bot

dp = Dispatcher()


class OrderHistory(StatesGroup):
    choosing_person = State()
    answering = State()


@dp.message(CommandStart())
async def command_start_handler(message: Message, state: FSMContext) -> None:
    response = f'''Привет, *{message.from_user.full_name}*!
Ты попал в бота, в котором ты можешь принимать важные решения вместе с историческими деятелями России 20 века!

Чтобы начать играть просто напиши /play'''

    await message.answer(response)


@dp.message(Command('play'))
async def play_handler(message: Message, state: FSMContext) -> None:
    await message.answer("Выбери персонажа:\n", reply_markup=get_play_keyboard())
    await state.set_state(OrderHistory.choosing_person)


@dp.message(OrderHistory.choosing_person, F.text.in_(data["persons"].keys()))
async def person_chosen(message: Message, state: FSMContext):
    await state.update_data(person=message.text)
    await state.update_data(action_i=0)
    await state.update_data(result=Result())
    text = f"Ты выбрал *{message.text}*!\n" \
           "Cейчас тебе предстоит принять важные решения вместе с выбранной личностью\n" \
           "В конце игры ты сможешь узнать к чему привели твои выборы\n" \
           "Удачи!"
    await message.answer(text)
    text = "Давай для начала немного познакомимся с нашей личностью:\n" + data['persons'][message.text]["description"]
    await message.answer(text)

    photo = FSInputFile(os.path.join('src', data['persons'][message.text]['image_url']))
    await bot.send_photo(message.from_user.id, photo)

    await ask_question(message, state)


@dp.message(OrderHistory.choosing_person)
async def person_chosen_incorrect(message: Message, state: FSMContext):
    await message.answer("Еще не знаю о таком персонаже, наверное, он был лысым")
    await message.answer("Выбери персонажа:\n", reply_markup=get_play_keyboard())


async def ask_question(message: Message, state: FSMContext):
    user_data = await state.get_data()
    person = user_data['person']
    person_data = data['persons'][person]
    if user_data['action_i'] < len(person_data['actions']):
        action = person_data['actions'][user_data['action_i']]

        text = f'''*{action["name"]}*
{action["description"]}
Ниже возможные исходы:'''
        await message.answer(text)
        for i in range(len(action['options'])):
            await message.answer(f"{i + 1}. " + action['options'][i]["description"])

        await state.update_data(n_options=len(action['options']))
        await message.answer("Прими решение", reply_markup=get_options_keyboard(len(action['options'])))
        await state.set_state(OrderHistory.answering)
    else:
        await print_result(message, state)


async def print_result(message: Message, state: FSMContext):
    await message.answer("Ты такой же гандон как и все деятели\nВыбирай следующего!", reply_markup=get_play_keyboard())
    await state.set_state(OrderHistory.choosing_person)


@dp.message(OrderHistory.answering, F.text.isdigit())
async def question_answered(message: Message, state: FSMContext):
    user_data = await state.get_data()
    selected_option = int(message.text)
    if selected_option < 1 or selected_option > user_data['n_options']:
        selected_option = random.randint(1, user_data['n_options'])
        await message.answer(f"Ты не смог определиться, решил за тебя выбрать *{selected_option}* и отправить в ГУЛАГ")
    person = user_data['person']
    person_data = data['persons'][person]
    action = person_data['actions'][user_data['action_i']]
    option = action["options"][selected_option - 1]
    await message.reply(option['consequence'])
    result = user_data['result']
    result.economy += option['impact']['economy']
    result.elite_opinion += option['impact']['elite_opinion']
    result.international_tension += option['impact']['international_tension']
    result.national_opinion += option['impact']['national_opinion']
    await state.update_data(result=result)
    await state.update_data(action_i=user_data['action_i'] + 1)
    await ask_question(message, state)


@dp.message(OrderHistory.answering)
async def question_answered_incorrect(message: Message, state: FSMContext):
    await message.answer("Прежде чем учить играть в историю, надо научиться считать")
    user_data = await state.get_data()
    await message.answer("Прими решение", reply_markup=get_options_keyboard(user_data['n_options']))

# @dp.message()
# async def message_handler(message: types.Message) -> None:
#     for person in data["persons"]:
#         if message.text == person["name"]:
#             await hero_selector_handler(message, person)
#             return
#
#
# async def hero_selector_handler(message: types.Message, person: dict) -> None:
#     text = f"Ты выбрал *{person['name']}*!\n" \
#                 "Cейчас тебе предстоит принять важные решения вместе с выбранной личностью\n" \
#                 "В конце игры ты сможешь узнать к чему привели твои выборы\n" \
#                 "Удачи!"
#     await message.answer(text)
#
#     text = "Давай для начала немного познакомимся с нашей личностью:\n" + person["description"]
#     await message.answer(text)
#
#     photo = FSInputFile("./src/vitte.jpeg")
#     await bot.send_photo(message.from_user.id, photo)
#
#     text = "Теперь начнем игру!"
#     await message.answer(text)
#
#     state = State
#     # я заебался
