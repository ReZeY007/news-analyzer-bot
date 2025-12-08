from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from newsapi.news import get_news, analyze_news
from bot.states import MainStates
from bot.commands import findnews_command
from bot.commands import analyzenews_command
from bot.formating import format_news, format_analyzis

news = Router()

@news.message(Command(findnews_command))
async def command_findnews_handler(message: Message, state: FSMContext) -> None:
    await state.update_data(command = findnews_command)
    await state.set_state(MainStates.waiting_for_topic)

    await message.answer('Отправьте тему новости')
    

@news.message(MainStates.waiting_for_topic, F.text)
async def handle_news_message(message: Message, state: FSMContext):
    data = await state.get_data()
    command = data['command']

    try:
        news = get_news(message.text)

        match command.command:
            case 'findnews':
                await send_news(message=message, news=news)
            case 'analyzenews':
                await send_news_analyzis(message=message, news=news)

        await state.clear()
    except Exception:
        await message.answer("К сожалению, мы ничего не нашли по вашему запросу. Попробуйте еще раз.")
        await message.answer('Отправьте тему новости')


@news.message(Command(analyzenews_command))
async def command_analyze_news_handler(message: Message, state: FSMContext) -> None:
    await state.update_data(command = analyzenews_command)
    await state.set_state(MainStates.waiting_for_topic)

    await message.answer('Отправьте тему новости')


async def send_news(message: Message, news: dict) -> None:
    for n in news:
        await message.answer(**format_news(news=n).as_kwargs())


async def send_news_analyzis(message: Message, news: dict) -> None:
    analyzis = await analyze_news(news)
    formated_analyzis = format_analyzis(analyzis)

    await message.answer(**formated_analyzis.as_kwargs())