from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_empty_products_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🔙 Назад", callback_data="back_to_menu")]
        ]
    )