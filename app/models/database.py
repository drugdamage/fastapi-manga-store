# database table models
from sqlalchemy import Boolean, Float, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db import Base


# Users table.
class UserDB(Base):
    __tablename__ = "users"

    # user id
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    # username
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    # password hash lives here
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    # user role
    role: Mapped[str] = mapped_column(String(20), default="user", nullable=False)

    # relationship to orders
    orders: Mapped[list["OrderDB"]] = relationship(back_populates="user")


# Products table.
class ProductDB(Base):
    __tablename__ = "products"

    # product id
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    # manga title
    title: Mapped[str] = mapped_column(String(120), nullable=False)
    # product description
    description: Mapped[str] = mapped_column(String(1000), nullable=False)
    # product price
    price: Mapped[float] = mapped_column(Float, nullable=False)
    # image url
    image_url: Mapped[str] = mapped_column(String(255), nullable=False)
    # volume number
    volume: Mapped[int] = mapped_column(Integer, nullable=False)
    # genre
    genre: Mapped[str] = mapped_column(String(50), nullable=False)
    # whether the product is in stock
    in_stock: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    # relationship to order items
    order_items: Mapped[list["OrderItemDB"]] = relationship(back_populates="product")


# Orders table.
class OrderDB(Base):
    __tablename__ = "orders"

    # order id
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    # order owner
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    # simple order status
    status: Mapped[str] = mapped_column(String(20), default="new", nullable=False)
    # total amount
    total_price: Mapped[float] = mapped_column(Float, default=0, nullable=False)

    # relationship to user
    user: Mapped["UserDB"] = relationship(back_populates="orders")
    # relationship to order items
    items: Mapped[list["OrderItemDB"]] = relationship(back_populates="order")


# Items within an order.
class OrderItemDB(Base):
    __tablename__ = "order_items"

    # order item id
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    # which order this belongs to
    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id"), nullable=False)
    # which product was bought
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"), nullable=False)
    # quantity
    quantity: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    # price at the time of order
    price: Mapped[float] = mapped_column(Float, nullable=False)

    # relationship to order
    order: Mapped["OrderDB"] = relationship(back_populates="items")
    # relationship to product
    product: Mapped["ProductDB"] = relationship(back_populates="order_items")
