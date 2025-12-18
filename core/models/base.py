from sqlalchemy import MetaData
from sqlalchemy.orm import DeclarativeBase, declared_attr

from app_config import db_config
from core.utils.case_converter import camel_case_to_snake_case


class Base(DeclarativeBase):
    __abstract__ = True

    metadata = MetaData(
        naming_convention=db_config.NAMING_CONVERSATION
    )

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return f"{camel_case_to_snake_case(cls.__name__)}s"