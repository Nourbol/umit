from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import CallbackQuery, Message

from apirequests import send_comment
from handlers.users.menu import find_user
from keyboards.inline.menu_buttons import get_location_kb
from keyboards.inline.spot import spot_kb_cb
from loader import dp


class CommentAddState(StatesGroup):
    text = State()
    coords = State()


@dp.callback_query_handler(spot_kb_cb.filter(action="add_comment"))
async def add_comment_handler(call: CallbackQuery, state: FSMContext, callback_data: dict):
    await CommentAddState.text.set()
    await call.message.answer("Напишите Ваш комментарий")
    await state.update_data(spot_id=callback_data["spot_id"])


@dp.message_handler(state=CommentAddState.text)
async def text_comment_handler(message: Message, state: FSMContext):
    await CommentAddState.coords.set()
    await state.update_data(text=message.text)
    await message.answer("Отлично! Теперь нужно отправить свою геопозици, чтобы подтвердить, "
                         "что вы действительно находитесь на локации 👾", reply_markup=get_location_kb())


@dp.message_handler(content_types=['location'], state=CommentAddState.coords)
async def coord_comment_handler(message: Message, state: FSMContext):
    data = await state.get_data()
    user = find_user(message.from_user.id)
    send_comment(user.token, data["spot_id"], data["text"], message.location.longitude, message.location.latitude)
    await state.finish()
    await message.answer("Вы добавили комментарий")
