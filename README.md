# FastAPI Manga Store

A small learning project — a manga shop built with FastAPI while getting
back into Python properly after a bit of a break. Still learning as I go,
so the whole thing's kept small and dead easy to follow on purpose.

Deliberately kept small and simple:
- products
- registration and login
- `user`, `manager`, `admin` roles
- orders
- a bare-bones HTML front end with Jinja2
- SQLite database

## What's working so far

- homepage and catalogue
- product detail view
- creating a product as `manager` or `admin`
- editing a product as `manager` or `admin`
- new user registration
- login and logout
- account page
- viewing your own orders
- viewing all orders as `manager` or `admin`
- changing user roles as `admin`
- an API for products at `/api/items`

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

Once it's up, have a look at:

- `http://127.0.0.1:8000`
- `http://127.0.0.1:8000/docs`

## How the database works

- the database gets created automatically when the app starts
- database file: `manga_store.db`
- starter products get seeded in automatically
- test accounts get seeded in automatically too

## Test accounts

- `user / user123`
- `manager / manager123`
- `admin / admin123`

## What each role can do

### user

- can register
- can log in
- can browse products
- can place an order
- can only see their own orders

### manager

- everything `user` can do
- can add products
- can edit products
- can see all orders

### admin

- everything `manager` can do
- can open the `/admin/users` page
- can change user roles

## Handy pages

- `/` - homepage
- `/catalog` - catalogue
- `/login` - login
- `/register` - registration
- `/account` - account
- `/orders` - my orders
- `/orders/all` - all orders, for manager/admin
- `/admin/users` - users and roles, for admin

## API

- `GET /api/items` - list of products
- `GET /api/items/{item_id}` - a single product
- `POST /api/items` - create a product, needs `manager` or `admin`
