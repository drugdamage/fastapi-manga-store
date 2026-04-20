# главный файл приложения
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from sqlalchemy import select
from starlette.middleware.sessions import SessionMiddleware

# подключаем базу и модели
from app.db import Base, engine, get_session
from app.models.database import ProductDB
from app.models.user import Role
# подключаем роуты и сервисы
from app.routers import items, pages
from app.services import auth_service

# создаем приложение FastAPI
app = FastAPI(title="Manga Store MVP")
# включаем сессии для входа
app.add_middleware(SessionMiddleware, secret_key="simple-manga-store-secret-key")

# подключаем папку со стилями и картинками
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# подключаем страницы и api
app.include_router(pages.router)
app.include_router(items.router, prefix="/api")


def seed_products() -> None:
    # Добавляем стартовые товары только один раз.
    with get_session() as session:
        # проверяем, есть ли уже товары
        existing_product = session.scalar(select(ProductDB.id).limit(1))
        if existing_product is not None:
            return

        # список стартовых манг
        products = [
            ProductDB(
                title="Jujutsu Kaisen",
                description="Dark fantasy manga about curses, sorcerers, and intense battles.",
                price=12.99,
                image_url="/static/images/jujutsu-kaisen-vol1.jpg",
                volume=1,
                genre="Dark Fantasy",
                in_stock=True,
            ),
            ProductDB(
                title="Vinland Saga",
                description="Historical action manga about war, revenge, and the Viking age.",
                price=14.50,
                image_url="/static/images/vinland-saga-vol1.jpg",
                volume=1,
                genre="Historical",
                in_stock=True,
            ),
            ProductDB(
                title="Chainsaw Man",
                description="A brutal and chaotic story about devils, hunters, and survival.",
                price=11.90,
                image_url="/static/images/chainsaw-man-vol1.jpg",
                volume=1,
                genre="Action Horror",
                in_stock=True,
            ),
            ProductDB(
                title="Tokyo Ghoul",
                description="A dark supernatural manga about identity, fear, and ghouls.",
                price=13.20,
                image_url="https://placehold.co/600x800?text=Tokyo+Ghoul",
                volume=1,
                genre="Supernatural",
                in_stock=False,
            ),
            ProductDB(
                title="Attack on Titan",
                description="A famous action manga about humanity fighting giant titans.",
                price=15.00,
                image_url="https://placehold.co/600x800?text=Attack+on+Titan",
                volume=1,
                genre="Action",
                in_stock=True,
            ),
        ]

        # сохраняем товары в базу
        session.add_all(products)
        session.commit()


def seed_users() -> None:
    # Добавляем demo пользователей по ролям.
    demo_users = [
        ("admin", "admin123", Role.admin.value),
        ("manager", "manager123", Role.manager.value),
        ("user", "user123", Role.user.value),
    ]

    # пробуем добавить demo аккаунты
    for username, password, role in demo_users:
        try:
            auth_service.create_user(username, password, role)
        except ValueError:
            # если такой уже есть, просто идем дальше
            continue


@app.on_event("startup")
def on_startup() -> None:
    # Создаем таблицы и начальные данные.
    # создаем таблицы в sqlite
    Base.metadata.create_all(bind=engine)
    # добавляем стартовые товары
    seed_products()
    # добавляем demo пользователей
    seed_users()
