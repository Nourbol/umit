from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData


def show_comments_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="Загрузить", callback_data="show_comments")
        ]
    ])


author_like_kb_cb: CallbackData = CallbackData("author_kb_cb", "action", "comment_id", "spot_id")


def author_like_kb(comment_id, spot_id):
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="Показать профиль", callback_data=author_like_kb_cb.new("author_profile", comment_id, spot_id))
        ],
        [
            InlineKeyboardButton(text="Поставить лайк", callback_data=author_like_kb_cb.new("like", comment_id, spot_id))
        ]
    ])
