from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import CallbackQuery, Message

from apirequests import post_code
from loader import dp


class CheckingCode(StatesGroup):
    code = State()


@dp.callback_query_handler(text="auth_code")
async def check_code(call: CallbackQuery):
    await CheckingCode.code.set()
    await call.message.answer(f"Пожалуйста, введите код")


@dp.message_handler(state = CheckingCode.code)
async def code_input(message: Message, state: FSMContext):
    code = message.text
    if not post_code(code) is None:
        await message.answer(f"Все ок!")
    else:
        await message.answer(f"все не ок")

    await state.finish()


