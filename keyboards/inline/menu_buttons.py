from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def menu_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="Точка поблизости", callback_data="nearest_point")
        ],
        [
            InlineKeyboardButton(text="Мои комментарии", callback_data="my_comments")
        ],
        [
            InlineKeyboardButton(text="Профиль", callback_data="profile")
        ]
    ])


def get_location_kb():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button = types.KeyboardButton("Share Position", request_location=True)
    keyboard.add(button)
    return keyboard
