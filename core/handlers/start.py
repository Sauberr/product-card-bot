from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from core.keyboards.start_keyboard import get_main_menu_keyboard

router = Router()


@router.message(CommandStart())
async def start_command(message: Message, bot) -> None:
    is_admin = message.from_user.id in bot.my_admins_list

    await message.answer(
        "🏪 <b>Добро пожаловать в магазин!</b>\n\nВыберите действие:",
        reply_markup=get_main_menu_keyboard(is_admin),
    )