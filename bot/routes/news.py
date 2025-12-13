from aiogram import Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from newsapi.news import get_news, analyze_news
from bot.states import MainStates
from bot.commands import analyzenews_command, findnews_command
from bot.formatting import format_news, format_analyzis
from bot.routes.topics import send_topics_list

news = Router()

@news.message(Command(findnews_command))
async def command_findnews_handler(message: Message, state: FSMContext) -> None:
    await state.update_data(command = findnews_command)
    await state.set_state(MainStates.waiting_for_topic)

    await message.answer('Выберете тему из сохранненых или напишите новую.')
    await send_topics_list(message=message)


@news.message(Command(analyzenews_command))
async def command_analyze_news_handler(message: Message, state: FSMContext) -> None:
    await state.update_data(command = analyzenews_command)
    await state.set_state(MainStates.waiting_for_topic)

    await message.answer('Выберете тему из сохранненых или напишите новую.')
    await send_topics_list(message=message)


async def process_topic(message: Message, topic: str, state: FSMContext) -> None:
    data = await state.get_data()
    command = data['command']
    news = None
    
    try:
        news = get_news(topic)

        match command.command:
            case 'findnews':
                await send_news(message=message, news=news)
            case 'analyzenews':
                await send_news_analyzis(message=message, news=news)
    except Exception:
        await message.answer("К сожалению, мы ничего не нашли по вашему запросу. Попробуйте еще раз.")
        await message.answer('Выберете тему из сохранненых или напишите новую.')
        await send_topics_list(message=message)


async def send_news(message: Message, news: dict) -> None:
    for n in news:
        await message.answer(**format_news(news=n).as_kwargs())


async def send_news_analyzis(message: Message, news: dict) -> None:
    analyzis = await analyze_news(news)
    formated_analyzis = format_analyzis(analyzis)

    await message.answer(**formated_analyzis.as_kwargs())