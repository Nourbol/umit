from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

profile_kb_cb: CallbackData = CallbackData("profile_kb_cb", "action")


def get_profile_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="Сменить аватар👤", callback_data=profile_kb_cb.new("avatar"))
        ],
        [
            InlineKeyboardButton(text="Выйти🔙", callback_data=profile_kb_cb.new("exit"))
        ]
    ])
