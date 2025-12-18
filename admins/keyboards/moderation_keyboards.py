from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from products.models.product import ProductStatus


def get_moderation_navigation_keyboard(
    product_id: int,
    admin_id: int,
    status: ProductStatus,
    has_previous: bool,
    has_next: bool
) -> InlineKeyboardMarkup:
    buttons = []

    nav_buttons = []
    if has_previous:
        nav_buttons.append(
            InlineKeyboardButton(text="«", callback_data=f"mod_prev_{admin_id}")
        )
    if has_next:
        nav_buttons.append(
            InlineKeyboardButton(text="»", callback_data=f"mod_next_{admin_id}")
        )

    if nav_buttons:
        buttons.append(nav_buttons)

    if status == ProductStatus.PENDING:
        action_buttons = [
            InlineKeyboardButton(
                text="✅ Одобрить", callback_data=f"approve_{product_id}_{admin_id}"
            ),
            InlineKeyboardButton(
                text="❌ Отклонить", callback_data=f"reject_{product_id}_{admin_id}"
            ),
        ]
        buttons.append(action_buttons)

    elif status == ProductStatus.APPROVED:
        action_buttons = [
            InlineKeyboardButton(
                text="❌ Отклонить", callback_data=f"reject_{product_id}_{admin_id}"
            ),
            InlineKeyboardButton(
                text="🗑 Удалить", callback_data=f"delete_{product_id}_{admin_id}"
            ),
        ]
        buttons.append(action_buttons)

    elif status == ProductStatus.REJECTED:
        action_buttons = [
            InlineKeyboardButton(
                text="✅ Одобрить", callback_data=f"approve_{product_id}_{admin_id}"
            ),
            InlineKeyboardButton(
                text="🗑 Удалить", callback_data=f"delete_{product_id}_{admin_id}"
            ),
        ]
        buttons.append(action_buttons)

    buttons.append(
        [
            InlineKeyboardButton(
                text="✏️ Изменить", callback_data=f"edit_{product_id}_{admin_id}"
            )
        ]
    )

    buttons.append([InlineKeyboardButton(text="🔙 Назад", callback_data="admin_menu")])

    return InlineKeyboardMarkup(inline_keyboard=buttons)

