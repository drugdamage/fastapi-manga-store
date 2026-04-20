# сервис для заказов
from sqlalchemy import select
from sqlalchemy.orm import joinedload

# подключаем базу, таблицы и схемы
from app.db import get_session
from app.models.database import OrderDB, OrderItemDB, ProductDB, UserDB
from app.models.order import OrderItemView, OrderView


def create_order(user_id: int, product_id: int, quantity: int) -> OrderView:
    # Создаем простой заказ из одного товара.
    with get_session() as session:
        # ищем пользователя и товар
        user = session.get(UserDB, user_id)
        product = session.get(ProductDB, product_id)

        if user is None or product is None:
            raise ValueError("User or product not found")
        # количество должно быть больше нуля
        if quantity < 1:
            raise ValueError("Quantity must be positive")
        # нельзя заказать товар не в наличии
        if not product.in_stock:
            raise ValueError("Product is out of stock")

        # цена одной штуки
        item_price = product.price
        # общая сумма
        total_price = item_price * quantity

        # создаем сам заказ
        order = OrderDB(
            user_id=user_id,
            status="new",
            total_price=total_price,
        )
        session.add(order)
        # flush нужен, чтобы получить id заказа
        session.flush()

        # создаем строку заказа
        order_item = OrderItemDB(
            order_id=order.id,
            product_id=product.id,
            quantity=quantity,
            price=item_price,
        )
        session.add(order_item)
        # сохраняем заказ и позицию
        session.commit()

        # возвращаем данные для страницы
        return OrderView(
            id=order.id,
            user_id=user.id,
            username=user.username,
            status=order.status,
            total_price=order.total_price,
            items=[
                OrderItemView(
                    product_title=product.title,
                    quantity=quantity,
                    price=item_price,
                )
            ],
        )


def get_orders_for_user(user_id: int) -> list[OrderView]:
    # Берем только заказы одного пользователя.
    with get_session() as session:
        # грузим пользователя и товары вместе
        orders = session.scalars(
            select(OrderDB)
            .options(
                joinedload(OrderDB.user),
                joinedload(OrderDB.items).joinedload(OrderItemDB.product),
            )
            .where(OrderDB.user_id == user_id)
            .order_by(OrderDB.id.desc())
        ).unique().all()

        return [_to_order_view(order) for order in orders]


def get_all_orders() -> list[OrderView]:
    # Берем все заказы для manager и admin.
    with get_session() as session:
        # грузим все заказы и связанные данные
        orders = session.scalars(
            select(OrderDB)
            .options(
                joinedload(OrderDB.user),
                joinedload(OrderDB.items).joinedload(OrderItemDB.product),
            )
            .order_by(OrderDB.id.desc())
        ).unique().all()

        return [_to_order_view(order) for order in orders]


def _to_order_view(order: OrderDB) -> OrderView:
    # собираем удобный объект для шаблона
    return OrderView(
        id=order.id,
        user_id=order.user.id,
        username=order.user.username,
        status=order.status,
        total_price=order.total_price,
        items=[
            OrderItemView(
                product_title=item.product.title,
                quantity=item.quantity,
                price=item.price,
            )
            for item in order.items
        ],
    )
