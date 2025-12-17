from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from newsapi.news import analyze_news, get_news
from bot.states import MainStates
from bot.commands import analyzenews_command, findnews_command
from bot.formatting import format_news, format_analyzis
from bot.keyboards import get_topics_list

news = Router()

@news.message(Command(findnews_command))
async def command_findnews_handler(message: Message, state: FSMContext) -> None:
    await state.update_data(command = findnews_command)
    await state.set_state(MainStates.waiting_for_topic)

    try:
        topics_list = get_topics_list(user_id=message.from_user.id)
        await message.answer(text='Сохраненные темы:', reply_markup=topics_list.as_markup())
        await message.answer('Выберете тему из сохранненых или напишите новую.')
    except Exception:
        await message.answer('Напишите тему.')


@news.message(Command(analyzenews_command))
async def command_analyze_news_handler(message: Message, state: FSMContext) -> None:
    await state.update_data(command = analyzenews_command)
    await state.set_state(MainStates.waiting_for_topic)

    try:
        topics_list = get_topics_list(user_id=message.from_user.id)
        await message.answer(text='Сохраненные темы:', reply_markup=topics_list.as_markup())
        await message.answer('Выберете тему из сохранненых или напишите новую.')
    except Exception:
        await message.answer('Напишите тему.')


async def send_news(message: Message, topic: str) -> None:
    try:
        news = get_news(topic)
        for n in news:
            await message.answer(**format_news(news=n).as_kwargs())
    except Exception:
        await message.answer('К сожалению мы ничего не нашли. Попробуйте снова /findnews')


async def send_news_analyzis(message: Message, topic: str) -> None:
    try:
        news = get_news(topic)
        analyzis = await analyze_news(news)
        formated_analyzis = format_analyzis(analyzis)

        await message.answer(**formated_analyzis.as_kwargs())
    except Exception:
        await message.answer('К сожалению мы ничего не нашли. Попробуйте снова /analyzenews')