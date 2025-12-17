from aiogram.filters import CommandStart
from aiogram import Router
from aiogram.types import Message

from database.operations.users import save_user

start = Router()

@start.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    text = 'Привет! Напиши мне обсуждаемую тему, а я скажу тебе насколько она популярна и позитивна в текущее время.'
    save_user(message.from_user.id)
    await message.answer(text)
