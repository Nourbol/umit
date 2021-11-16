from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.types import ParseMode
from aiogram.utils.markdown import bold

from keyboards.inline.authorization import authorization_kb
from loader import dp, bot


@dp.message_handler(CommandStart(), state="*")
async def bot_start(message: types.Message, state: FSMContext):
    await state.finish()
    text = f"Привет, {message.from_user.full_name}!\n" \
           f"Я \"umit.\" бот! Чтобы продолжить, вам нужно пройти {bold('авторизацию')} 👤\n" \
           f"Сначала нажмите на кнопку \"{bold('Войти / Зарегистрироваться')}\" и вам выдадут код.\n" \
           f"Далее нажмите на кнопку \"{bold('У меня есть код')}\" и введите его"

    url = "https://vg123-test.s3.eu-central-1.amazonaws.com/5b2036ad-08ef-430a-9fda-5ac1aad6c73flogo.png"
    await bot.send_photo(message.chat.id, url, caption=text, reply_markup=authorization_kb(), parse_mode=ParseMode.MARKDOWN)

