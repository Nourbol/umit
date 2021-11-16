from aiogram import types
from aiogram.types import ParseMode
from aiogram.utils.markdown import bold

from loader import dp


@dp.message_handler(commands=['help'])
async def bot_help(message: types.Message):
    text = f"{bold('Список комманд')}:\n\n" \
           f"/start — запустить бота\n" \
           f"/menu — открыть меню бота (доступно только для авторизованных пользователей\n" \
           f"/FAQ — ответы на часто задаваемые вопросы"

    await message.answer(text, parse_mode=ParseMode.MARKDOWN)


@dp.message_handler(commands=['FAQ'])
async def show_faq(message: types.Message):
    text = f"{bold('Что такое')} \"umit.\" {bold('бот')}? \n" \
           f"Меня зовут \"umit.\" бот. " \
           f"Я был создан для того, чтобы помогать акимату в контроле проблемных точек в городе. " \
           f"Хотите помочь городу быть лучше? В данном случае, вам стоит вступить в наше сообщество! \n" \
           f"Станьте частью процветающего будущего вашего города!\n\n" \
           f"{bold('Что такое статус?')}\n" \
           f"Статус вы приобретаете получая лайки на своих комментариях." \
           f" Имея высокий статус, акимат будет предоставлять различные бонусы\n\n" \
           f"{bold('Над проектом работали: Владислав Горохов, Айша Балтабаева и Бектибай Нурбол')}"

    await message.answer(text, parse_mode=ParseMode.MARKDOWN)
