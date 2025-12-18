from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, InputMediaPhoto
from loguru import logger

from products.keyboards.product_keyboards import get_products_keyboard
from products.keyboards.empty_products_keyboards import get_empty_products_keyboard
from products.queries.product import get_user_approved_products
from products.states.view_products import ViewProducts
from core.utils.formater import format_price
from core.utils.paginator import Paginator
from core.utils.status import get_status_text

router = Router()


@router.callback_query(F.data == "view_products")
async def show_products(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    products = await get_user_approved_products(callback.from_user.id)

    logger.info(f"User {callback.from_user.id} viewed products: {len(products)} found")

    if not products:
        await callback.message.edit_text(
            "📦 <b>У вас пока нет одобренных товаров</b>\n\n"
            "Добавьте товар и дождитесь одобрения администратором!",
            reply_markup=get_empty_products_keyboard(),
        )
        return

    paginator = Paginator(products, page=1, per_page=1)
    await state.update_data(paginator=paginator)
    await state.set_state(ViewProducts.viewing)
    await show_product_card(callback, paginator)


async def show_product_card(callback: CallbackQuery, paginator: Paginator) -> None:
    current_products = paginator.get_page()
    if not current_products:
        return

    product = current_products[0]
    text = (
        f"📦 <b>{product.title}</b>\n\n"
        f"📄 <b>Описание:</b>\n{product.description}\n\n"
        f"💰 <b>Цена:</b> {format_price(product.price)}\n"
        f"📅 <b>Создано:</b> {product.created_at.strftime('%d.%m.%Y %H:%M')}\n"
        f"📊 <b>Статус:</b> {get_status_text(product.status.value)}\n\n"
        f"<i>Товар {paginator.page} из {paginator.pages}</i>"
    )

    keyboard = get_products_keyboard(paginator)

    if product.photo:
        try:
            if callback.message.photo:
                await callback.message.edit_media(
                    media=InputMediaPhoto(media=product.photo, caption=text, parse_mode="HTML"),
                    reply_markup=keyboard,
                )
            else:
                await callback.message.delete()
                await callback.bot.send_photo(
                    chat_id=callback.message.chat.id,
                    photo=product.photo,
                    caption=text,
                    reply_markup=keyboard,
                    parse_mode="HTML",
                )
        except Exception:
            await callback.message.edit_text(
                text + "\n\n❌ <i>Ошибка загрузки фото</i>",
                reply_markup=keyboard,
                parse_mode="HTML",
            )
    else:
        if callback.message.photo:
            await callback.message.delete()
            await callback.bot.send_message(
                chat_id=callback.message.chat.id,
                text=text,
                reply_markup=keyboard,
                parse_mode="HTML",
            )
        else:
            await callback.message.edit_text(text, reply_markup=keyboard, parse_mode="HTML")
