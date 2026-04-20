# FastAPI Manga Store

Простой учебный проект интернет-магазина манги на FastAPI.

Проект специально сделан маленьким и понятным:
- товары
- регистрация и вход
- роли `user`, `manager`, `admin`
- заказы
- простая HTML-часть на Jinja2
- SQLite база данных

## Что уже есть

- главная страница и каталог
- просмотр товара
- создание товара для `manager` и `admin`
- редактирование товара для `manager` и `admin`
- регистрация новых пользователей
- вход и выход
- страница аккаунта
- просмотр своих заказов
- просмотр всех заказов для `manager` и `admin`
- смена ролей пользователей для `admin`
- API для товаров по пути `/api/items`

## Технологии

- Python 3
- FastAPI
- Uvicorn
- SQLAlchemy
- SQLite
- Pydantic
- Jinja2

## Структура проекта

```text
fastapi-manga-store/
├── app/
│   ├── models/
│   │   ├── database.py
│   │   ├── order.py
│   │   ├── product.py
│   │   └── user.py
│   ├── routers/
│   │   ├── items.py
│   │   └── pages.py
│   ├── services/
│   │   ├── auth_service.py
│   │   ├── catalog_service.py
│   │   └── order_service.py
│   ├── static/
│   ├── templates/
│   └── db.py
├── main.py
├── requirements.txt
└── README.md
```

## Как запустить

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn main:app --reload
```

После запуска открыть:

- `http://127.0.0.1:8000`
- `http://127.0.0.1:8000/docs`

## Как работает база

- база создается автоматически при старте приложения
- файл базы: `manga_store.db`
- стартовые товары добавляются автоматически
- тестовые аккаунты тоже добавляются автоматически

## Тестовые аккаунты

- `user / user123`
- `manager / manager123`
- `admin / admin123`

## Что проверять по ролям

### user

- может зарегистрироваться
- может войти
- может смотреть товары
- может делать заказ
- может смотреть только свои заказы

### manager

- может все, что `user`
- может добавлять товары
- может редактировать товары
- может смотреть все заказы

### admin

- может все, что `manager`
- может открывать страницу `/admin/users`
- может менять роли пользователей

## Полезные страницы

- `/` - главная
- `/catalog` - каталог
- `/login` - вход
- `/register` - регистрация
- `/account` - аккаунт
- `/orders` - мои заказы
- `/orders/all` - все заказы для manager/admin
- `/admin/users` - пользователи и роли для admin

## API

- `GET /api/items` - список товаров
- `GET /api/items/{item_id}` - один товар
- `POST /api/items` - создать товар, нужен `manager` или `admin`
