from decimal import Decimal

from sqlalchemy import select

from core.database.db_helper import db_helper
from products.models.product import Product
from products.models.product import ProductStatus
from sqlalchemy import update, delete, func, case



async def create_product(title: str, description: str, price: Decimal, photo: str, user_id: int) -> Product:
    async with db_helper.session_factory() as session:
        new_product = Product(
            title=title,
            description=description,
            price=price,
            photo=photo,
            user_id=user_id,
            status=ProductStatus.PENDING,
        )
        session.add(new_product)
        await session.commit()
        await session.refresh(new_product)
        return new_product


async def get_all_products() -> list[Product]:
    async with db_helper.session_factory() as session:
        stmt = select(Product).order_by(Product.created_at.desc())
        result = await session.execute(stmt)
        return result.scalars().all()


async def update_product_status(product_id: int, status: ProductStatus) -> None:
    async with db_helper.session_factory() as session:
        stmt = update(Product).where(Product.id == product_id).values(status=status)
        await session.execute(stmt)
        await session.commit()


async def delete_product_by_id(product_id: int) -> None:
    async with db_helper.session_factory() as session:
        stmt = delete(Product).where(Product.id == product_id)
        await session.execute(stmt)
        await session.commit()


async def update_product_field(product_id: int, field: str, value) -> None:
    async with db_helper.session_factory() as session:
        stmt = update(Product).where(Product.id == product_id).values(**{field: value})
        await session.execute(stmt)
        await session.commit()


async def get_products_statistics() -> list:
    async with db_helper.session_factory() as session:
        stmt = select(
            Product.user_id,
            func.count(Product.id).label("total"),
            func.sum(
                case((Product.status == ProductStatus.APPROVED, 1), else_=0)
            ).label("approved"),
            func.sum(
                case((Product.status == ProductStatus.REJECTED, 1), else_=0)
            ).label("rejected"),
            func.sum(case((Product.status == ProductStatus.PENDING, 1), else_=0)).label(
                "pending"
            ),
        ).group_by(Product.user_id)

        result = await session.execute(stmt)
        return result.all()

async def get_user_approved_products(user_id: int) -> list[Product]:
    async with db_helper.session_factory() as session:
        stmt = select(Product).where(
            Product.user_id == user_id,
            Product.status == ProductStatus.APPROVED
        )
        result = await session.execute(stmt)
        return result.scalars().all()