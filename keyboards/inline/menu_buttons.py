import logging

from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

from loader import dp


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


@dp.callback_query_handler(text_contains="my_comments")
async def show_my_comments(call: CallbackQuery):
    await call.answer(cache_time=10)
    callback_data = call.data
    logging.info(f"call={callback_data}")
    await call.message.answer(f"Ваши комментарии:",
                              reply_markup=your_comments_keybord)
