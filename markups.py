from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton

from data import *

def get_play_keyboard() -> ReplyKeyboardMarkup:
    persons_keyboard = []

    for person in data["persons"]:
        button = KeyboardButton(text=person)
        persons_keyboard.append(button)

    return ReplyKeyboardMarkup(keyboard=[persons_keyboard], one_time_keyboard=True)

def get_options_keyboard(n) -> ReplyKeyboardMarkup:
    options_keyboard = []
    for i in range(n):
        button = KeyboardButton(text=str(i + 1))
        options_keyboard.append(button)

    return ReplyKeyboardMarkup(keyboard=[options_keyboard], one_time_keyboard=True)