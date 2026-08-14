# product schemas for the api and forms
from pydantic import BaseModel, Field


# data for creating a product
class ProductCreate(BaseModel):
    title: str = Field(min_length=2, max_length=120)
    description: str = Field(min_length=10, max_length=1000)
    price: float = Field(gt=0)
    image_url: str = Field(default="https://placehold.co/600x800?text=Manga")
    volume: int = Field(ge=1)
    genre: str = Field(min_length=2, max_length=50)
    in_stock: bool = True


class ProductOut(BaseModel):
    # product id
    id: int
    # title
    title: str
    # description
    description: str
    # price
    price: float
    # image
    image_url: str
    # volume
    volume: int
    # genre
    genre: str
    # in stock
    in_stock: bool

    class Config:
        # Allow building the response from an ORM object.
        from_attributes = True


# data for editing a product
class ProductUpdate(BaseModel):
    title: str = Field(min_length=2, max_length=120)
    description: str = Field(min_length=10, max_length=1000)
    price: float = Field(gt=0)
    image_url: str = Field(default="https://placehold.co/600x800?text=Manga")
    volume: int = Field(ge=1)
    genre: str = Field(min_length=2, max_length=50)
    in_stock: bool = True
