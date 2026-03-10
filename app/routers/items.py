from fastapi import APIRouter, HTTPException

from app.models.product import ProductCreate, ProductOut
from app.services import catalog_service

router = APIRouter(tags=["manga-api"])


@router.get("/items", response_model=list[ProductOut])
def list_items():
    return catalog_service.list_products()


@router.get("/items/{item_id}", response_model=ProductOut)
def get_item(item_id: int):
    product = catalog_service.get_product(item_id)
    if product is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return product


@router.post("/items", response_model=ProductOut, status_code=201)
def create_item(payload: ProductCreate):
    return catalog_service.create_product(payload)