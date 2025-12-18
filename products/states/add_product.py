from decimal import Decimal

from aiogram.fsm.state import State, StatesGroup


class AddProduct(StatesGroup):
    title: str = State()
    description: str = State()
    price: Decimal = State()
    photo: str = State()
