from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from loguru import logger

from admins.filters.is_admin import IsAdmin
from admins.handlers.moderation import show_moderation_card

router = Router()


@router.callback_query(F.data.startswith("mod_prev_"), IsAdmin())
async def mod_prev_product(callback: CallbackQuery, state: FSMContext):
    await callback.answer()

    data = await state.get_data()
    paginator = data.get("paginator")

    if not paginator:
        await callback.answer("❌ Ошибка: пагинатор не найден")
        return

    if paginator.has_previous():
        paginator.get_previous()
        await state.update_data(paginator=paginator)
        logger.debug(f"Admin {callback.from_user.id} -> previous product (page {paginator.page})")
        await show_moderation_card(callback, paginator, callback.from_user.id)


@router.callback_query(F.data.startswith("mod_next_"), IsAdmin())
async def mod_next_product(callback: CallbackQuery, state: FSMContext):
    await callback.answer()

    data = await state.get_data()
    paginator = data.get("paginator")

    if not paginator:
        await callback.answer("❌ Ошибка: пагинатор не найден")
        return

    if paginator.has_next():
        paginator.get_next()
        await state.update_data(paginator=paginator)
        logger.debug(f"Admin {callback.from_user.id} -> next product (page {paginator.page})")
        await show_moderation_card(callback, paginator, callback.from_user.id)
