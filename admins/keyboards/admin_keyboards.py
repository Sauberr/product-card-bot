from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def get_admin_menu_keyboard() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🛡️ Модерация", callback_data="admin_moderation")],
            [InlineKeyboardButton(text="📊 Статистика", callback_data="admin_statistics")],
            [InlineKeyboardButton(text="◀️ Назад", callback_data="back_to_main")]
        ]
    )
    return keyboard