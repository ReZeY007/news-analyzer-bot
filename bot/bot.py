from os import getenv

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from bot.routes.start import start
from bot.routes.news import news
from bot.routes.topics import topics


TOKEN = getenv('BOT_TOKEN')
bot = Bot(token=TOKEN,
          default=DefaultBotProperties(parse_mode=ParseMode.HTML, link_preview_is_disabled=True))


dp = Dispatcher()
dp.include_router(start)
dp.include_router(news)
dp.include_router(topics)