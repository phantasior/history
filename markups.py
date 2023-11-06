from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton

from data import *

def get_play_keyboard() -> ReplyKeyboardMarkup:
    persons_keyboard = []

    for person in data["persons"]:
        button = KeyboardButton(text=person["name"])
        persons_keyboard += [button]

    return ReplyKeyboardMarkup(keyboard=[persons_keyboard], one_time_keyboard=True)