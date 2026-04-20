# модели таблиц базы
from sqlalchemy import Boolean, Float, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db import Base


# Таблица пользователей.
class UserDB(Base):
    __tablename__ = "users"

    # id пользователя
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    # логин пользователя
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    # тут лежит хеш пароля
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    # роль пользователя
    role: Mapped[str] = mapped_column(String(20), default="user", nullable=False)

    # связь с заказами
    orders: Mapped[list["OrderDB"]] = relationship(back_populates="user")


# Таблица товаров.
class ProductDB(Base):
    __tablename__ = "products"

    # id товара
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    # название манги
    title: Mapped[str] = mapped_column(String(120), nullable=False)
    # описание товара
    description: Mapped[str] = mapped_column(String(1000), nullable=False)
    # цена товара
    price: Mapped[float] = mapped_column(Float, nullable=False)
    # ссылка на картинку
    image_url: Mapped[str] = mapped_column(String(255), nullable=False)
    # номер тома
    volume: Mapped[int] = mapped_column(Integer, nullable=False)
    # жанр
    genre: Mapped[str] = mapped_column(String(50), nullable=False)
    # есть ли товар в наличии
    in_stock: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    # связь с товарами в заказе
    order_items: Mapped[list["OrderItemDB"]] = relationship(back_populates="product")


# Таблица заказов.
class OrderDB(Base):
    __tablename__ = "orders"

    # id заказа
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    # владелец заказа
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    # простой статус заказа
    status: Mapped[str] = mapped_column(String(20), default="new", nullable=False)
    # общая сумма
    total_price: Mapped[float] = mapped_column(Float, default=0, nullable=False)

    # связь с пользователем
    user: Mapped["UserDB"] = relationship(back_populates="orders")
    # связь с товарами заказа
    items: Mapped[list["OrderItemDB"]] = relationship(back_populates="order")


# Товары внутри заказа.
class OrderItemDB(Base):
    __tablename__ = "order_items"

    # id позиции заказа
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    # к какому заказу относится
    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id"), nullable=False)
    # какой товар купили
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"), nullable=False)
    # сколько штук
    quantity: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    # цена на момент заказа
    price: Mapped[float] = mapped_column(Float, nullable=False)

    # связь с заказом
    order: Mapped["OrderDB"] = relationship(back_populates="items")
    # связь с товаром
    product: Mapped["ProductDB"] = relationship(back_populates="order_items")
