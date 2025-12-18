from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, InputMediaPhoto, Message
from loguru import logger

from admins.filters.is_admin import IsAdmin
from admins.keyboards.admin_keyboards import get_admin_menu_keyboard
from admins.keyboards.moderation_keyboards import get_moderation_navigation_keyboard
from core.utils.formater import format_price
from core.utils.paginator import Paginator
from core.utils.status import get_status_text
from products.models.product import ProductStatus
from admins.states.moderation import ModerationState
from products.queries.product import (
    update_product_status,
    delete_product_by_id,
    get_all_products,
)

router = Router()


@router.callback_query(F.data == "admin_moderation", IsAdmin())
async def admin_moderation(callback: CallbackQuery, state: FSMContext) -> None:
    await callback.answer()

    products = await get_all_products()

    logger.info(f"Admin {callback.from_user.id} opened moderation: {len(products)} products")

    if not products:
        await callback.message.edit_text(
            "🛡️ <b>Модерация товаров</b>\n\n📭 Нет товаров",
            reply_markup=get_admin_menu_keyboard(),
        )
        return

    paginator = Paginator(products, page=1, per_page=1)
    await state.update_data(paginator=paginator)
    await state.set_state(ModerationState.viewing)

    await show_moderation_card(callback, paginator, callback.from_user.id)


async def show_moderation_card(
    callback_or_message: CallbackQuery | Message,
    paginator: Paginator,
    admin_id: int,
    edit_mode: bool = True,
) -> None:
    current_products = paginator.get_page()
    if not current_products:
        return

    product = current_products[0]

    text = (
        f"🛡️ <b>Модерация товара</b>\n\n"
        f"📦 <b>{product.title}</b>\n\n"
        f"📄 <b>Описание:</b>\n{product.description}\n\n"
        f"💰 <b>Цена:</b> {format_price(product.price)}\n"
        f"👤 <b>Автор:</b> <code>{product.user_id}</code>\n"
        f"📅 <b>Создано:</b> {product.created_at.strftime('%d.%m.%Y %H:%M')}\n"
        f"📊 <b>Статус:</b> {get_status_text(product.status.value)}\n\n"
        f"<i>Товар {paginator.page} из {paginator.pages}</i>"
    )

    keyboard = get_moderation_navigation_keyboard(
        product_id=product.id,
        admin_id=admin_id,
        status=product.status,
        has_previous=paginator.has_previous(),
        has_next=paginator.has_next(),
    )

    if isinstance(callback_or_message, CallbackQuery):
        message = callback_or_message.message
        bot = callback_or_message.bot
    else:
        message = callback_or_message
        bot = callback_or_message.bot

    if edit_mode and isinstance(callback_or_message, CallbackQuery):
        try:
            if product.photo:
                if hasattr(message, "photo") and message.photo:
                    await message.edit_media(
                        media=InputMediaPhoto(
                            media=product.photo, caption=text, parse_mode="HTML"
                        ),
                        reply_markup=keyboard,
                    )
                else:
                    await message.delete()
                    await bot.send_photo(
                        chat_id=message.chat.id,
                        photo=product.photo,
                        caption=text,
                        reply_markup=keyboard,
                        parse_mode="HTML",
                    )
            else:
                if hasattr(message, "photo") and message.photo:
                    await message.delete()
                    await bot.send_message(
                        chat_id=message.chat.id,
                        text=text,
                        reply_markup=keyboard,
                        parse_mode="HTML",
                    )
                else:
                    await message.edit_text(
                        text, reply_markup=keyboard, parse_mode="HTML"
                    )
        except Exception as e:
            logger.error(f"Error displaying moderation card: {e}")
            try:
                await message.edit_text(
                    text + "\n\n❌ <i>Ошибка отображения</i>",
                    reply_markup=keyboard,
                    parse_mode="HTML",
                )
            except Exception:
                pass
    else:
        if product.photo:
            await bot.send_photo(
                chat_id=message.chat.id,
                photo=product.photo,
                caption=text,
                reply_markup=keyboard,
                parse_mode="HTML",
            )
        else:
            await bot.send_message(
                chat_id=message.chat.id,
                text=text,
                reply_markup=keyboard,
                parse_mode="HTML",
            )


@router.callback_query(F.data.startswith("approve_"), IsAdmin())
async def approve_product(callback: CallbackQuery, state: FSMContext):
    parts = callback.data.split("_")
    product_id = int(parts[1])

    await update_product_status(product_id, ProductStatus.APPROVED)
    logger.info(f"Admin {callback.from_user.id} APPROVED product ID: {product_id}")

    await callback.answer("✅ Товар одобрен и теперь доступен пользователям!", show_alert=True)

    updated_paginator = await refresh_paginator(state)
    if updated_paginator:
        await show_moderation_card(callback, updated_paginator, callback.from_user.id)
    else:
        await state.clear()
        await callback.message.edit_text(
            "🛡️ <b>Модерация товаров</b>\n\n📭 Нет товаров",
            reply_markup=get_admin_menu_keyboard(),
        )


@router.callback_query(F.data.startswith("reject_"), IsAdmin())
async def reject_product(callback: CallbackQuery, state: FSMContext):
    parts = callback.data.split("_")
    product_id = int(parts[1])

    await update_product_status(product_id, ProductStatus.REJECTED)
    logger.info(f"Admin {callback.from_user.id} REJECTED product ID: {product_id}")

    await callback.answer("❌ Товар отклонен и скрыт от пользователей!", show_alert=True)

    updated_paginator = await refresh_paginator(state)
    if updated_paginator:
        await show_moderation_card(callback, updated_paginator, callback.from_user.id)
    else:
        await state.clear()
        await callback.message.edit_text(
            "🛡️ <b>Модерация товаров</b>\n\n📭 Нет товаров",
            reply_markup=get_admin_menu_keyboard(),
        )


@router.callback_query(F.data.startswith("delete_"), IsAdmin())
async def delete_product(callback: CallbackQuery, state: FSMContext):
    parts = callback.data.split("_")
    product_id = int(parts[1])

    await delete_product_by_id(product_id)
    logger.warning(f"Admin {callback.from_user.id} DELETED product ID: {product_id}")

    await callback.answer("🗑 Товар полностью удален из системы!", show_alert=True)

    updated_paginator = await refresh_paginator(state)
    if updated_paginator:
        await show_moderation_card(callback, updated_paginator, callback.from_user.id)
    else:
        await state.clear()
        await callback.message.edit_text(
            "🛡️ <b>Модерация товаров</b>\n\n📭 Нет товаров",
            reply_markup=get_admin_menu_keyboard(),
        )


async def refresh_paginator(state: FSMContext) -> Paginator | None:
    data = await state.get_data()
    paginator = data.get("paginator")

    if not paginator:
        return None

    current_page = paginator.page
    fresh_products = await get_all_products()

    if not fresh_products:
        return None

    new_paginator = Paginator(
        fresh_products, page=min(current_page, len(fresh_products)), per_page=1
    )
    await state.update_data(paginator=new_paginator)

    return new_paginator
