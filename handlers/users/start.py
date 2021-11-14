from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart

from keyboards.inline.authorization import authorization_kb
from loader import dp


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    await message.answer(f"Привет, {message.from_user.full_name}!\n"
                         f"Я umit. бот! Чтобы продолжить, вам нужно пройти авторизацию\n"
                         f"Сначала нажмите на кнопку \"Войти / Зарегистрироваться\" и вам выдадут код.\n"
                         f"Далее нажмите на кнопку \"У меня есть код\" и введите его", reply_markup=authorization_kb())


