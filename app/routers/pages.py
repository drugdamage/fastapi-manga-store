# роуты для html страниц
from fastapi import APIRouter, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

# подключаем схемы и сервисы
from app.models.product import ProductCreate, ProductUpdate
from app.models.user import Role
from app.services import auth_service, catalog_service, order_service

# роутер для страниц
router = APIRouter()
# папка с шаблонами
templates = Jinja2Templates(directory="app/templates")


def build_context(request: Request, **extra):
    # Общий контекст для шаблонов.
    # берем пользователя из сессии
    current_user = auth_service.get_current_user(request)
    context = {
        "request": request,
        "current_user": current_user,
        # проверяем роль менеджера
        "is_manager": current_user is not None and auth_service.has_role(current_user, Role.manager.value),
        # проверяем роль админа
        "is_admin": current_user is not None and auth_service.has_role(current_user, Role.admin.value),
    }
    # добавляем свои данные для шаблона
    context.update(extra)
    return context


@router.get("/", response_class=HTMLResponse)
def home(request: Request):
    # берем несколько товаров для главной
    featured_products = catalog_service.list_products()[:3]
    return templates.TemplateResponse(
        "index.html",
        build_context(request, products=featured_products),
    )


@router.get("/catalog", response_class=HTMLResponse)
def catalog(request: Request):
    # показываем весь каталог
    products = catalog_service.list_products()
    return templates.TemplateResponse(
        "catalog.html",
        build_context(request, products=products),
    )


@router.get("/products/new", response_class=HTMLResponse)
def create_product_page(request: Request):
    # сюда может зайти только менеджер или админ
    auth_service.require_role(request, Role.manager.value)
    return templates.TemplateResponse(
        "create_product.html",
        build_context(request),
    )


@router.get("/products/{product_id}", response_class=HTMLResponse)
def product_detail(request: Request, product_id: int):
    # ищем товар по id
    product = catalog_service.get_product(product_id)
    if product is None:
        # если товара нет, показываем 404 страницу
        return templates.TemplateResponse(
            "product.html",
            build_context(request, product=None),
            status_code=404,
        )

    return templates.TemplateResponse(
        "product.html",
        build_context(request, product=product),
    )

@router.post("/products/new")
def create_product_page_post(
    request: Request,
    title: str = Form(...),
    description: str = Form(...),
    price: float = Form(...),
    image_url: str = Form(...),
    volume: int = Form(...),
    genre: str = Form(...),
    in_stock: bool = Form(False),
):
    # проверяем роль менеджера
    auth_service.require_role(request, Role.manager.value)
    # собираем данные из формы
    payload = ProductCreate(
        title=title,
        description=description,
        price=price,
        image_url=image_url,
        volume=volume,
        genre=genre,
        in_stock=in_stock,
    )
    # сохраняем новый товар
    product = catalog_service.create_product(payload)
    # после создания идем на страницу товара
    return RedirectResponse(url=f"/products/{product.id}", status_code=303)


@router.get("/products/{product_id}/edit", response_class=HTMLResponse)
def edit_product_page(request: Request, product_id: int):
    # редактировать товар может менеджер
    auth_service.require_role(request, Role.manager.value)
    # ищем товар
    product = catalog_service.get_product(product_id)
    if product is None:
        return templates.TemplateResponse(
            "product.html",
            build_context(request, product=None),
            status_code=404,
        )

    return templates.TemplateResponse(
        "edit_product.html",
        build_context(request, product=product),
    )


@router.post("/products/{product_id}/edit")
def edit_product_page_post(
    request: Request,
    product_id: int,
    title: str = Form(...),
    description: str = Form(...),
    price: float = Form(...),
    image_url: str = Form(...),
    volume: int = Form(...),
    genre: str = Form(...),
    in_stock: bool = Form(False),
):
    # проверяем роль менеджера
    auth_service.require_role(request, Role.manager.value)
    # собираем новые данные из формы
    payload = ProductUpdate(
        title=title,
        description=description,
        price=price,
        image_url=image_url,
        volume=volume,
        genre=genre,
        in_stock=in_stock,
    )
    # обновляем товар в базе
    product = catalog_service.update_product(product_id, payload)
    if product is None:
        return templates.TemplateResponse(
            "product.html",
            build_context(request, product=None),
            status_code=404,
        )
    return RedirectResponse(url=f"/products/{product.id}", status_code=303)


@router.get("/register", response_class=HTMLResponse)
def register_page(request: Request):
    # показываем страницу регистрации
    return templates.TemplateResponse(
        "register.html",
        build_context(request, error=None),
    )


@router.post("/register", response_class=HTMLResponse)
def register_post(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
):
    # пробуем создать пользователя
    try:
        user = auth_service.create_user(username=username, password=password)
    except ValueError:
        # если логин занят, показываем ошибку
        return templates.TemplateResponse(
            "register.html",
            build_context(request, error="Username already exists"),
            status_code=400,
        )

    # сразу логиним нового пользователя
    auth_service.login_user(request, user)
    return RedirectResponse(url="/account", status_code=303)


@router.get("/login", response_class=HTMLResponse)
def login_page(request: Request):
    # показываем страницу входа
    return templates.TemplateResponse(
        "login.html",
        build_context(request, error=None),
    )


@router.post("/login", response_class=HTMLResponse)
def login_post(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
):
    # проверяем логин и пароль
    user = auth_service.authenticate_user(username=username, password=password)
    if user is None:
        # если данные неверные, показываем ошибку
        return templates.TemplateResponse(
            "login.html",
            build_context(request, error="Wrong username or password"),
            status_code=400,
        )

    # сохраняем пользователя в сессии
    auth_service.login_user(request, user)
    return RedirectResponse(url="/account", status_code=303)


@router.post("/logout")
def logout_post(request: Request):
    # выходим из аккаунта
    auth_service.logout_user(request)
    return RedirectResponse(url="/", status_code=303)


@router.get("/account", response_class=HTMLResponse)
def account_page(request: Request):
    # сюда пускаем только после входа
    user = auth_service.require_login(request)
    return templates.TemplateResponse(
        "account.html",
        build_context(request, account_user=user),
    )


@router.post("/products/{product_id}/order")
def create_order_post(
    request: Request,
    product_id: int,
    quantity: int = Form(1),
):
    # проверяем, что пользователь вошел
    user = auth_service.require_login(request)
    try:
        # создаем заказ на один товар
        order_service.create_order(user_id=user.id, product_id=product_id, quantity=quantity)
    except ValueError:
        # если ошибка, возвращаем назад
        return RedirectResponse(url=f"/products/{product_id}", status_code=303)
    # после заказа идем в список заказов
    return RedirectResponse(url="/orders", status_code=303)


@router.get("/orders", response_class=HTMLResponse)
def orders_page(request: Request):
    # пользователь видит только свои заказы
    user = auth_service.require_login(request)
    orders = order_service.get_orders_for_user(user.id)
    return templates.TemplateResponse(
        "orders.html",
        build_context(request, orders=orders, title="My Orders", show_username=False),
    )


@router.get("/orders/all", response_class=HTMLResponse)
def all_orders_page(request: Request):
    # все заказы видит менеджер и админ
    auth_service.require_role(request, Role.manager.value)
    orders = order_service.get_all_orders()
    return templates.TemplateResponse(
        "orders.html",
        build_context(request, orders=orders, title="All Orders", show_username=True),
    )


@router.get("/admin/users", response_class=HTMLResponse)
def users_page(request: Request):
    # список пользователей только для админа
    auth_service.require_role(request, Role.admin.value)
    users = auth_service.get_all_users()
    return templates.TemplateResponse(
        "users.html",
        build_context(request, users=users, roles=[role.value for role in Role]),
    )


@router.post("/admin/users/{user_id}/role")
def update_user_role_post(
    request: Request,
    user_id: int,
    role: str = Form(...),
):
    # менять роли может только админ
    auth_service.require_role(request, Role.admin.value)
    try:
        # обновляем роль в базе
        auth_service.update_user_role(user_id, role)
    except ValueError:
        return RedirectResponse(url="/admin/users", status_code=303)
    return RedirectResponse(url="/admin/users", status_code=303)
