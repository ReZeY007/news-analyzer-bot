from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from bot.states import MainStates
from bot.keyboards import get_topics_list
from bot.commands import savetopic_command, deletetopic_command
from bot.routes.news import send_news, send_news_analyzis

from database import create_session
from database.classes import User, Topic
from database.operations.topics import save_topic, delete_topic

topics = Router()

@topics.message(Command(savetopic_command))
async def command_savetopic_handler(message: Message, state=FSMContext) -> None:
    await state.update_data(command = savetopic_command)
    await state.set_state(MainStates.waiting_for_topic)

    await message.answer('Напишите тему, чтобы я ее сохранил.')


@topics.message(Command(deletetopic_command))
async def command_deletetopic_handler(message: Message, state=FSMContext) -> None:
    await state.update_data(command = deletetopic_command)

    try:
        topics_list = get_topics_list(user_id=message.from_user.id)
        await message.answer('Выбери тему, которую хочешь удалить.')
        await message.answer(text='Сохраненные темы:', reply_markup=topics_list.as_markup())
    except Exception:
        await message.answer('У вас нет сохраненных тем.')
    
    await state.set_state(MainStates.waiting_for_topic)


@topics.message(MainStates.waiting_for_topic, F.text)
async def handle_topic_message(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    command = data['command']
    
    match command.command:
        case 'findnews':
            await send_news(message=message, topic=message.text)
        case 'analyzenews':
            await send_news_analyzis(message=message, topic=message.text)
        case 'savetopic':
            save_topic(topic_str=message.text, user_id=message.from_user.id)
            await message.answer(f'Тема <i><b>{message.text}</b></i> сохранена!')

    await state.clear()


@topics.callback_query(F.data.startswith('topic_'))
async def callback_topic(callback: CallbackQuery, state: FSMContext) -> None:
    await callback.answer()

    st = await state.get_state()
    if st != "MainStates:waiting_for_topic":
        return

    callback_data = callback.data.split('_')
    state_data = await state.get_data()
    topic_id = callback_data[1]
    command = state_data['command']

    session = create_session()
    topic = session.query(Topic).filter(Topic.id == topic_id).first()
    
    match command.command:
        case 'findnews':
            await send_news(message=callback.message, topic=topic.title)
            await callback.message.delete()
        case 'analyzenews':
            await send_news_analyzis(message=callback.message, topic=topic.title)
            await callback.message.delete()
        case 'deletetopic':
            delete_topic(topic_id)
            await callback.message.edit_text('Тема удалена!')

    session.close()
    await state.clear()
