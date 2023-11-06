from aiogram import Bot, Dispatcher, Router, types
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, FSInputFile

from markups import *
from data import *
from state import *
from main import bot

dp = Dispatcher()   

@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    response = f"Привет, *{message.from_user.full_name}*!\n" \
                "Ты попал в бота, в котором ты можешь принимать важные решения" \
                "вместе с великими историческими деятелями России 20 века!\n\n" \
                "Чтобы начать играть просто напиши /play"

    await message.answer(response)


@dp.message()
async def message_handler(message: types.Message) -> None:
    if message.text == "/play":
        await play_handler(message)
        return

    for person in data["persons"]:
        if message.text == person["name"]:
            await hero_selector_handler(message, person)
            return


async def hero_selector_handler(message: types.Message, person: dict) -> None:
    text = f"Ты выбрал *{person['name']}*!\n" \
                "Cейчас тебе предстоит принять важные решения вместе с выбранной личностью\n" \
                "В конце игры ты сможешь узнать к чему привели твои выборы\n" \
                "Удачи!"
    await message.answer(text)

    text = "Давай для начала немного познакомимся с нашей личностью:\n" + person["description"]
    await message.answer(text)

    photo = FSInputFile("./src/vitte.jpeg")
    await bot.send_photo(message.from_user.id, photo)

    text = "Теперь начнем игру!"
    await message.answer(text)

    state = State
    # я заебался

async def play_handler(message: types.Message) -> None:
    await message.answer("Выбери персонажа:\n", reply_markup=get_play_keyboard())
     