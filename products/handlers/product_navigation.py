from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from loguru import logger

from products.handlers.view_products import show_product_card
from app_config import env_config
from core.keyboards.start_keyboard import get_main_menu_keyboard

router = Router()


@router.callback_query(F.data == "prev_product")
async def prev_product(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    data = await state.get_data()
    paginator = data.get("paginator")

    if not paginator:
        await callback.answer("❌ Ошибка: пагинатор не найден")
        return

    if paginator.has_previous():
        paginator.get_previous()
        await state.update_data(paginator=paginator)
        logger.debug(f"User {callback.from_user.id} -> previous product (page {paginator.page})")
        await show_product_card(callback, paginator)


@router.callback_query(F.data == "next_product")
async def next_product(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    data = await state.get_data()
    paginator = data.get("paginator")

    if not paginator:
        await callback.answer("❌ Ошибка: пагинатор не найден")
        return

    if paginator.has_next():
        paginator.get_next()
        await state.update_data(paginator=paginator)
        logger.debug(f"User {callback.from_user.id} -> next product (page {paginator.page})")
        await show_product_card(callback, paginator)


@router.callback_query(F.data == "back_to_menu")
async def back_to_menu(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.clear()

    is_admin = str(callback.from_user.id) in env_config.ADMIN_LIST

    await callback.message.delete()
    await callback.bot.send_message(
        chat_id=callback.message.chat.id,
        text="🏪 <b>Добро пожаловать в магазин!</b>\n\nВыберите действие:",
        reply_markup=get_main_menu_keyboard(is_admin),
        parse_mode="HTML"
    )
