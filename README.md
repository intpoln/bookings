# 🏨 Hotel Booking API

REST API сервис для бронирования отелей, построенный на современном стеке Python с использованием паттернов Repository и DataMapper.

![Python](https://img.shields.io/badge/Python-3.13-blue?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.124-009688?logo=fastapi&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Latest-336791?logo=postgresql&logoColor=white)
![Redis](https://img.shields.io/badge/Redis-Latest-DC382D?logo=redis&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?logo=docker&logoColor=white)

## 📋 Содержание

- [Особенности](#-особенности)
- [Технологический стек](#-технологический-стек)
- [Архитектура](#-архитектура)
- [Установка и запуск](#-установка-и-запуск)
- [API Endpoints](#-api-endpoints)
- [Структура проекта](#-структура-проекта)
- [Тестирование](#-тестирование)

## ✨ Особенности

- 🔐 **JWT аутентификация** — безопасная авторизация через токены
- 🏨 **Управление отелями** — полный CRUD для отелей и номеров
- 📅 **Система бронирования** — бронирование номеров с проверкой доступности
- 🛋️ **Удобства номеров** — гибкая система удобств (facilities)
- 🖼️ **Загрузка изображений** — асинхронная обработка и ресайз через Celery
- ⚡ **Кэширование** — Redis для быстрых ответов
- 📊 **Фоновые задачи** — Celery + Celery Beat для отложенных операций
- 🐳 **Docker-ready** — полная контейнеризация приложения
- ✅ **Тесты** — unit и integration тесты

## 🛠 Технологический стек

| Категория | Технология |
|-----------|------------|
| **Backend Framework** | FastAPI |
| **ORM** | SQLAlchemy 2.0 (async) |
| **База данных** | PostgreSQL + asyncpg |
| **Кэширование** | Redis + fastapi-cache2 |
| **Фоновые задачи** | Celery + Celery Beat |
| **Миграции БД** | Alembic |
| **Аутентификация** | JWT (PyJWT) + bcrypt |
| **Валидация** | Pydantic v2 |
| **Обработка изображений** | Pillow |
| **Тестирование** | Pytest + pytest-asyncio + HTTPX |
| **Контейнеризация** | Docker + Docker Compose |
| **Пакетный менеджер** | uv |

## 🏗 Архитектура

Проект построен с использованием **слоистой архитектуры** и паттернов:

```
┌─────────────────────────────────────────────────────────┐
│                      API Layer                          │
│            (FastAPI Routers & Dependencies)             │
├─────────────────────────────────────────────────────────┤
│                    Service Layer                        │
│              (Business Logic & Validation)              │
├─────────────────────────────────────────────────────────┤
│                  Repository Layer                       │
│      (Data Access with Repository Pattern)              │
├─────────────────────────────────────────────────────────┤
│                   DataMapper Layer                      │
│         (ORM Models ↔ Domain Entities)                  │
├─────────────────────────────────────────────────────────┤
│                   Database Layer                        │
│            (PostgreSQL + SQLAlchemy Async)              │
└─────────────────────────────────────────────────────────┘
```

### Паттерны

- **Repository Pattern** — абстракция доступа к данным, позволяющая легко заменить источник данных
- **DataMapper Pattern** — преобразование между ORM-моделями и Pydantic-схемами
- **Dependency Injection** — через FastAPI `Depends` для управления зависимостями
- **Unit of Work** — через `DBManager` для транзакционности операций

## 🚀 Установка и запуск

### Через Docker Compose (рекомендуется)

1. **Клонируйте репозиторий:**
```bash
git clone https://github.com/intpoln/booking-api.git
cd booking-api
```

2. **Создайте файл `.env-docker-compose`:**
```env
MODE=DEV

DB_HOST=postgres
DB_PORT=5432
DB_USER=postgres
DB_PASS=postgres
DB_NAME=booking

REDIS_HOST=redis
REDIS_PORT=6379

JWT_SECRET_KEY=your-super-secret-key-change-in-production
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7
```

3. **Запустите контейнеры:**
```bash
docker-compose up --build
```

4. **Примените миграции:**
```bash
docker exec -it booking_back alembic upgrade head
```

API будет доступен по адресу: http://localhost:8000

### Локальная установка

1. **Установите зависимости:**
```bash
# С использованием uv (рекомендуется)
pip install uv
uv pip install -r requirements.txt

# Или через pip
pip install -r requirements.txt
```

2. **Создайте файл `.env`:**
```env
MODE=LOCAL

DB_HOST=localhost
DB_PORT=5432
DB_USER=postgres
DB_PASS=postgres
DB_NAME=booking

REDIS_HOST=localhost
REDIS_PORT=6379

JWT_SECRET_KEY=your-super-secret-key
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7
```

3. **Запустите PostgreSQL и Redis** (через Docker или локально)

4. **Примените миграции:**
```bash
alembic upgrade head
```

5. **Запустите приложение:**
```bash
python src/main.py
```

## 📡 API Endpoints

### Документация
После запуска доступна интерактивная документация:
- **Swagger UI:** http://localhost:8000/docs
- **OpenAPI JSON:** http://localhost:8000/openapi.json

### Авторизация и аутентификация `/auth`

| Метод | Endpoint | Описание |
|-------|----------|----------|
| POST | `/auth/register` | Регистрация нового пользователя |
| POST | `/auth/login` | Авторизация и получение access + refresh токенов |
| POST | `/auth/refresh` | Обновление токенов по refresh token |
| POST | `/auth/logout` | Выход из системы |
| GET | `/auth/me` | Получение информации о текущем пользователе |

### Отели `/hotels`

| Метод | Endpoint | Описание |
|-------|----------|----------|
| GET | `/hotels` | Список отелей с фильтрацией и пагинацией |
| POST | `/hotels` | Создание нового отеля |
| GET | `/hotels/{hotel_id}` | Информация об отеле |
| PUT | `/hotels/{hotel_id}` | Полное обновление отеля |
| PATCH | `/hotels/{hotel_id}` | Частичное обновление отеля |
| DELETE | `/hotels/{hotel_id}` | Удаление отеля |

### Номера `/hotels/{hotel_id}/rooms`

| Метод | Endpoint | Описание |
|-------|----------|----------|
| GET | `/hotels/{hotel_id}/rooms` | Список доступных номеров |
| POST | `/hotels/{hotel_id}/rooms` | Создание номера |
| GET | `/hotels/{hotel_id}/rooms/{room_id}` | Информация о номере |
| PUT | `/hotels/{hotel_id}/rooms/{room_id}` | Обновление номера |
| PATCH | `/hotels/{hotel_id}/rooms/{room_id}` | Частичное обновление |
| DELETE | `/hotels/{hotel_id}/rooms/{room_id}` | Удаление номера |

### Бронирования `/bookings`

| Метод | Endpoint | Описание |
|-------|----------|----------|
| GET | `/bookings` | Все бронирования |
| POST | `/bookings` | Создание бронирования |
| GET | `/bookings/me` | Бронирования текущего пользователя |

### Удобства `/facilities`

| Метод | Endpoint | Описание |
|-------|----------|----------|
| GET | `/facilities` | Список удобств |
| POST | `/facilities` | Создание удобства |

### Изображения `/images`

| Метод | Endpoint | Описание |
|-------|----------|----------|
| POST | `/images` | Загрузка изображения (async resize через Celery) |

## 📁 Структура проекта

```
bookings/
├── src/
│   ├── api/                    # API endpoints (routers)
│   │   ├── auth.py             # Авторизация
│   │   ├── bookings.py         # Бронирования
│   │   ├── dependencies.py     # FastAPI dependencies
│   │   ├── facilities.py       # Удобства
│   │   ├── hotels.py           # Отели
│   │   ├── images.py           # Изображения
│   │   └── rooms.py            # Номера
│   │
│   ├── models/                 # SQLAlchemy ORM модели
│   │   ├── bookings.py
│   │   ├── facilities.py
│   │   ├── hotels.py
│   │   ├── rooms.py
│   │   └── users.py
│   │
│   ├── repositories/           # Слой доступа к данным
│   │   ├── base.py             # Базовый репозиторий
│   │   ├── mappers/            # DataMapper'ы
│   │   └── ...
│   │
│   ├── schemas/                # Pydantic схемы
│   │   ├── bookings.py
│   │   ├── hotels.py
│   │   └── ...
│   │
│   ├── services/               # Бизнес-логика
│   │   ├── auth.py
│   │   ├── bookings.py
│   │   └── ...
│   │
│   ├── tasks/                  # Celery задачи
│   │   ├── celery_app.py
│   │   └── tasks.py
│   │
│   ├── migrations/             # Alembic миграции
│   ├── connectors/             # Подключения (Redis)
│   ├── utils/                  # Утилиты (DBManager)
│   ├── config.py               # Конфигурация
│   ├── database.py             # Настройка БД
│   └── main.py                 # Точка входа
│
├── tests/                      # Тесты
│   ├── integration_tests/
│   └── unit_tests/
│
├── docker-compose.yml
├── Dockerfile
├── pyproject.toml
├── requirements.txt
└── alembic.ini
```

## 🧪 Тестирование

```bash
# Запуск всех тестов
pytest

# Запуск с подробным выводом
pytest -v

# Только unit тесты
pytest tests/unit_tests/

# Только integration тесты
pytest tests/integration_tests/
```

## 🔧 Переменные окружения

| Переменная | Описание | Пример |
|------------|----------|--------|
| `MODE` | Режим работы (TEST/LOCAL/DEV/PROD) | `DEV` |
| `DB_HOST` | Хост PostgreSQL | `localhost` |
| `DB_PORT` | Порт PostgreSQL | `5432` |
| `DB_USER` | Пользователь БД | `postgres` |
| `DB_PASS` | Пароль БД | `postgres` |
| `DB_NAME` | Имя базы данных | `booking` |
| `REDIS_HOST` | Хост Redis | `localhost` |
| `REDIS_PORT` | Порт Redis | `6379` |
| `JWT_SECRET_KEY` | Секретный ключ для JWT | `your-secret-key` |
| `JWT_ALGORITHM` | Алгоритм JWT | `HS256` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Время жизни access токена (мин) | `15` |
| `REFRESH_TOKEN_EXPIRE_DAYS` | Время жизни refresh токена (дни) | `7` |
