Отлично — распишу **по пунктам** каждый модуль/папку проекта и что в них делать для быстрого старта. Сделаю так: сначала краткое назначение модуля, затем — файлы, которые нужно создать сразу, и краткие примеры/шаблоны (мини-код), которые можно вставить и запустить. Всё по-русски и по делу.

# 1. `app/main.py` — точка входа

**Назначение:** создаёт экземпляр FastAPI, подключает роутеры, статику, шаблоны, middlewares.

**Создать:**

* `app/main.py`

**Пример:**

```python
from fastapi import FastAPI
from app.api.router import api_router
from app.core.config import settings
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI(title=settings.PROJECT_NAME, version=settings.VERSION)

app.include_router(api_router, prefix="/api")

app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

@app.get("/")
def index(request):
    return templates.TemplateResponse("index.html", {"request": request})
```

# 2. `app/core/` — конфигурация и инициализация

**Назначение:** хранит настройки, секреты, логику инициализации приложения, security helpers.

**Файлы:**

* `config.py` — `pydantic.BaseSettings` с переменными окружения.
* `security.py` — хеширование паролей, JWT-утилиты.
* `logging_config.py` — настройка логирования.
* `init_app.py` *(опционально)* — функция для инициализации (event handlers, middleware).

**Пример `config.py`:**

```python
from pydantic import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "FastAPI App"
    VERSION: str = "0.1.0"
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    SQLALCHEMY_DATABASE_URL: str

    class Config:
        env_file = ".env"

settings = Settings()
```

**Пример `security.py` (минимум):**

```python
from passlib.context import CryptContext
from datetime import datetime, timedelta
import jwt
from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain, hashed) -> bool:
    return pwd_context.verify(plain, hashed)

def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm="HS256")
```

# 3. `app/db/` — подключение к БД и сессии

**Назначение:** engine, session, base, helper для зависимостей.

**Файлы:**

* `session.py` — создание `engine` и `SessionLocal`.
* `base.py` — `Base = declarative_base()` и импорт всех моделей в одном месте.
* `init_db.py` — опциональный скрипт создания таблиц (для dev).

**Пример `session.py`:**

```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

engine = create_engine(settings.SQLALCHEMY_DATABASE_URL, future=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
```

**Зависимость для роутов:**

```python
from fastapi import Depends
from app.db.session import SessionLocal

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

# 4. `app/models/` — SQLAlchemy ORM модели

**Назначение:** описать таблицы базы данных.

**Файлы/модели:**

* `user.py` — модель пользователя.
* `item.py` *(пример ресурса)*.

**Пример `user.py`:**

```python
from sqlalchemy import Column, Integer, String, Boolean
from app.db.base import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
```

# 5. `app/schemas/` — Pydantic схемы (вход/выход)

**Назначение:** валидация request/response.

**Файлы:**

* `user.py` — `UserCreate`, `UserOut`, `UserInDB`.
* `token.py` — `Token`, `TokenData`.
* `item.py` — примеры.

**Пример `user.py`:**

```python
from pydantic import BaseModel, EmailStr

class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    password: str

class UserOut(UserBase):
    id: int
    is_active: bool

    class Config:
        orm_mode = True
```

# 6. `app/api/` — маршруты / endpoints

**Назначение:** хранит версии API и routers.

**Структура:**

* `router.py` — объединяет все routers (v1, v2).
* `v1/`

  * `auth.py` — `/register`, `/login`, `/refresh`.
  * `users.py` — `/users/` CRUD.
  * `items.py` — пример ресурса.

**Пример `api/v1/auth.py` (минимум):**

```python
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.user import UserCreate, UserOut
from app.db.session import get_db
from app.services.user_service import create_user, authenticate_user
from app.core.security import create_access_token

router = APIRouter()

@router.post("/register", response_model=UserOut)
def register(user_in: UserCreate, db: Session = Depends(get_db)):
    user = create_user(db, user_in)
    return user

@router.post("/login")
def login(form_data: dict, db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data["email"], form_data["password"])
    if not user:
        raise HTTPException(401, "Invalid credentials")
    token = create_access_token({"sub": user.email})
    return {"access_token": token, "token_type": "bearer"}
```

# 7. `app/services/` — бизнес-логика

**Назначение:** код, который не должен быть в роутинге — регистрация, авторизация, отправка писем.

**Файлы:**

* `user_service.py` — `create_user`, `get_user_by_email`, `authenticate_user`.
* `auth_service.py` — операции с токенами, refresh, проверка ролей.

**Пример `create_user`:**

```python
from app.models.user import User
from app.core.security import hash_password

def create_user(db, user_in):
    user = User(email=user_in.email, hashed_password=hash_password(user_in.password))
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
```

# 8. `app/utils/` — утилиты

**Назначение:** вспомогательные функции: email, валидации, генераторы паролей, форматирование дат.

**Файлы:**

* `email_sender.py`
* `password_utils.py`
* `time_utils.py`

# 9. `app/templates/` и `app/static/` — фронтенд-ресурсы

**Назначение:** если нужен сайт с HTML, храним Jinja2-шаблоны и статические файлы.

**Файлы:**

* `templates/base.html`, `index.html`, `login.html`, `profile.html`.
* `static/css/`, `static/js/`, `static/img/`.

# 10. `alembic/` — миграции

**Назначение:** управление схемой БД.

**Создать:**

* `alembic.ini` и папку `alembic/versions/`.
* Конфиг, чтобы ссылался на `app.db.base.Base.metadata`.

# 11. `tests/` — автоматические тесты

**Назначение:** тесты на endpoints, services и db.

**Файлы:**

* `tests/conftest.py` — фикстуры (тестовый client, тестовая БД).
* `tests/test_auth.py`, `tests/test_users.py`.

**Пример (pytest):**

```python
def test_register(client):
    resp = client.post("/api/v1/auth/register", json={"email":"a@b.com","password":"pwd"})
    assert resp.status_code == 200
    assert resp.json()["email"] == "a@b.com"
```

# 12. `Dockerfile` и `docker-compose.yml`

**Назначение:** контейнеризация приложения, БД (Postgres), миграции.

**Советы:**

* Один сервис `web` с uvicorn/gunicorn.
* Сервис `db` — Postgres.
* Запустить миграции в entrypoint.

# 13. `.env` — переменные окружения

**Минимум переменных:**

```
SECRET_KEY=...
SQLALCHEMY_DATABASE_URL=postgresql://user:pass@db:5432/app
ACCESS_TOKEN_EXPIRE_MINUTES=60
PROJECT_NAME=FastAPI App
VERSION=0.1.0
```

# 14. `requirements.txt` (или `pyproject.toml`)

**Рекомендуемые пакеты:**

```
fastapi
uvicorn[standard]
sqlalchemy
alembic
pydantic
psycopg2-binary
python-jose  # или pyjwt
passlib[bcrypt]
jinja2
pytest
httpx
python-dotenv
```

# 15. `README.md` и скрипты для удобства

**README:** как запускать, переменные окружения, примеры запросов.
**scripts/** — `start.sh`, `migrate.sh`, `test.sh`.

# 16. `app/core/deps.py` — зависимости общие

**Назначение:** `get_current_user`, `get_current_active_user`, `get_db` — в одном месте для переиспользования.

**Пример `get_current_user`:**

```python
from fastapi import Depends, HTTPException
from app.core.security import decode_token

def get_current_user(token: str = Depends(oauth2_scheme), db=Depends(get_db)):
    payload = decode_token(token)
    email = payload.get("sub")
    if not email:
        raise HTTPException(401, "Invalid token")
    user = get_user_by_email(db, email)
    return user
```

# 17. Права/роли и админка

**Реализация:** поле `is_superuser` или `roles` в модели User + dependency `require_admin`.

**Опции админки:**

* Быстрая интеграция: `sqladmin` или `fastapi-admin`.

# 18. Логирование, мониторинг и CORS

**Логирование:** `logging_config.py` для настройки handlers.
**CORS:** `app.add_middleware(CORSMiddleware, ...)`.
**Monitoring:** добавь endpoints health (`/health`) и metrics (Prometheus) при надобности.

# 19. План действий — первые шаги (чеклист)

1. Создать структуру папок и файлы (см. выше).
2. Написать `config.py` и `.env`.
3. Настроить `db/session.py` и простую модель `User`.
4. Сделать `schemas` и `services.create_user`.
5. Сделать `api/v1/auth.py` с `/register` и `/login`.
6. Запустить приложение (uvicorn) и проверить регистрация/вход.
7. Добавить Alembic и базовые миграции.
8. Добавить тесты и CI (GitHub Actions) — базовый pipeline: lint → test → build.

# 20. Полезные советы и «антишаблоны»

* **Разделяй бизнес-логику от роутов** — роуты только диспетчеры.
* **Используй зависимости (Depends)** для аутентификации/базы.
* **Не держи секреты в коде** — `.env` + CI secrets.
* **Пиши тесты сразу** для критичных путей (auth, CRUD).
* **Форматируй** код (black, isort) и добавь pre-commit.
