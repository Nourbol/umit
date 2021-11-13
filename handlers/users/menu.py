from aiogram import types
from aiogram.dispatcher.filters import Command
from aiogram.types import CallbackQuery

from apirequests import get_avatar, get_user
from data.config import User, USERS
from keyboards.inline.menu_buttons import menu_kb
from loader import dp, bot


def find_user(user_id):
    for i in range(len(USERS)):
        if USERS[i].user_id == user_id:
            return USERS[i]
    return None


@dp.message_handler(commands=['menu'])
async def show_menu(message: types.Message):
    if find_user(message.from_user.id) is None:
        return

    await message.answer(f"Вот наше меню",
                         reply_markup=menu_kb())


@dp.callback_query_handler(text="profile")
async def show_profile(call: CallbackQuery):
    user = find_user(call.from_user.id)
    avatar = get_avatar(user.token)
    user_info = get_user(user.token)

    text = f"Email: {user_info['email']}\n" \
           f"Никнейм: {user_info['username']}\n" \
           f"Статус: {user_info['status']}"

    if not user_info['avatarUrl'] is None:
        await bot.send_photo(call.message.chat.id, user_info['avatarUrl'])
    await call.message.answer(text)


@dp.message_handler(content_types=['location'])
async def show_points_nearby(message: types.Message):
    lat = message.location.latitude
    lon = message.location.longitude
