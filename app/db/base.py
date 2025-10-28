from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


# Импорт моделей перенесён в места вызова (например, init_db),
# чтобы избежать циклических импортов при старте приложения.


