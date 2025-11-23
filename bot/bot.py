from os import getenv

from aiogram import Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message

from bot.routes.news import news

TOKEN = getenv('NewsBotToken')

dp = Dispatcher()
dp.include_router(news)
last_user = None
bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    text = 'Привет. Отправь мне заголовок или содержание какой-нибудь новости, а я скажу тебе, насколько она позитивна и популярна в последнее время.'

    await message.answer(text)
