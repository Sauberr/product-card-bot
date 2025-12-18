from aiogram import Router, F
from aiogram.types import CallbackQuery
from loguru import logger

from admins.filters.is_admin import IsAdmin
from admins.keyboards.admin_keyboards import get_admin_menu_keyboard
from products.queries.product import get_products_statistics

router = Router()


@router.callback_query(F.data == "admin_statistics", IsAdmin())
async def admin_statistics(callback: CallbackQuery):
    await callback.answer()

    stats = await get_products_statistics()

    logger.info(f"Admin {callback.from_user.id} viewed statistics")

    if not stats:
        await callback.message.edit_text(
            "📊 <b>Статистика</b>\n\n📭 Нет данных для отображения",
            reply_markup=get_admin_menu_keyboard(),
        )
        return

    text = "📊 <b>Статистика пользователей</b>\n\n"

    for stat in stats:
        text += (
            f"👤 <b>ID:</b> <code>{stat.user_id}</code>\n"
            f"📦 <b>Всего:</b> {stat.total}\n"
            f"✅ <b>Одобрено:</b> {stat.approved}\n"
            f"❌ <b>Отклонено:</b> {stat.rejected}\n"
            f"⏳ <b>На модерации:</b> {stat.pending}\n\n"
        )

    await callback.message.edit_text(text, reply_markup=get_admin_menu_keyboard())
