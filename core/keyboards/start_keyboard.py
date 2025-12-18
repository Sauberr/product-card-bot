from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def get_main_menu_keyboard(is_admin: bool = False) -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton(text="➕ Добавить товар", callback_data="add_product")],
        [
            InlineKeyboardButton(
                text="📦 Посмотреть карточки", callback_data="view_products"
            )
        ],
    ]
    if is_admin:
        buttons.append(
            [InlineKeyboardButton(text="🛠 Админ меню", callback_data="admin_menu")]
        )

    return InlineKeyboardMarkup(inline_keyboard=buttons)