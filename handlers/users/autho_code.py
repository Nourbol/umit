from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import CallbackQuery, Message

from apirequests import post_code
from data.config import USERS, User
from loader import dp


class CheckingCode(StatesGroup):
    code = State()


@dp.callback_query_handler(text="auth_code")
async def check_code(call: CallbackQuery):
    await CheckingCode.code.set()
    await call.message.answer(f"Пожалуйста, введите код 🗝")


@dp.message_handler(state=CheckingCode.code)
async def code_input(message: Message, state: FSMContext):
    code = message.text
    token = post_code(code)
    if not token is None:
        USERS.append(User(message.from_user.id, token))
        await message.answer(f"✔️ Вы успешно прошли авторизацию!\n"
                             f"Для дальнейших дейсвий можете использовать команду /menu 👾")
    else:
        await message.answer(f"✖️ Вы ввели неправильный код! Попробуйте раз!")

    await state.finish()
