from fastapi import APIRouter, HTTPException
from app.models.items import ItemCreate, ItemOut
from app.services import items_service

router = APIRouter()

@router.get("/items/{item_id}", response_model=ItemOut)
def get_item(item_id: int):
    try:
        return items_service.get_item_by_id(item_id)
    except KeyError:
        raise HTTPException(status_code=404, detail="Item not found")

@router.post("/items", response_model=ItemOut, status_code=201)
def create_item(payload: ItemCreate):
    return items_service.create_item(payload)