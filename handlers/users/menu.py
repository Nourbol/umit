from typing import List

import requests
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import CallbackQuery, InputMediaPhoto, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData
from requests.exceptions import MissingSchema

import apirequests
from apirequests import get_user, get_avatar
from data.config import USERS
from keyboards.inline.menu_buttons import menu_kb, get_location_kb
from keyboards.inline.profile_keyboard import get_profile_kb, profile_kb_cb
from loader import dp, bot


def find_user(user_id):
    for i in range(len(USERS)):
        if USERS[i].user_id == user_id:
            return USERS[i]
    return None


@dp.message_handler(commands=['menu'], state="*")
async def show_menu(message: types.Message, state: FSMContext):
    await state.finish()

    if find_user(message.from_user.id) is None:
        return

    await message.answer(f"Выберите действие👾",
                         reply_markup=menu_kb())


@dp.callback_query_handler(text="profile")
async def show_profile(call: CallbackQuery):
    user = find_user(call.from_user.id)
    user_info = get_user(user.token)

    text = f"Ваш профиль:\n" \
           f"----------------------------------\n" \
           f"Email: {user_info['email']}\n" \
           f"Никнейм: {user_info['username']}\n" \
           f"----------------------------------\n" \
           f"Статус: {user_info['status']}\n" \
           f"(генерируется на основе вашей активности)"
    try:
        url = user_info['avatarUrl']
        if url is not None:
            await bot.send_photo(call.message.chat.id, url, caption=text, reply_markup=get_profile_kb())
        else:
            await bot.send_message(call.message.chat.id, text, reply_markup=get_profile_kb())
    except MissingSchema:
        pass
    except requests.ConnectionError:
        pass


@dp.callback_query_handler(profile_kb_cb.filter(action="exit"))
async def sign_out_handler(call: CallbackQuery):
    user = find_user(call.from_user.id)
    USERS.remove(user)
    await call.message.answer("Вы вышли с аккаунта, чтобы авторизоваться снова, перейдите по команде /start")


set_avatar_kb_cb: CallbackData = CallbackData("set_avatar_kb_cb", "id")


class SetAvatarState(StatesGroup):
    progress = State()


@dp.callback_query_handler(profile_kb_cb.filter(action="avatar"))
async def change_avatar_handler(call: CallbackQuery, state: FSMContext):
    avatars: List = get_avatar()
    await SetAvatarState.progress.set()
    await state.update_data(avatars=avatars)
    await download_more_avatars_handler(call, state)


@dp.callback_query_handler(profile_kb_cb.filter(action="avatar"), state=SetAvatarState.progress)
async def download_more_avatars_handler(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    avatars = data["avatars"]

    for i, avatar in enumerate(avatars):
        kb = InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(text="Выбрать этот аватар", callback_data=set_avatar_kb_cb.new(avatar["id"]))
            ]])
        await bot.send_photo(chat_id=call.message.chat.id, photo=avatar["url"], reply_markup=kb)

        avatars.remove(avatar)
        if i == 2:
            break
    await state.update_data(avatars=avatars)

    buttons = []
    text = "Аватары закончились, Вы моежет выбрать один из отправленных, либо завершить выбор аватара"
    if len(avatars) != 0:
        text = f"Еще есть {len(avatars)} аватаров, загрузить еще?"
        buttons.append([
            InlineKeyboardButton(text="Загрузить еще", callback_data=profile_kb_cb.new("avatar"))
        ])

    buttons.append([
        InlineKeyboardButton(text="Завершить выбор аватарки", callback_data=profile_kb_cb.new("stop"))
    ])

    kb = InlineKeyboardMarkup(inline_keyboard=buttons)
    await call.message.answer(text, reply_markup=kb)


@dp.callback_query_handler(profile_kb_cb.filter(action="stop"), state=SetAvatarState.progress)
async def stop_avatar_set(call: CallbackQuery, state: FSMContext):
    await state.finish()
    await call.message.answer("Вы завершили выбор аватарки, можете перейти в /menu")


@dp.callback_query_handler(set_avatar_kb_cb.filter(), state=SetAvatarState.progress)
async def set_avatar(call: CallbackQuery, callback_data: dict, state: FSMContext):
    user = find_user(call.from_user.id)
    apirequests.set_avatar(user.token, callback_data["id"])
    await call.message.answer(f"Аватар выбран, Вы можете перейти в /menu")
    await state.finish()


@dp.callback_query_handler(text="nearest_point")
async def ask_location(call: CallbackQuery):
    await call.message.answer("Поделитесь своим местоположением✈️!", reply_markup=get_location_kb())

# Сделай так, чтобы при нажатии инлайн-кнопки "Мои комментарии", бот отвечал сообщением (см. схему Влада) и прикрепи
# нужные инлайн-кнопки
