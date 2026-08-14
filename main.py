# main application file
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from sqlalchemy import select
from starlette.middleware.sessions import SessionMiddleware

# wire up the database and models
from app.db import Base, engine, get_session
from app.models.database import ProductDB
from app.models.user import Role
# wire up the routers and services
from app.routers import items, pages
from app.services import auth_service

# create the FastAPI app
app = FastAPI(title="Manga Store MVP")
# enable sessions for login
app.add_middleware(SessionMiddleware, secret_key="simple-manga-store-secret-key")

# mount the folder with styles and images
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# wire up pages and api
app.include_router(pages.router)
app.include_router(items.router, prefix="/api")


def seed_products() -> None:
    # Add the starter products only once.
    with get_session() as session:
        # check if products already exist
        existing_product = session.scalar(select(ProductDB.id).limit(1))
        if existing_product is not None:
            return

        # list of starter manga
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

        # save products to the database
        session.add_all(products)
        session.commit()


def seed_users() -> None:
    # Add demo users for each role.
    demo_users = [
        ("admin", "admin123", Role.admin.value),
        ("manager", "manager123", Role.manager.value),
        ("user", "user123", Role.user.value),
    ]

    # try to add the demo accounts
    for username, password, role in demo_users:
        try:
            auth_service.create_user(username, password, role)
        except ValueError:
            # already exists, just move on
            continue


@app.on_event("startup")
def on_startup() -> None:
    # Create tables and seed data.
    # create tables in sqlite
    Base.metadata.create_all(bind=engine)
    # add starter products
    seed_products()
    # add demo users
    seed_users()
