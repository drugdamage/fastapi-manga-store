# service for working with products
from sqlalchemy import select

# wire up the database and schemas
from app.db import get_session
from app.models.database import ProductDB
from app.models.product import ProductCreate, ProductOut, ProductUpdate


def list_products() -> list[ProductOut]:
    # Get all products from the database.
    with get_session() as session:
        # query sorted by id
        products = session.scalars(select(ProductDB).order_by(ProductDB.id)).all()
        # convert orm objects to pydantic
        return [ProductOut.model_validate(product) for product in products]


def get_product(product_id: int) -> ProductOut | None:
    # Look up a single product by id.
    with get_session() as session:
        # get the product by key
        product = session.get(ProductDB, product_id)
        if product is None:
            return None
        return ProductOut.model_validate(product)


def create_product(payload: ProductCreate) -> ProductOut:
    # Create a new product in the database.
    with get_session() as session:
        # build the product object
        product = ProductDB(
            title=payload.title,
            description=payload.description,
            price=payload.price,
            image_url=payload.image_url,
            volume=payload.volume,
            genre=payload.genre,
            in_stock=payload.in_stock,
        )
        # add the product to the session
        session.add(product)
        # save to the database
        session.commit()
        # refresh the object after saving
        session.refresh(product)
        return ProductOut.model_validate(product)


def update_product(product_id: int, payload: ProductUpdate) -> ProductOut | None:
    # Update the product in the database.
    with get_session() as session:
        # look up the product to edit
        product = session.get(ProductDB, product_id)
        if product is None:
            return None

        # update the product fields
        product.title = payload.title
        product.description = payload.description
        product.price = payload.price
        product.image_url = payload.image_url
        product.volume = payload.volume
        product.genre = payload.genre
        product.in_stock = payload.in_stock

        # save the new data
        session.commit()
        session.refresh(product)
        return ProductOut.model_validate(product)
