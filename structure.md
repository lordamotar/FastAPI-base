
## 🧱 БАЗОВАЯ СТРУКТУРА ПРОЕКТА НА FastAPI

```
project_name/
│
├── app/
│   ├── main.py                  # Точка входа приложения
│   ├── __init__.py
│   │
│   ├── core/                    # Основные настройки и конфигурации
│   │   ├── config.py            # Настройки окружения (.env)
│   │   ├── security.py          # JWT, хеширование, авторизация
│   │   ├── logging_config.py    # Логирование
│   │   └── init_app.py          # Инициализация FastAPI, подключение роутов
│   │
│   ├── api/                     # Все эндпоинты (REST)
│   │   ├── deps.py              # Зависимости (Depends)
│   │   ├── v1/
│   │   │   ├── auth.py          # /login, /register, /refresh
│   │   │   ├── users.py         # /users
│   │   │   ├── items.py         # /items (пример)
│   │   │   └── __init__.py
│   │   └── router.py            # Объединение роутеров в API
│   │
│   ├── models/                  # SQLAlchemy модели
│   │   ├── user.py
│   │   ├── item.py
│   │   └── __init__.py
│   │
│   ├── schemas/                 # Pydantic-схемы
│   │   ├── user.py
│   │   ├── item.py
│   │   └── __init__.py
│   │
│   ├── db/                      # Работа с БД
│   │   ├── base.py              # Base = declarative_base()
│   │   ├── session.py           # SessionLocal и engine
│   │   └── init_db.py
│   │
│   ├── services/                # Бизнес-логика (вспомогательные функции)
│   │   ├── auth_service.py
│   │   ├── user_service.py
│   │   └── ...
│   │
│   ├── templates/               # HTML-шаблоны (если нужны страницы)
│   │   ├── base.html
│   │   ├── index.html
│   │   ├── login.html
│   │   └── profile.html
│   │
│   ├── static/                  # CSS, JS, изображения
│   │   ├── css/
│   │   ├── js/
│   │   └── images/
│   │
│   ├── tests/                   # Pytest-тесты
│   │   ├── test_auth.py
│   │   └── test_users.py
│   │
│   └── utils/                   # Общие утилиты (email, время, валидация и т.п.)
│       ├── email_sender.py
│       ├── password_utils.py
│       └── time_utils.py
│
├── alembic/                     # Миграции базы данных
│
├── .env                         # Переменные окружения (SECRET_KEY, DB_URL и т.д.)
├── requirements.txt             # Зависимости
├── docker-compose.yml           # (если нужно)
├── Dockerfile                   # (если нужно)
├── .gitignore
└── README.md
```

---

## ⚙️ КЛЮЧЕВЫЕ КОМПОНЕНТЫ

| Папка / файл         | Назначение                                                          |
| -------------------- | ------------------------------------------------------------------- |
| **core/config.py**   | Настройки проекта: читаются из `.env` через `pydantic.BaseSettings` |
| **core/security.py** | Авторизация: хеширование паролей, JWT токены                        |
| **db/session.py**    | Подключение к базе (PostgreSQL, SQLite и т.д.)                      |
| **api/router.py**    | Регистрирует все маршруты из `/api/v1`                              |
| **templates/**       | Шаблоны Jinja2, если нужны HTML страницы                            |
| **services/**        | Логика вне роутеров (например, регистрация, логин, CRUD)            |
| **schemas/**         | Pydantic-модели для запросов/ответов                                |
| **models/**          | SQLAlchemy ORM-модели                                               |
| **tests/**           | Тесты с использованием Pytest                                       |
| **utils/**           | Общие функции и хелперы                                             |

---

## 🔐 Минимальный набор функций для универсального старта

* ✅ Регистрация и авторизация пользователей (JWT)
* ✅ Роли (admin / user)
* ✅ CRUD-пример (например, “items”)
* ✅ Страница входа и главная (`login.html`, `index.html`)
* ✅ Документация Swagger (`/docs`)
* ✅ Поддержка CORS, статики и шаблонов
* ✅ Миграции через Alembic
* ✅ Возможность масштабировать API (v1, v2 и т.п.)

---

## 🧩 Технологии по умолчанию

| Компонент  | Инструмент                  |
| ---------- | --------------------------- |
| Framework  | **FastAPI**                 |
| ORM        | **SQLAlchemy**              |
| Auth       | **JWT + bcrypt**            |
| Templates  | **Jinja2**                  |
| Migrations | **Alembic**                 |
| Config     | **pydantic-settings**       |
| Testing    | **pytest**                  |
| Docs       | **Swagger / Redoc**         |
| Optional   | **Docker / Docker Compose** |


## 🔧 Преимущества такой структуры

* ✅ Подходит **для любого проекта** — API, сайта, админки, SaaS и т.п.
* ✅ Легко расширять без ломки логики
* ✅ Совместимо с async/await
* ✅ Продакшн-готовая архитектура
* ✅ Работает и в Docker, и без него

---

## 🚀 Быстрый старт (Windows 11, PowerShell)

### 1) Установки
- **Python** 3.11+ (`py -V`), **Git**, при желании **PostgreSQL** (или используйте SQLite).

### 2) Виртуальное окружение и зависимости
```powershell
cd C:\Workspace\python\FastAPI\Base
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 3) Создать .env (минимум)
```dotenv
APP_NAME=FastAPI Base
ENV=dev
SECRET_KEY=REPLACE_ME
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Один из вариантов БД:
# PostgreSQL (рекомендуется в проде)
DATABASE_URL=postgresql+psycopg://user:password@localhost:5432/app_db
# или SQLite для локалки (синхронный драйвер)
# DATABASE_URL=sqlite:///./app.db

CORS_ORIGINS=*
```
Сгенерировать ключ: 
```powershell
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

### 4) Миграции БД (Alembic)
- Если папка `alembic/` уже есть: создаём первую ревизию и применяем.
```powershell
# при необходимости укажем URL БД только в этой сессии
$env:DATABASE_URL = "postgresql+psycopg://user:password@localhost:5432/app_db"

alembic revision --autogenerate -m "init"
alembic upgrade head
```
- Если `alembic/` ещё нет:
```powershell
alembic init alembic
# затем настройте target_metadata и DATABASE_URL, после чего как выше
```

### 5) Запуск приложения
```powershell
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```
- Swagger: `http://localhost:8000/docs`
- Redoc: `http://localhost:8000/redoc`

### 6) Базовая проверка авторизации (пример)
- Регистрация пользователя (если роут `POST /api/v1/auth/register` реализован):
```powershell
curl -Method Post -Uri http://localhost:8000/api/v1/auth/register -Headers @{"Content-Type"="application/json"} -Body '{
  "email":"admin@example.com",
  "password":"admin123",
  "full_name":"Admin"
}'
```

---

## ☁️ Публикация в GitHub (как базовый шаблон)
```powershell
git init
git add .
git commit -m "feat: bootstrap FastAPI base"
git branch -M main

# замените USER/REPO на свои
git remote add origin https://github.com/USER/REPO.git
git push -u origin main
```
- Включите в репозитории кнопку "Use this template" (Settings → General → Template repository), чтобы переиспользовать.

---

## ♻️ Переиспользование как старт проекта

### Вариант A: через GitHub Template
- На странице шаблона нажмите "Use this template" → "Create a new repository" → назовите новый проект.
- Клонируйте новый репозиторий:
```powershell
git clone https://github.com/USER/NEW_REPO.git MyProject
cd .\MyProject
```
- Дальше повторите шаги 2–5.

### Вариант B: вручную из любого репо
```powershell
git clone https://github.com/USER/REPO.git MyProject
cd .\MyProject

# (опционально) оторвём историю, чтобы начать "с чистого листа"
Remove-Item -Recurse -Force .git
git init
git add .
git commit -m "chore: project init from base"
git branch -M main
```
- Затем повторите шаги 2–5 и добавьте новый origin при необходимости.

---

## 🐳 Опционально: Docker (если есть `Dockerfile`/`docker-compose.yml`)
```powershell
docker compose up -d --build
```
- Откройте `http://localhost:8000/docs`.

---

## ✅ Что настроено в базе
- **JWT авторизация**, **пользователи**, **роли**, **CRUD-пример**, статика, шаблоны, **Swagger**.
- Дальше добавляйте свои модели/схемы/роуты в `models/`, `schemas/`, `api/v1/` и бизнес-логику в `services/`.

---

## 🗺️ План разработки (по шагам)

1) Инициализация проекта
   - Создать репозиторий из шаблона (см. раздел «Публикация в GitHub / Переиспользование»)
   - Настроить `.env` под окружение (секрет, БД, CORS)
   - Запустить локально `uvicorn app.main:app --reload`

2) Конфигурация и инфраструктура
   - `app/core/config.py`: убедиться, что все нужные переменные читаются из `.env`
   - `app/core/logging_config.py`: включить формат логов, уровень из ENV
   - `app/api/router.py`: зарегистрировать базовые роутеры `v1`

3) База данных
   - `app/db/session.py`: проверить строку подключения `DATABASE_URL`
   - `app/db/base.py`: собрать все модели в метаданные
   - Инициализировать/обновить Alembic, выполнить `upgrade head`

4) Модели и схемы пользователей
   - `app/models/user.py`: модель пользователя (email уникальный, пароль хеш)
   - `app/schemas/user.py`: `UserCreate`, `UserRead`, `UserUpdate`
   - `app/services/user_service.py`: CRUD-операции

5) Авторизация и безопасность
   - `app/core/security.py`: хеширование паролей (bcrypt), JWT (access/refresh по желанию)
   - `app/api/v1/auth.py`: `POST /register`, `POST /login`, `POST /refresh`
   - Зависимость `get_current_user` в `app/api/deps.py`

6) Пользователи (CRUD и профиль)
   - `app/api/v1/users.py`: `GET /me`, `PATCH /me`, `GET /users` (admin), `GET /users/{id}`
   - Ролевые проверки (admin/user) через Depends

7) Примерный CRUD (items)
   - `app/models/item.py`, `app/schemas/item.py`
   - `app/api/v1/items.py`: `create/read/update/delete`, фильтрация, пагинация
   - Связь item → owner (ForeignKey на user)

8) Тестирование
   - Pytest фикстуры: тестовая БД, клиент
   - Тесты: auth, users, items, ролевые ограничения, валидация

9) Шаблоны/статика (опционально)
   - Включить Jinja2 (если нужны страницы), базовые шаблоны `templates/`
   - Подключить статику `static/`

10) Докеризация (опционально)
   - `Dockerfile`, `docker-compose.yml` (app + db)
   - ENV передавать через `.env`/секреты

11) Качество и автопроверки
   - Настроить `ruff/flake8`, `black`, `mypy` (если требуется)
   - GitHub Actions: формат, линт, тесты при PR

12) Деплой
   - Выбор среды: Docker на VPS, Fly.io, Render, Railway, Koyeb и т.д.
   - Миграции при деплое: `alembic upgrade head`
   - Настроить переменные окружения в проде

13) Масштабирование
   - Версионирование API: `api/v2`
   - Разделение сервисов, кеширование (Redis), rate limiting, мониторинг
