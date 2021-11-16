from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

from keyboards.inline.spot import spot_kb_cb


def show_comments_kb(spot_id):
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="Загрузить", callback_data=spot_kb_cb.new("show_more_comments", spot_id))
        ]
    ])


author_like_kb_cb: CallbackData = CallbackData("author_kb_cb", "action", "comment_id")


def author_like_kb(comment_id):
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="Поставить лайк ❣️", callback_data=author_like_kb_cb.new("like", comment_id))
        ]
    ])
