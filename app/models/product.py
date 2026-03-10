from pydantic import BaseModel, Field


class ProductCreate(BaseModel):
    title: str = Field(min_length=2, max_length=120)
    description: str = Field(min_length=10, max_length=1000)
    price: float = Field(gt=0)
    image_url: str = Field(default="https://placehold.co/600x800?text=Manga")
    volume: int = Field(ge=1)
    genre: str = Field(min_length=2, max_length=50)
    in_stock: bool = True


class ProductOut(BaseModel):
    id: int
    title: str
    description: str
    price: float
    image_url: str
    volume: int
    genre: str
    in_stock: bool