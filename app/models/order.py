# модели для вывода заказов
from pydantic import BaseModel


# одна строка в заказе
class OrderItemView(BaseModel):
    product_title: str
    quantity: int
    price: float


# заказ для страницы
class OrderView(BaseModel):
    id: int
    user_id: int
    username: str
    status: str
    total_price: float
    items: list[OrderItemView]
