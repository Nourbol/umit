from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import CallbackQuery, Message, ParseMode

from aiogram.utils.markdown import bold
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
        await message.answer(f"☑️ {bold('Вы успешно прошли авторизацию')}!\n"
                             f"Для дальнейших действий — можете воспользоваться командой /menu 👾", parse_mode=ParseMode.MARKDOWN)
    else:
        await message.answer(f"🔘 Вы ввели {bold('неправильный')} код!\n"
                             f"Чтобы повторно ввести код — нажмите на \"{bold('У меня есть код')}\"", parse_mode=ParseMode.MARKDOWN)

    await state.finish()
