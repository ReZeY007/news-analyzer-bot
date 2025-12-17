from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from database.operations.users import get_user_topics

def get_topics_list(user_id: int) -> None:
    builder = InlineKeyboardBuilder()
    topics = get_user_topics(user_id)

    for i in range(len(topics)):
        builder.row(InlineKeyboardButton(text=f'{i + 1}. {topics[i].title}', callback_data=f'topic_{topics[i].id}'))

    return builder