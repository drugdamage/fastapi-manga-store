# api роуты для товаров
from fastapi import APIRouter, HTTPException, Request

# схемы товара и сервисы
from app.models.product import ProductCreate, ProductOut
from app.services import auth_service, catalog_service

# создаем api роутер
router = APIRouter(tags=["manga-api"])


@router.get("/items", response_model=list[ProductOut])
def list_items():
    # отдаем список товаров в json
    return catalog_service.list_products()


@router.get("/items/{item_id}", response_model=ProductOut)
def get_item(item_id: int):
    # ищем товар по id
    product = catalog_service.get_product(item_id)
    if product is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return product


@router.post("/items", response_model=ProductOut, status_code=201)
def create_item(payload: ProductCreate, request: Request):
    # проверяем роль менеджера
    auth_service.require_role(request, "manager")
    # создаем новый товар
    return catalog_service.create_product(payload)
