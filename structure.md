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

Отличный вопрос 👍
Если ты хочешь **единый базовый шаблон FastAPI**, который подойдёт **для любого веб-проекта** — от небольшого сайта с HTML-страницами до REST-сервиса с API и авторизацией, — ниже приведена **универсальная архитектура**, проверенная на практике.

---

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
