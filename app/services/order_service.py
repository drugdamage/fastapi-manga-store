# service for orders
from sqlalchemy import select
from sqlalchemy.orm import joinedload

# wire up the database, tables, and schemas
from app.db import get_session
from app.models.database import OrderDB, OrderItemDB, ProductDB, UserDB
from app.models.order import OrderItemView, OrderView


def create_order(user_id: int, product_id: int, quantity: int) -> OrderView:
    # Create a simple single-product order.
    with get_session() as session:
        # look up the user and product
        user = session.get(UserDB, user_id)
        product = session.get(ProductDB, product_id)

        if user is None or product is None:
            raise ValueError("User or product not found")
        # quantity must be greater than zero
        if quantity < 1:
            raise ValueError("Quantity must be positive")
        # can't order a product that's out of stock
        if not product.in_stock:
            raise ValueError("Product is out of stock")

        # price per unit
        item_price = product.price
        # total amount
        total_price = item_price * quantity

        # create the order itself
        order = OrderDB(
            user_id=user_id,
            status="new",
            total_price=total_price,
        )
        session.add(order)
        # flush is needed to get the order id
        session.flush()

        # create the order line
        order_item = OrderItemDB(
            order_id=order.id,
            product_id=product.id,
            quantity=quantity,
            price=item_price,
        )
        session.add(order_item)
        # save the order and its item
        session.commit()

        # return data for the page
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
    # Get only one user's orders.
    with get_session() as session:
        # load the user and products together
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
    # Get all orders for manager and admin.
    with get_session() as session:
        # load all orders and related data
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
    # build a convenient object for the template
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
