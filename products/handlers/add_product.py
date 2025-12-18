from decimal import Decimal, InvalidOperation
from aiogram import Router, F
from aiogram.filters import StateFilter, Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery
from loguru import logger

from app_config import env_config
from core.constants import ProductLimits
from products.queries.product import create_product
from products.states.add_product import AddProduct
from core.keyboards.start_keyboard import get_main_menu_keyboard
from core.utils.status import get_status_text

router = Router()


@router.callback_query(F.data == "add_product")
async def start_add_product(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    logger.info(f"User {callback.from_user.id} started adding product")
    await callback.message.answer(
        "📝 <b>Добавление товара</b>\n\n"
        "Введите название товара (4-100 символов):\n\n"
        "<i>Используйте /cancel для отмены или /back для возврата назад</i>",
        reply_markup=ReplyKeyboardRemove(),
    )
    await state.set_state(AddProduct.title)


@router.message(StateFilter("*"), Command("cancel"))
async def cancel_handler(message: Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state and current_state.startswith("AddProduct"):
        await state.clear()
        logger.info(f"User {message.from_user.id} cancelled product adding")
        is_admin = str(message.from_user.id) in env_config.ADMIN_LIST
        await message.answer(
            "❌ Добавление товара отменено",
            reply_markup=get_main_menu_keyboard(is_admin),
        )
    else:
        await message.answer("❗ Нет активного процесса для отмены")


@router.message(StateFilter("*"), Command("back"))
async def back_step_handler(message: Message, state: FSMContext):
    current_state = await state.get_state()
    if not current_state or not current_state.startswith("AddProduct"):
        await message.answer("❗ Нет активного процесса")
        return

    states_order = [AddProduct.title, AddProduct.description, AddProduct.price, AddProduct.photo]
    current_index = None
    for i, state_obj in enumerate(states_order):
        if state_obj.state == current_state:
            current_index = i
            break

    if current_index is None or current_index == 0:
        await message.answer("❗ Это первый шаг, вернуться некуда")
        return

    previous_state = states_order[current_index - 1]
    await state.set_state(previous_state)

    messages = {
        AddProduct.title: "📝 Введите название товара (4-100 символов):",
        AddProduct.description: "📄 Введите описание товара (10-1000 символов):",
        AddProduct.price: "💰 Введите цену товара (число больше 0):",
    }
    await message.answer(messages[previous_state])


@router.message(AddProduct.title, F.text)
async def add_title(message: Message, state: FSMContext):
    title = message.text.strip()
    if not (ProductLimits.TITLE_MIN_LENGTH <= len(title) <= ProductLimits.TITLE_MAX_LENGTH):
        await message.answer(
            f"❌ <b>Ошибка!</b>\n\nНазвание должно содержать от {ProductLimits.TITLE_MIN_LENGTH} "
            f"до {ProductLimits.TITLE_MAX_LENGTH} символов.\nПопробуйте еще раз:"
        )
        return

    await state.update_data(title=title)
    await message.answer("📄 <b>Отлично!</b>\n\nТеперь введите описание товара (10-1000 символов):")
    await state.set_state(AddProduct.description)


@router.message(AddProduct.title)
async def title_error(message: Message):
    await message.answer("❌ <b>Неверный формат!</b>\n\nОтправьте текстовое сообщение с названием товара")


@router.message(AddProduct.description, F.text)
async def add_description(message: Message, state: FSMContext):
    description = message.text.strip()
    if not (ProductLimits.DESCRIPTION_MIN_LENGTH <= len(description) <= ProductLimits.DESCRIPTION_MAX_LENGTH):
        await message.answer(
            f"❌ <b>Ошибка!</b>\n\nОписание должно содержать от {ProductLimits.DESCRIPTION_MIN_LENGTH} "
            f"до {ProductLimits.DESCRIPTION_MAX_LENGTH} символов.\nПопробуйте еще раз:"
        )
        return

    await state.update_data(description=description)
    await message.answer("💰 <b>Супер!</b>\n\nТеперь введите цену товара (число больше 0):")
    await state.set_state(AddProduct.price)


@router.message(AddProduct.description)
async def description_error(message: Message):
    await message.answer("❌ <b>Неверный формат!</b>\n\nОтправьте текстовое сообщение с описанием товара")


@router.message(AddProduct.price, F.text)
async def add_price(message: Message, state: FSMContext):
    try:
        price = Decimal(message.text.replace(",", "."))
        if price <= 0:
            raise ValueError("Цена должна быть больше 0")
    except (InvalidOperation, ValueError):
        await message.answer(
            "❌ <b>Ошибка!</b>\n\nВведите корректную цену (число больше 0).\nНапример: 100 или 99.99"
        )
        return

    await state.update_data(price=price)
    await message.answer('📸 <b>Почти готово!</b>\n\nОтправьте фото товара или напишите "пропустить" если фото не нужно:')
    await state.set_state(AddProduct.photo)


@router.message(AddProduct.price)
async def price_error(message: Message):
    await message.answer("❌ <b>Неверный формат!</b>\n\nОтправьте число для цены товара")


@router.message(AddProduct.photo, F.photo)
async def add_photo(message: Message, state: FSMContext):
    photo_id = message.photo[-1].file_id
    await state.update_data(photo=photo_id)
    await save_product(message, state)


@router.message(AddProduct.photo, F.text.lower().in_(["пропустить", "skip", "нет"]))
async def skip_photo(message: Message, state: FSMContext):
    await state.update_data(photo=None)
    await save_product(message, state)


@router.message(AddProduct.photo)
async def photo_error(message: Message):
    await message.answer('❌ <b>Неверный формат!</b>\n\nОтправьте фото или напишите "пропустить"')


async def save_product(message: Message, state: FSMContext):
    try:
        data = await state.get_data()
        new_product = await create_product(
            title=data["title"],
            description=data["description"],
            price=data["price"],
            photo=data["photo"],
            user_id=message.from_user.id,
        )

        logger.info(f"User {message.from_user.id} created product: '{data['title']}' (ID: {new_product.id})")
        is_admin = str(message.from_user.id) in env_config.ADMIN_LIST

        await message.answer(
            f"✅ <b>Карточка товара отправлена на модерацию!</b>\n\n"
            f"📝 Название: {data['title']}\n"
            f"📄 Описание: {data['description']}\n"
            f"💰 Цена: {data['price']} руб.\n"
            f"📸 Фото: {'Есть' if data['photo'] else 'Нет'}\n\n"
            f"⏳ <b>Статус:</b> {get_status_text('pending')}\n\n"
            f"<i>Ваш товар будет рассмотрен администратором</i>",
            reply_markup=get_main_menu_keyboard(is_admin),
        )
    except Exception as e:
        logger.error(f"Error saving product: {e}")
        is_admin = str(message.from_user.id) in env_config.ADMIN_LIST
        await message.answer(
            "❌ <b>Ошибка при отправке товара на модерацию!</b>",
            reply_markup=get_main_menu_keyboard(is_admin),
        )
    finally:
        await state.clear()
