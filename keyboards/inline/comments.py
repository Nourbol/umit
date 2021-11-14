from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def comments_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="Показать комментарии", callback_data="show_comments")
        ],
        [
            InlineKeyboardButton(text="Добавить комментарий", callback_data="add_comment")
        ]
    ])