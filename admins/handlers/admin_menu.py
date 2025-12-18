from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from loguru import logger

from admins.filters.is_admin import IsAdmin
from admins.keyboards.admin_keyboards import get_admin_menu_keyboard
from core.keyboards.start_keyboard import get_main_menu_keyboard

router = Router()


@router.message(Command("admin"), IsAdmin())
async def admin_command(message: Message):
    logger.info(f"Admin {message.from_user.id} accessed admin panel via command")
    await message.answer(
        "🛠 <b>Админ панель</b>\n\nВыберите действие:",
        reply_markup=get_admin_menu_keyboard(),
    )


@router.callback_query(F.data == "admin_menu", IsAdmin())
async def show_admin_menu(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.clear()
    logger.debug(f"Admin {callback.from_user.id} opened admin menu")
    await callback.message.answer(
        "🛠 <b>Админ панель</b>\n\nВыберите действие:",
        reply_markup=get_admin_menu_keyboard(),
    )


@router.callback_query(F.data == "back_to_main")
async def back_to_main_menu(callback: CallbackQuery, state: FSMContext, bot):
    await callback.answer()
    await state.clear()

    is_admin = callback.from_user.id in bot.my_admins_list

    logger.debug(f"Admin {callback.from_user.id} returned to main menu from admin panel")

    await callback.message.answer(
        "🏪 <b>Добро пожаловать в магазин!</b>\n\nВыберите действие:",
        reply_markup=get_main_menu_keyboard(is_admin),
    )
