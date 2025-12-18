from aiogram.fsm.state import StatesGroup, State

class EditProduct(StatesGroup):
    waiting_new_value: str = State()