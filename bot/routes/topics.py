from aiogram import Router, F
from aiogram.types import Message, InlineKeyboardButton, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from bot.states import MainStates
from bot.commands import savetopic_command, deletetopic_command

from database import create_session
from database.classes import User, Topic


topics = Router()

@topics.message(Command(savetopic_command))
async def command_savetopic_handler(message: Message, state=FSMContext) -> None:
    await state.update_data(command = savetopic_command)
    await state.set_state(MainStates.waiting_for_topic)

    await message.answer('Напишите тему, чтобы я ее сохранил.')


@topics.message(Command(deletetopic_command))
async def command_deletetopic_handler(message: Message, state=FSMContext) -> None:
    await state.update_data(command = deletetopic_command)
    await state.set_state(MainStates.waiting_for_topic)

    await message.answer('Выбери тему, которую хочешь удалить.')
    await send_topics_list(message)


@topics.message(MainStates.waiting_for_topic, F.text)
async def handle_topic_message(message: Message, state: FSMContext) -> None:
    from bot.routes.news import process_topic

    data = await state.get_data()
    command = data['command']
    
    match command.command:
        case 'findnews':
            await process_topic(message=message, topic=message.text, state=state)
        case 'analyzenews':
            await process_topic(message=message, topic=message.text, state=state)
        case 'savetopic':
            save_topic(topic_str=message.text, user_id=message.from_user.id)

    await state.clear()


async def send_topics_list(message: Message, user_id: int) -> None:
    builder = InlineKeyboardBuilder()
    session = create_session()

    user = session.query(User).filter(User.id == user_id).first()
    topics = user.topics

    for i in range(len(topics)):
        builder.row(InlineKeyboardButton(text=f'{i + 1}. {topics[i].title}', callback_data=f'topic_{topics[i].id}'))

    session.close()

    await message.answer(text='Сохраненные темы:', reply_markup=builder.as_markup())



@topics.callback_query(F.data.startswith('topic_'))
async def callback_topic(callback: CallbackQuery, state: FSMContext) -> None:
    from bot.routes.news import process_topic

    await callback.answer()

    st = await state.get_state()
    if st is None:
        return

    data = callback.data.split('_')
    state_data = await state.get_data()
    topic_id = data[1]
    command = state_data['command']

    session = create_session()
    topic = session.query(Topic).filter(Topic.id == topic_id).first()
    
    match command.command:
        case 'findnews':
            await process_topic(message=callback, topic=topic.title, state=state)
        case 'analyzenews':
            await process_topic(message=callback, topic=topic.title, state=state)
        case 'deletetopic':
            delete_topic(topic_id)

    session.close()
    await state.clear()

def save_topic(topic_str: str, user_id: int) -> None:
    session = create_session()

    user = session.query(User).filter(User.id == user_id).first()
    user.topics.append(Topic(title=topic_str))

    session.commit()
    session.close()


def delete_topic(topic_id: int) -> None:
    session = create_session()

    topic = session.query(Topic).filter(Topic.id == topic_id).first()
    session.delete(topic)

    session.commit()
    session.close()
