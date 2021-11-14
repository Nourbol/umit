from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import CallbackQuery

from apirequests import get_comments
from handlers.users.menu import find_user
from handlers.users.points import spot_kb_cb
from loader import dp


@dp.callback_query_handler(spot_kb_cb.filter(title="show_comments"))
async def show_comments(call: CallbackQuery, callback_data: dict):
    user = find_user(call.message.from_user.id)
    text = get_comments(user.token, callback_data['spot_id'])


class AddingComment(StatesGroup):
    comment = State()


@dp.callback_query_handler(text="add_comment")
async def add_comments(call: CallbackQuery):
    await AddingComment.comment.set()
    await call.message.answer(f"Напишите свой комментарий и прикрепите фото этой точки!")
