from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

spot_kb_cb: CallbackData = CallbackData("spot_kb_cb", "action", "spot_id")


def comments_kb(spot_id):
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="Показать комментарии", callback_data=spot_kb_cb.new("show_comments", spot_id))
        ],
        [
            InlineKeyboardButton(text="Добавить комментарий", callback_data=spot_kb_cb.new("add_comment", spot_id))
        ]
    ])