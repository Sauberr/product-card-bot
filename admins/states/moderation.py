from aiogram.fsm.state import StatesGroup, State


class ModerationState(StatesGroup):
    viewing = State()
