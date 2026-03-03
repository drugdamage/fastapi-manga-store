from typing import Dict
from app.models.items import ItemCreate, ItemOut

_items: Dict[int, ItemOut] = {}
_next_id = 1

def get_item_by_id(item_id: int) -> ItemOut:
    return _items[item_id]

def create_item(payload: ItemCreate) -> ItemOut:
    global _next_id
    item = ItemOut(id=_next_id, name=payload.name, price=payload.price)
    _items[_next_id] = item
    _next_id += 1
    return item