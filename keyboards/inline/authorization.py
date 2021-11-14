from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def authorization_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="Войти / Зарегистрироваться", url="http://bazarjok-group.com:60010/user/auth")
        ],
        [
            InlineKeyboardButton(text="У меня есть код", callback_data="auth_code")
        ]
    ])
