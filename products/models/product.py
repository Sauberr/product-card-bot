from datetime import UTC, datetime
from decimal import Decimal
from enum import Enum
from typing import Optional

from sqlalchemy import DECIMAL, BigInteger, DateTime, String, Text, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, validates

from core.constants import ProductLimits
from core.mixin.int_id_pk import IdIntMixin
from core.models.base import Base


class ProductStatus(Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"


class Product(Base, IdIntMixin):
    __tablename__ = "products"

    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    price: Mapped[Decimal] = mapped_column(DECIMAL(10, 2), nullable=False, default=0)
    photo: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    status: Mapped[ProductStatus] = mapped_column(
        SQLEnum(ProductStatus), default=ProductStatus.PENDING, nullable=False
    )
    user_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.now(UTC), nullable=False
    )

    @validates("title")
    def validate_title(self, key, value):
        value = value.strip()
        if not (
            ProductLimits.TITLE_MIN_LENGTH
            <= len(value)
            <= ProductLimits.TITLE_MAX_LENGTH
        ):
            raise ValueError(
                f"Название должно быть {ProductLimits.TITLE_MIN_LENGTH}-"
                f"{ProductLimits.TITLE_MAX_LENGTH} символов"
            )
        return value

    @validates("description")
    def validate_description(self, key, value):
        value = value.strip()
        if not (
            ProductLimits.DESCRIPTION_MIN_LENGTH
            <= len(value)
            <= ProductLimits.DESCRIPTION_MAX_LENGTH
        ):
            raise ValueError(
                f"Описание должно быть {ProductLimits.DESCRIPTION_MIN_LENGTH}-"
                f"{ProductLimits.DESCRIPTION_MAX_LENGTH} символов"
            )
        return value

    @validates("price")
    def validate_price(self, key, value):
        if not (ProductLimits.PRICE_MIN < value <= ProductLimits.PRICE_MAX):
            raise ValueError(
                f"Цена должна быть больше {ProductLimits.PRICE_MIN} и не больше {ProductLimits.PRICE_MAX}"
            )
        return value

    def __str__(self):
        return f"Product: {self.title} ({self.id})"