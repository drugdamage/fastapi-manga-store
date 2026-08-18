# FastAPI Manga Store

A small manga shop built with FastAPI, made while relearning Python.
Kept small on purpose: products, login, `user`/`manager`/`admin` roles,
orders, a Jinja2 front end, SQLite.

> **Not maintained.** Old project, not currently worked on, no plans
> to continue it.

## What works

- homepage and catalogue
- product detail view, create/edit as `manager` or `admin`
- registration, login, logout, account page
- own orders (user) or all orders (`manager`/`admin`)
- role changes (`admin`)
- products API at `/api/items`

## Tech stack

- Python 3
- FastAPI
- Uvicorn
- SQLAlchemy
- SQLite
- Pydantic
- Jinja2

## Project structure

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

## Getting it running

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn main:app --reload
```

Then open:

- `http://127.0.0.1:8000`
- `http://127.0.0.1:8000/docs`

## Database

Created automatically on startup (`manga_store.db`), seeded with
starter products and test accounts.

## Test accounts

- `user / user123`
- `manager / manager123`
- `admin / admin123`

## Roles

- **user** — register, log in, browse, order, view own orders
- **manager** — user, plus add/edit products, view all orders
- **admin** — manager, plus `/admin/users` page, change roles

## Pages

- `/` - homepage
- `/catalog` - catalogue
- `/login` - login
- `/register` - registration
- `/account` - account
- `/orders` - my orders
- `/orders/all` - all orders, for manager/admin
- `/admin/users` - users and roles, for admin

## API

- `GET /api/items` - list products
- `GET /api/items/{item_id}` - single product
- `POST /api/items` - create product (`manager`/`admin`)
