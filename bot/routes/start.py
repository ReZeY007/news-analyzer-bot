from aiogram.filters import CommandStart
from aiogram import Router
from aiogram.types import Message

from database import create_session
from database.classes import User

start = Router()

@start.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    text = 'Привет! Напиши мне обсуждаемую тему, а я скажу тебе насколько она популярна и позитивна в текущее время.'
    save_user(message.from_user.id)
    await message.answer(text)


def save_user(user_id: int) -> None:
    session = create_session()
    usr = session.query(User).filter(User.id == user_id).first()
    
    if usr:
        session.close()
        return

    user = User(id = user_id)
    session.add(user)
    
    session.commit()
    session.close()