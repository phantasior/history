from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

from data import *


def get_play_keyboard() -> ReplyKeyboardMarkup:
    persons_keyboard = [[KeyboardButton(text=person)] for person in data["persons"]]
    return ReplyKeyboardMarkup(keyboard=persons_keyboard, one_time_keyboard=True, resize_keyboard=True, is_persistent=True)


def get_options_keyboard(n) -> ReplyKeyboardMarkup:
    options_keyboard = []
    for i in range(n):
        button = KeyboardButton(text=str(i + 1))
        options_keyboard.append(button)

    return ReplyKeyboardMarkup(keyboard=[options_keyboard], one_time_keyboard=True, resize_keyboard=True, is_persistent=True)