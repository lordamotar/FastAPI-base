from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


# Импортируйте модели здесь, чтобы Alembic видел метаданные
from app.models.user import User  # noqa: F401
from app.models.item import Item  # noqa: F401


