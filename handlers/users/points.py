import requests
from aiogram import types
from aiogram.types import InputMediaPhoto, ReplyKeyboardRemove
from requests.exceptions import MissingSchema

from apirequests import get_nearest
from handlers.users.menu import find_user
from keyboards.inline.spot import comments_kb
from loader import dp, bot


@dp.message_handler(content_types=['location'])
async def show_points_nearby(message: types.Message):
    lat = message.location.latitude
    lon = message.location.longitude

    user = find_user(message.from_user.id)
    point = get_nearest(user.token, lon, lat)
    text = f"Адрес: {point['title']}\n" \
           f"Детали: {point['details']}"

    await message.answer(f"Мы успешно обработали вашу геолокацию!", reply_markup=ReplyKeyboardRemove())

    if len(point['images']) > 1:

        urls = []
        for url in point['images']:
            try:
                requests.get(url)
                media = InputMediaPhoto(url)
                urls.append(media)
            except MissingSchema:
                pass
            except requests.ConnectionError:
                pass
        await bot.send_media_group(message.chat.id, urls)
    elif len(point['images']) == 1:
        url = point['images'][0]
        await bot.send_photo(message.chat.id, url)

    await bot.send_message(message.chat.id, text, reply_markup=comments_kb(point['id']))
