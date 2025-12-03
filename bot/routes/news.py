from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from ai.ai import ai_request
from newsapi.news import get_news, format_news
from bot.states import MainStates
from bot.commands import findnews_command

news = Router()

@news.message(Command(findnews_command))
async def command_findnews_handler(message: Message, state: FSMContext) -> None:
    await message.answer('Отправьте тему новости')
    await state.update_data(command = Command('findnews'))
    await state.set_state(MainStates.waiting_for_topic)
    

@news.message(MainStates.waiting_for_topic, F.text)
async def handle_news_message(message: Message, state: FSMContext):
    news = get_news(message.text)

    await send_news(message=message, news=news)
    await state.clear()


async def send_news(message: Message, news: dict) -> None:
    for n in news:
        await message.answer(**format_news(news=n).as_kwargs())