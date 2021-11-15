import requests
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import CallbackQuery, Message, InputMediaPhoto
from requests.exceptions import MissingSchema

from apirequests import get_comments, get_copy_of_comments
from handlers.users.menu import find_user
from keyboards.inline.comments import show_comments_kb, author_like_kb
from keyboards.inline.spot import spot_kb_cb
from loader import dp, bot


class ShowingComments(StatesGroup):
    comments = State()


async def show_n_comments(n, message: Message, state: FSMContext, spot_id):
    comments: [] = (await state.get_data())["comments"]
    if len(comments) < n:
        n = len(comments)

    for i in range(n):
        text = f"{comments[i]['text']}\n\n" \
               f"Комментарий был оставлен: {comments[i]['creationDate']}"

        await message.answer(text, reply_markup=author_like_kb(comments[i]['id'], spot_id))

    comments = comments[n:]
    await state.update_data(comments=comments)


@dp.callback_query_handler(spot_kb_cb.filter(action='show_comments'))
async def show_comments(call: CallbackQuery, state: FSMContext, callback_data: dict):
    user = find_user(call.from_user.id)
    await ShowingComments.comments.set()
    comments = get_comments(user.token, callback_data['spot_id'])
    await state.update_data(comments=comments)
    await show_n_comments(3, call.message, state, callback_data['spot_id'])
    if len(comments) >= 3:
        await call.message.answer("Вы можете заргузить еще комментарии", reply_markup=show_comments_kb())
    else:
        await show_n_comments(len(comments), call.message, state, callback_data['spot_id'])

    await state.finish()


def find_comment(user_id, comment_id, spot_id):
    comments = get_copy_of_comments(user_id, spot_id)
    for key, comment in enumerate(comments):
        if comment_id == comment['id']:
            return comment


@dp.callback_query_handler(spot_kb_cb.filter(action="show_author_profile"))
async def show_author_profile(call: CallbackQuery, callback_data: dict):
    comment = find_comment(call.message.from_user.id, callback_data['comment_id'], callback_data['spot_id'])
    text = f"Имя пользователя: {comment['authorsUsername']}\n" \
           f"Статус: {comment['authorsStatus']}"

    urls = []
    try:
        url = comment['authorsAvatarUrl']
        requests.get(url)
        media = InputMediaPhoto(url)
        urls.append(media)
    except MissingSchema:
        pass
    except requests.ConnectionError:
        pass
    if len(urls) > 0:
        await bot.send_media_group(call.message.chat.id, urls)
    await bot.send_message(call.message.chat.id, text)


class AddingComment(StatesGroup):
    comment = State()


@dp.callback_query_handler(text="add_comment")
async def add_comments(call: CallbackQuery):
    await AddingComment.comment.set()
    await call.message.answer(f"Напишите свой комментарий и прикрепите фото этой точки!")
