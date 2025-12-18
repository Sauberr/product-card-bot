from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from core.utils.paginator import Paginator


def get_products_keyboard(paginator: Paginator) -> InlineKeyboardMarkup:
    buttons = []

    nav_row = []
    if paginator.has_previous():
        nav_row.append(
            InlineKeyboardButton(text="⬅️ Назад", callback_data="prev_product")
        )
    if paginator.has_next():
        nav_row.append(
            InlineKeyboardButton(text="Вперёд ➡️", callback_data="next_product")
        )

    if nav_row:
        buttons.append(nav_row)

    buttons.append(
        [InlineKeyboardButton(text="🏠 Главное меню", callback_data="back_to_menu")]
    )

    return InlineKeyboardMarkup(inline_keyboard=buttons)
