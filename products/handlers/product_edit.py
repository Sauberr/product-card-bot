from decimal import Decimal, InvalidOperation

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message, ReplyKeyboardRemove
from loguru import logger

from admins.filters.is_admin import IsAdmin
from admins.keyboards.edit_field_keyboards import get_edit_field_keyboard
from core.constants import ProductLimits
from products.queries.product import update_product_field
from products.states.edit_product import EditProduct
from admins.states.moderation import ModerationState
from admins.handlers.moderation import show_moderation_card, refresh_paginator

router = Router()


@router.callback_query(F.data.startswith("edit_"), IsAdmin())
async def edit_product_menu(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    parts = callback.data.split("_")
    product_id = int(parts[1])

    logger.info(f"Admin {callback.from_user.id} started editing product ID: {product_id}")

    await state.update_data(product_id=product_id)

    await callback.message.answer(
        "✏️ <b>Редактирование товара</b>\n\nВыберите, что хотите изменить:",
        reply_markup=get_edit_field_keyboard(),
    )


@router.message(F.text.in_(["📝 Название", "📄 Описание", "💰 Цена", "🖼 Фото"]), IsAdmin())
async def choose_edit_field(message: Message, state: FSMContext):
    data = await state.get_data()

    if "product_id" not in data:
        await message.answer("❌ Ошибка: данные редактирования не найдены")
        return

    field_map = {
        "📝 Название": "title",
        "📄 Описание": "description",
        "💰 Цена": "price",
        "🖼 Фото": "photo",
    }

    field = field_map[message.text]
    await state.update_data(field=field)

    logger.debug(f"Admin {message.from_user.id} chose to edit field: {field}")

    await state.set_state(EditProduct.waiting_new_value)

    field_prompts = {
        "title": "✏️ Введите новое название товара (минимум 3 символа, максимум 100):",
        "description": "✏️ Введите новое описание товара (минимум 10 символов, максимум 1000):",
        "price": "✏️ Введите новую цену товара (число больше 0):",
        "photo": "📸 Отправьте новое фото или напишите 'пропустить' для удаления фото:",
    }

    await message.answer(field_prompts[field], reply_markup=ReplyKeyboardRemove())


@router.message(F.text == "❌ Отмена", IsAdmin())
async def cancel_edit(message: Message, state: FSMContext):
    data = await state.get_data()
    product_id = data.get("product_id", "unknown")

    logger.info(f"Admin {message.from_user.id} cancelled editing product ID: {product_id}")

    await state.set_state(ModerationState.viewing)

    await message.answer("❌ Редактирование отменено", reply_markup=ReplyKeyboardRemove())


@router.message(EditProduct.waiting_new_value, IsAdmin())
async def save_edit_value(message: Message, state: FSMContext):
    data = await state.get_data()

    if "product_id" not in data or "field" not in data:
        await message.answer("❌ Ошибка: данные редактирования не найдены")
        return

    product_id = data["product_id"]
    field = data["field"]
    new_value = None

    if field == "photo":
        if message.photo:
            new_value = message.photo[-1].file_id
        elif message.text and message.text.lower() in ["пропустить", "skip"]:
            new_value = None
        else:
            await message.answer(
                "❌ <b>Неверный формат!</b>\n\nОтправьте фото или напишите 'пропустить' для удаления фото"
            )
            return

    elif field == "price":
        try:
            new_value = Decimal(message.text.replace(",", "."))
            if new_value <= ProductLimits.PRICE_MIN:
                raise ValueError("Цена должна быть больше 0")
            if new_value > ProductLimits.PRICE_MAX:
                raise ValueError("Цена слишком большая")
        except (InvalidOperation, ValueError):
            await message.answer(
                f"❌ <b>Ошибка!</b>\n\nВведите корректную цену (от {ProductLimits.PRICE_MIN} "
                f"до {ProductLimits.PRICE_MAX}).\nНапример: 100 или 99.99"
            )
            return

    elif field == "title":
        if not message.text:
            await message.answer("❌ Название не может быть пустым")
            return

        new_value = message.text.strip()
        if len(new_value) < ProductLimits.TITLE_MIN_LENGTH:
            await message.answer(
                f"❌ <b>Название слишком короткое!</b>\n\nМинимальная длина: {ProductLimits.TITLE_MIN_LENGTH} символа"
            )
            return

        if len(new_value) > ProductLimits.TITLE_MAX_LENGTH:
            await message.answer(
                f"❌ <b>Название слишком длинное!</b>\n\nМаксимальная длина: {ProductLimits.TITLE_MAX_LENGTH} символов"
            )
            return

    elif field == "description":
        if not message.text:
            await message.answer("❌ Описание не может быть пустым")
            return

        new_value = message.text.strip()
        if len(new_value) < ProductLimits.DESCRIPTION_MIN_LENGTH:
            await message.answer(
                f"❌ <b>Описание слишком короткое!</b>\n\nМинимальная длина: {ProductLimits.DESCRIPTION_MIN_LENGTH} символов"
            )
            return

        if len(new_value) > ProductLimits.DESCRIPTION_MAX_LENGTH:
            await message.answer(
                f"❌ <b>Описание слишком длинное!</b>\n\nМаксимальная длина: {ProductLimits.DESCRIPTION_MAX_LENGTH} символов"
            )
            return

    await update_product_field(product_id, field, new_value)

    logger.info(f"Admin {message.from_user.id} updated product ID: {product_id}, field: {field}")

    field_names = {
        "title": "Название",
        "description": "Описание",
        "price": "Цена",
        "photo": "Фото",
    }

    await message.answer(
        f"✅ {field_names.get(field, field)} успешно изменено!",
        reply_markup=ReplyKeyboardRemove(),
    )

    updated_paginator = await refresh_paginator(state)
    if updated_paginator:
        await show_moderation_card(message, updated_paginator, message.from_user.id, edit_mode=False)
        await state.set_state(ModerationState.viewing)
    else:
        await state.clear()
        await message.answer("📭 Товаров для модерации не осталось")
