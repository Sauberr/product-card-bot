# Product card tg bot

Telegram bot for managing product cards with a moderation system and admin panel.

## 🚀 Features

### For users:
- **Adding products** - creating cards with name, description, price, and photo
- **Viewing products** - pagination through approved cards
- **Moderation system** - all products undergo review by an administrator

### For administrators:
- **Product moderation** - approving/rejecting/deleting cards
- **Product editing** - changing any card attributes
- **Statistics** - viewing data on users and their products
- **Full control** - managing all products in the system

## 🛠 Technologies

- **Python 3.12** - modern version with improved performance
- **aiogram 3.22.0** - asynchronous framework for Telegram Bot API
- **SQLAlchemy 2.0** - modern ORM for database management
- **SQLite** - lightweight embedded database
- **Pydantic** - data and settings validation
- **uv** - ultra-fast package manager for Python

## ⚡ Quick Start

### 1. Creating a virtual environment
```bash
uv venv --python 3.12
```

### 2. Activating the enviroment

**Windows:**
```bash
.venv\Scripts\activate
```

**macOS/Linux:**
```bash
source .venv/bin/activate
```

### 3. Installing dependencies
```bash
uv sync
```

### 4. Environment variale configuration

Copy `example.env` в `.env`:
```bash
cp example.env .env
```

Edit `.env` file:
```env
BOT_TOKEN=your_bot_token_here
ADMIN_IDS=123456789,987654321
DATABASE_URL=sqlite+aiosqlite:///./products.db
DB_ECHO=False
```

### 5. Getting the bot token

1. Find [@BotFather](https://t.me/BotFather) on Telegram
2. Send the `/newbot` command
3. Follow the instructions to create a bot
4. Copy the received token into `.env`

### 6. Getting an administrator ID

1. Find [@userinfobot](https://t.me/userinfobot) on Telegram
2. Send any message
3. Copy your ID into `ADMIN_IDS` in `.env`

### 7. Running the bot
```bash
python app.py
```

## 📁 Project Structure

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

## 🎯 Basic Commands

- `/start` - bot startup and main menu
- `/admin` - admin panel (for administrators only)
- `/cancel` - canceling the current action
- `/back` - return to the previous step

## 🔧 Development

### Adding new dependencies
```bash
uv add package_name
```

### Updating dependencies
```bash
uv pip install --upgrade -e .

```
