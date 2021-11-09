from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def authorization_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="Sign in/up", url="https://youtu.be/dQw4w9WgXcQ")
        ],
        [
            InlineKeyboardButton(text="У меня есть код", callback_data="auth_code")
        ]
    ])
