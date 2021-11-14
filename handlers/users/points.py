import requests
from aiogram import types
from aiogram.types import InputMediaPhoto, ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData
from requests.exceptions import MissingSchema

from apirequests import get_nearest
from handlers.users.menu import find_user
from loader import dp, bot

spot_kb_cb: CallbackData = CallbackData("spot_kb_cb", "action", "spot_id")


def comments_kb(spot_id):
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="Show comments", callback_data=spot_kb_cb.new("show_comments", spot_id))
        ],
        [
            InlineKeyboardButton(text="Add comment", callback_data=spot_kb_cb.new("add_comment", spot_id))
        ]
    ])


@dp.message_handler(content_types=['location'])
async def show_points_nearby(message: types.Message):
    lat = message.location.latitude
    lon = message.location.longitude
    user = find_user(message.from_user.id)
    point = get_nearest(user.token, lon, lat)
    text = f"Адрес: {point['title']}\n" \
           f"Детали: {point['details']}"

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
    if len(urls) > 0:
        await bot.send_media_group(message.chat.id, urls)
    await bot.send_message(message.chat.id, text, reply_markup=comments_kb(point['id']))
