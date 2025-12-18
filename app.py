import asyncio

import betterlogging as bt
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from betterlogging import logging
from dotenv import load_dotenv

from app_config import env_config
from core.database.db_helper import db_helper
from admins.handlers import router as admin_router
from products.handlers import router as product_router
from core.handlers.start import router as start_router
from core.models import Base

load_dotenv()

bot = Bot(
    token=env_config.TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)

bot.my_admins_list = [int(x.strip()) for x in env_config.ADMIN_LIST.split(",") if x.strip()]

dp = Dispatcher()


async def create_tables():
    async with db_helper.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("\033[32mТаблицы проверены/созданы")


async def on_startup() -> None:
    await create_tables()
    print("\033[32mБот запущен!")


async def on_shutdown() -> None:
    await db_helper.dispose()
    print("\033[31mБот остановлен!")


async def main() -> None:
    bt.basic_colorized_config(level=logging.INFO)

    dp.include_router(start_router)
    dp.include_router(admin_router)
    dp.include_router(product_router)

    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\033[31mБот остановлен пользователем!")