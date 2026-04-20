# сервис для работы с товарами
from sqlalchemy import select

# подключаем базу и схемы
from app.db import get_session
from app.models.database import ProductDB
from app.models.product import ProductCreate, ProductOut, ProductUpdate


def list_products() -> list[ProductOut]:
    # Берем все товары из базы.
    with get_session() as session:
        # делаем запрос с сортировкой по id
        products = session.scalars(select(ProductDB).order_by(ProductDB.id)).all()
        # переводим orm объекты в pydantic
        return [ProductOut.model_validate(product) for product in products]


def get_product(product_id: int) -> ProductOut | None:
    # Ищем один товар по id.
    with get_session() as session:
        # берем товар по ключу
        product = session.get(ProductDB, product_id)
        if product is None:
            return None
        return ProductOut.model_validate(product)


def create_product(payload: ProductCreate) -> ProductOut:
    # Создаем новый товар в базе.
    with get_session() as session:
        # собираем объект товара
        product = ProductDB(
            title=payload.title,
            description=payload.description,
            price=payload.price,
            image_url=payload.image_url,
            volume=payload.volume,
            genre=payload.genre,
            in_stock=payload.in_stock,
        )
        # добавляем товар в сессию
        session.add(product)
        # сохраняем в базу
        session.commit()
        # обновляем объект после сохранения
        session.refresh(product)
        return ProductOut.model_validate(product)


def update_product(product_id: int, payload: ProductUpdate) -> ProductOut | None:
    # Обновляем товар в базе.
    with get_session() as session:
        # ищем товар для редактирования
        product = session.get(ProductDB, product_id)
        if product is None:
            return None

        # меняем поля товара
        product.title = payload.title
        product.description = payload.description
        product.price = payload.price
        product.image_url = payload.image_url
        product.volume = payload.volume
        product.genre = payload.genre
        product.in_stock = payload.in_stock

        # сохраняем новые данные
        session.commit()
        session.refresh(product)
        return ProductOut.model_validate(product)
