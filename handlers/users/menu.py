from aiogram import types
from aiogram.dispatcher.filters import Command
from aiogram.types import CallbackQuery

from apirequests import get_avatar, get_user
from data.config import User, USERS
from keyboards.inline.menu_buttons import menu_kb
from loader import dp, bot


def find_user(user_id):
    for i in USERS:
        if USERS[i].id == user_id:
            return USERS[i]


@dp.message_handler(commands=['menu'])
async def show_menu(message: types.Message):
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
    await bot.send_photo(avatar)
    await call.answer(text)


@dp.message_handler(content_types=['location'])
async def show_points_nearby(message: types.Message):
    lat = message.location.latitude
    lon = message.location.longitude
