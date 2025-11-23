from aiogram import Router
from aiogram.types import Message

news = Router()

@news.message()
async def echo_handler(message: Message) -> None:
    try:
        await message.answer("Nothing is done for now")
    except TypeError:
        await message.answer("Error!")  
