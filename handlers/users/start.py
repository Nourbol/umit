import requests
from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.types import InputMediaPhoto
from requests.exceptions import MissingSchema

from keyboards.inline.authorization import authorization_kb
from loader import dp, bot


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    text = f"Привет, {message.from_user.full_name}!\n" \
           f"Я umit. бот! Чтобы продолжить, вам нужно пройти авторизацию👤\n " \
           f"Сначала нажмите на кнопку \"Войти / Зарегистрироваться\" и вам выдадут код.\n" \
           f"Далее нажмите на кнопку \"У меня есть код\" и введите его"

    url = "https://vg123-test.s3.eu-central-1.amazonaws.com/5b2036ad-08ef-430a-9fda-5ac1aad6c73flogo.png"
    await bot.send_photo(message.chat.id, url, caption=text, reply_markup=authorization_kb())

