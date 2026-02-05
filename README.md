# Product card tg bot

Телеграм-бот для управления карточками товаров с системой модерации и админ-панелью.

## 🚀 Что умеет бот

### Для пользователей:
- **Добавление товаров** - создание карточек с названием, описанием, ценой и фото
- **Просмотр товаров** - пагинация по одобренным карточкам
- **Система модерации** - все товары проходят проверку администратором

### Для администраторов:
- **Модерация товаров** - одобрение/отклонение/удаление карточек
- **Редактирование товаров** - изменение любых атрибутов карточек
- **Статистика** - просмотр данных по пользователям и их товарам
- **Полный контроль** - управление всеми товарами в системе

## 🛠 Технологии

- **Python 3.12** - современная версия с улучшенной производительностью
- **aiogram 3.22.0** - асинхронный фреймворк для Telegram Bot API
- **SQLAlchemy 2.0** - современный ORM для работы с базой данных
- **SQLite** - легкая встроенная база данных
- **Pydantic** - валидация данных и настроек
- **uv** - сверхбыстрый пакетный менеджер для Python

## ⚡ Быстрый запуск

### 1. Создание виртуального окружения
```bash
uv venv --python 3.12
```

### 2. Активация окружения

**Windows:**
```bash
.venv\Scripts\activate
```

**macOS/Linux:**
```bash
source .venv/bin/activate
```

### 3. Установка зависимостей
```bash
uv sync
```

### 4. Настройка переменных окружения

Скопируйте `example.env` в `.env`:
```bash
cp example.env .env
```

Отредактируйте `.env` файл:
```env
BOT_TOKEN=your_bot_token_here
ADMIN_IDS=123456789,987654321
DATABASE_URL=sqlite+aiosqlite:///./products.db
DB_ECHO=False
```

### 5. Получение токена бота

1. Найдите [@BotFather](https://t.me/BotFather) в Telegram
2. Отправьте команду `/newbot`
3. Следуйте инструкциям для создания бота
4. Скопируйте полученный токен в `.env`

### 6. Получение ID администратора

1. Найдите [@userinfobot](https://t.me/userinfobot) в Telegram
2. Отправьте любое сообщение
3. Скопируйте ваш ID в `ADMIN_IDS` в `.env`

### 7. Запуск бота
```bash
python app.py
```

## 📁 Структура проекта

```
test-task/
├── app.py
├── app_config.py
├── pyproject.toml
├── README.md
├── uv.lock
│
├── data/
│   └── bot.db
│
├── core/
│   ├── constants.py
│   ├── database/
│   │   ├── __init__.py
│   │   └── db_helper.py
│   ├── handlers/
│   │   ├── __init__.py
│   │   └── start.py
│   ├── keyboards/
│   │   ├── __init__.py
│   │   └── start_keyboard.py
│   ├── mixin/
│   │   ├── __init__.py
│   │   └── int_id_pk.py
│   ├── models/
│   │   ├── __init__.py
│   │   └── base.py
│   └── utils/
│       ├── __init__.py
│       ├── case_converter.py
│       ├── formater.py
│       ├── paginator.py
│       └── status.py
│
├── admins/
│   ├── filters/
│   │   ├── __init__.py
│   │   └── is_admin.py
│   ├── handlers/
│   │   ├── __init__.py
│   │   ├── admin_menu.py
│   │   ├── moderation.py
│   │   ├── moderation_navigation.py
│   │   ├── product_edit.py
│   │   └── statistics.py
│   ├── keyboards/
│   │   ├── __init__.py
│   │   ├── admin_keyboards.py
│   │   ├── edit_field_keyboards.py
│   │   └── moderation_keyboards.py
│   └── queries/
│       ├── __init__.py
│       └── admin.py
│
└── products/
    ├── handlers/
    │   ├── __init__.py
    │   ├── add_product.py
    │   ├── product_navigation.py
    │   └── view_products.py
    ├── keyboards/
    │   ├── __init__.py
    │   ├── empty_products_keyboards.py
    │   └── product_keyboards.py
    ├── models/
    │   ├── __init__.py
    │   └── product.py
    ├── queries/
    │   ├── __init__.py
    │   └── product.py
    └── states/
        ├── __init__.py
        ├── add_product.py
        ├── edit_product.py
        ├── moderation.py
        └── view_products.py

```

## 🎯 Основные команды

- `/start` - запуск бота и главное меню
- `/admin` - админ-панель (только для администраторов)
- `/cancel` - отмена текущего действия
- `/back` - возврат к предыдущему шагу

## 🔧 Разработка

### Добавление новых зависимостей
```bash
uv add package_name
```

### Обновление зависимостей
```bash
uv pip install --upgrade -e .

```
