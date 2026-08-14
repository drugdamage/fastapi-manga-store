# routes for html pages
from fastapi import APIRouter, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

# wire up schemas and services
from app.models.product import ProductCreate, ProductUpdate
from app.models.user import Role
from app.services import auth_service, catalog_service, order_service

# router for pages
router = APIRouter()
# templates folder
templates = Jinja2Templates(directory="app/templates")


def build_context(request: Request, **extra):
    # Shared context for templates.
    # get the user from the session
    current_user = auth_service.get_current_user(request)
    context = {
        "request": request,
        "current_user": current_user,
        # check manager role
        "is_manager": current_user is not None and auth_service.has_role(current_user, Role.manager.value),
        # check admin role
        "is_admin": current_user is not None and auth_service.has_role(current_user, Role.admin.value),
    }
    # add custom data for the template
    context.update(extra)
    return context


@router.get("/", response_class=HTMLResponse)
def home(request: Request):
    # get a few products for the homepage
    featured_products = catalog_service.list_products()[:3]
    return templates.TemplateResponse(
        "index.html",
        build_context(request, products=featured_products),
    )


@router.get("/catalog", response_class=HTMLResponse)
def catalog(request: Request):
    # show the whole catalog
    products = catalog_service.list_products()
    return templates.TemplateResponse(
        "catalog.html",
        build_context(request, products=products),
    )


@router.get("/products/new", response_class=HTMLResponse)
def create_product_page(request: Request):
    # only a manager or admin can get here
    auth_service.require_role(request, Role.manager.value)
    return templates.TemplateResponse(
        "create_product.html",
        build_context(request),
    )


@router.get("/products/{product_id}", response_class=HTMLResponse)
def product_detail(request: Request, product_id: int):
    # look up the product by id
    product = catalog_service.get_product(product_id)
    if product is None:
        # if the product doesn't exist, show the 404 page
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
    # check manager role
    auth_service.require_role(request, Role.manager.value)
    # gather the data from the form
    payload = ProductCreate(
        title=title,
        description=description,
        price=price,
        image_url=image_url,
        volume=volume,
        genre=genre,
        in_stock=in_stock,
    )
    # save the new product
    product = catalog_service.create_product(payload)
    # after creation, go to the product page
    return RedirectResponse(url=f"/products/{product.id}", status_code=303)


@router.get("/products/{product_id}/edit", response_class=HTMLResponse)
def edit_product_page(request: Request, product_id: int):
    # a manager can edit a product
    auth_service.require_role(request, Role.manager.value)
    # look up the product
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
    # check manager role
    auth_service.require_role(request, Role.manager.value)
    # gather the updated data from the form
    payload = ProductUpdate(
        title=title,
        description=description,
        price=price,
        image_url=image_url,
        volume=volume,
        genre=genre,
        in_stock=in_stock,
    )
    # update the product in the database
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
    # show the registration page
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
    # try to create the user
    try:
        user = auth_service.create_user(username=username, password=password)
    except ValueError:
        # if the username is taken, show an error
        return templates.TemplateResponse(
            "register.html",
            build_context(request, error="Username already exists"),
            status_code=400,
        )

    # log the new user in immediately
    auth_service.login_user(request, user)
    return RedirectResponse(url="/account", status_code=303)


@router.get("/login", response_class=HTMLResponse)
def login_page(request: Request):
    # show the login page
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
    # check username and password
    user = auth_service.authenticate_user(username=username, password=password)
    if user is None:
        # if the credentials are wrong, show an error
        return templates.TemplateResponse(
            "login.html",
            build_context(request, error="Wrong username or password"),
            status_code=400,
        )

    # store the user in the session
    auth_service.login_user(request, user)
    return RedirectResponse(url="/account", status_code=303)


@router.post("/logout")
def logout_post(request: Request):
    # log out of the account
    auth_service.logout_user(request)
    return RedirectResponse(url="/", status_code=303)


@router.get("/account", response_class=HTMLResponse)
def account_page(request: Request):
    # only allow access here after logging in
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
    # check that the user is logged in
    user = auth_service.require_login(request)
    try:
        # create an order for one product
        order_service.create_order(user_id=user.id, product_id=product_id, quantity=quantity)
    except ValueError:
        # on error, go back
        return RedirectResponse(url=f"/products/{product_id}", status_code=303)
    # after ordering, go to the orders list
    return RedirectResponse(url="/orders", status_code=303)


@router.get("/orders", response_class=HTMLResponse)
def orders_page(request: Request):
    # a user only sees their own orders
    user = auth_service.require_login(request)
    orders = order_service.get_orders_for_user(user.id)
    return templates.TemplateResponse(
        "orders.html",
        build_context(request, orders=orders, title="My Orders", show_username=False),
    )


@router.get("/orders/all", response_class=HTMLResponse)
def all_orders_page(request: Request):
    # manager and admin see all orders
    auth_service.require_role(request, Role.manager.value)
    orders = order_service.get_all_orders()
    return templates.TemplateResponse(
        "orders.html",
        build_context(request, orders=orders, title="All Orders", show_username=True),
    )


@router.get("/admin/users", response_class=HTMLResponse)
def users_page(request: Request):
    # user list is admin-only
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
    # only an admin can change roles
    auth_service.require_role(request, Role.admin.value)
    try:
        # update the role in the database
        auth_service.update_user_role(user_id, role)
    except ValueError:
        return RedirectResponse(url="/admin/users", status_code=303)
    return RedirectResponse(url="/admin/users", status_code=303)
