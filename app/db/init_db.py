from app.db.session import engine
from app.db.base import Base

# Важно: загрузить модели до create_all
from app.models.user import User  # noqa: F401
from app.models.item import Item  # noqa: F401


def create_tables() -> None:
    Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    create_tables()


