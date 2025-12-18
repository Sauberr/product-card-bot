from aiogram import Router

from .add_product import router as product_router
from .view_products import router as view_products_router
from .product_navigation import router as navigation_router
from .product_edit import router as edit_router

router = Router()
router.include_router(product_router)
router.include_router(edit_router)
router.include_router(view_products_router)
router.include_router(navigation_router)

__all__ = ["router"]
