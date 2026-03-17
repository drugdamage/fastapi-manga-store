from app.models.product import ProductCreate, ProductOut

_products: list[ProductOut] = [
    ProductOut(
        id=1,
        title="Jujutsu Kaisen",
        description="Dark fantasy manga about curses, sorcerers, and intense battles.",
        price=12.99,
        image_url="/static/images/jujutsu-kaisen-vol1.jpg",
        volume=1,
        genre="Dark Fantasy",
        in_stock=True,
    ),
    ProductOut(
        id=2,
        title="Vinland Saga",
        description="Historical action manga about war, revenge, and the Viking age.",
        price=14.50,
        image_url="/static/images/vinland-saga-vol1.jpg",
        volume=1,
        genre="Historical",
        in_stock=True,
    ),
    ProductOut(
        id=3,
        title="Chainsaw Man",
        description="A brutal and chaotic story about devils, hunters, and survival.",
        price=11.90,
        image_url="/static/images/chainsaw-man-vol1.jpg",
        volume=1,
        genre="Action Horror",
        in_stock=True,
    ),
    ProductOut(
        id=4,
        title="Tokyo Ghoul",
        description="A dark supernatural manga about identity, fear, and ghouls.",
        price=13.20,
        image_url="https://placehold.co/600x800?text=Tokyo+Ghoul",
        volume=1,
        genre="Supernatural",
        in_stock=False,
    ),
    ProductOut(
        id=5,
        title="Attack on Titan",
        description="A famous action manga about humanity fighting giant titans.",
        price=15.00,
        image_url="https://placehold.co/600x800?text=Attack+on+Titan",
        volume=1,
        genre="Action",
        in_stock=True,
    ),
]

_next_id = 6


def list_products() -> list[ProductOut]:
    return _products


def get_product(product_id: int) -> ProductOut | None:
    for product in _products:
        if product.id == product_id:
            return product
    return None


def create_product(payload: ProductCreate) -> ProductOut:
    global _next_id

    product = ProductOut(
        id=_next_id,
        title=payload.title,
        description=payload.description,
        price=payload.price,
        image_url=payload.image_url,
        volume=payload.volume,
        genre=payload.genre,
        in_stock=payload.in_stock,
    )

    _products.append(product)
    _next_id += 1
    return product