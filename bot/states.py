from aiogram.fsm.state import StatesGroup, State


class MainStates(StatesGroup):
    waiting_for_topic = State()