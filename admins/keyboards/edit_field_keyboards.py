from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def get_edit_field_keyboard() -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📝 Название"), KeyboardButton(text="📄 Описание")],
            [KeyboardButton(text="💰 Цена"), KeyboardButton(text="🖼 Фото")],
            [KeyboardButton(text="❌ Отмена")],
        ],
        resize_keyboard=True,
    )
    return keyboard