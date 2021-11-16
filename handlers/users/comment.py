from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import CallbackQuery, Message, ParseMode
from aiogram.utils.markdown import bold

from apirequests import get_comments, post_likes
from handlers.users.menu import find_user
from keyboards.inline.comments import show_comments_kb, author_like_kb, author_like_kb_cb
from keyboards.inline.spot import spot_kb_cb
from loader import dp, bot


class ShowingComments(StatesGroup):
    comments = State()


async def show_n_comments(n, message: Message, state: FSMContext):
    comments: [] = (await state.get_data())["comments"]
    if len(comments) < n:
        n = len(comments)

    for i in range(n):
        text = f"{comments[i]['text']}\n\n" \
               f"Комментарий понравился {comments[i]['likes']} людям\n" \
               f"{bold('Комментарий был оставлен')}: {comments[i]['creationDate']}\n" \
               f"{bold('Имя пользователя')}: {comments[i]['authorsUsername']}\n" \
               f"{bold('Статус пользователя')}: {comments[i]['authorsStatus']}\n"

        await message.answer(text, reply_markup=author_like_kb(comments[i]['id']), parse_mode=ParseMode.MARKDOWN)

    comments = comments[n:]
    await state.update_data(comments=comments)


@dp.callback_query_handler(author_like_kb_cb.filter(action="like"), state=ShowingComments.comments)
async def like_comment(call: CallbackQuery, state: FSMContext, callback_data: dict):
    user = find_user(call.from_user.id)
    like = post_likes(user.token, (await state.get_data())['spot_id'], callback_data['comment_id'])
    if not like is None:
        await bot.answer_callback_query(call.id, f"Лайк поставлен ❣️", show_alert=True)
    else:
        await bot.answer_callback_query(call.id, f"Нельзя поставить лайк более одного раза!", show_alert=True)


@dp.callback_query_handler(spot_kb_cb.filter(action='show_comments'))
async def show_comments(call: CallbackQuery, state: FSMContext, callback_data: dict):
    user = find_user(call.from_user.id)
    await ShowingComments.comments.set()
    comments = get_comments(user.token, callback_data['spot_id'])
    await state.update_data(comments=comments)
    await state.update_data(spot_id=callback_data['spot_id'])

    if len(comments) == 0:
        await bot.answer_callback_query(call.id, f"Комментариев еще нет. Будьте первыми!", show_alert=True)
        await state.finish()
        return

    await show_n_comments(3, call.message, state)
    if len(comments) >= 3:
        await call.message.answer("Вы можете заргузить еще комментарии 👾\n"
                                  "Если хотите прекратить просмотр комментариев, нажмите на /stop ",
                                  reply_markup=show_comments_kb(callback_data['spot_id']))
    else:
        await call.message.answer(f"Если хотите прекратить просмотр комментариев, нажмите на /stop ")


@dp.callback_query_handler(spot_kb_cb.filter(action='show_more_comments'))
async def show_more_comments(call: CallbackQuery, state: FSMContext, callback_data: dict):
    user = find_user(call.from_user.id)
    await show_n_comments(3, call.message, state)
    if len((await state.get_data())["comments"]) >= 3:
        await call.message.answer("Вы можете заргузить еще комментарии 👾",
                                  reply_markup=show_comments_kb(callback_data['spot_id']))
    else:
        await show_n_comments(len((await state.get_data())["comments"]), call.message, state)


@dp.message_handler(commands=['stop'], state=ShowingComments)
async def stop_showing_comments(message: Message, state: FSMContext):
    await message.answer(f"Вы прекратили просмотр комментариев")

    await state.finish()
