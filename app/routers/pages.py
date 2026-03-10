from fastapi import APIRouter, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from app.models.product import ProductCreate
from app.services import catalog_service

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@router.get("/", response_class=HTMLResponse)
def home(request: Request):
    featured_products = catalog_service.list_products()[:3]
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "products": featured_products,
        },
    )


@router.get("/catalog", response_class=HTMLResponse)
def catalog(request: Request):
    products = catalog_service.list_products()
    return templates.TemplateResponse(
        "catalog.html",
        {
            "request": request,
            "products": products,
        },
    )


@router.get("/products/{product_id}", response_class=HTMLResponse)
def product_detail(request: Request, product_id: int):
    product = catalog_service.get_product(product_id)
    if product is None:
        return templates.TemplateResponse(
            "product.html",
            {
                "request": request,
                "product": None,
            },
            status_code=404,
        )

    return templates.TemplateResponse(
        "product.html",
        {
            "request": request,
            "product": product,
        },
    )


@router.get("/products/new", response_class=HTMLResponse)
def create_product_page(request: Request):
    return templates.TemplateResponse(
        "create_product.html",
        {
            "request": request,
        },
    )


@router.post("/products/new")
def create_product(
    title: str = Form(...),
    description: str = Form(...),
    price: float = Form(...),
    image_url: str = Form(...),
    volume: int = Form(...),
    genre: str = Form(...),
    in_stock: bool = Form(False),
):
    payload = ProductCreate(
        title=title,
        description=description,
        price=price,
        image_url=image_url,
        volume=volume,
        genre=genre,
        in_stock=in_stock,
    )
    product = catalog_service.create_product(payload)
    return RedirectResponse(url=f"/products/{product.id}", status_code=303)