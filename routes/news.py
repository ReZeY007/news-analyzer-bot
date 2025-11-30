from aiogram import Router
from aiogram.types import Message

from ai.ai import ai_request

news = Router()

@news.message()
async def echo_handler(message: Message) -> None:
    try:
        answer = await ai_request(message.text)
        await message.answer(answer)
    except TypeError as e:
        await message.answer("Error!")  
