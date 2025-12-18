from aiogram import Router

from .admin_menu import router as menu_router
from .moderation import router as moderation_router
from .moderation_navigation import router as navigation_router
from .statistics import router as stats_router

router = Router()
router.include_router(menu_router)
router.include_router(moderation_router)
router.include_router(navigation_router)
router.include_router(stats_router)

__all__ = ["router"]
