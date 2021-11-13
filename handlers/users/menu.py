from aiogram import types
from aiogram.dispatcher.filters import Command

from keyboards.inline.menu_buttons import menu_kb
from loader import dp


@dp.message_handler(commands=['menu'])
async def show_menu(message: types.Message):
    await message.answer(f"Вот наше меню",
                         reply_markup=menu_kb())
