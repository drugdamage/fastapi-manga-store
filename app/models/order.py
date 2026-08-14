# models for rendering orders
from pydantic import BaseModel


# one line in an order
class OrderItemView(BaseModel):
    product_title: str
    quantity: int
    price: float


# order for the page
class OrderView(BaseModel):
    id: int
    user_id: int
    username: str
    status: str
    total_price: float
    items: list[OrderItemView]
