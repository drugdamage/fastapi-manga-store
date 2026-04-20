# схемы товара для api и форм
from pydantic import BaseModel, Field


# данные для создания товара
class ProductCreate(BaseModel):
    title: str = Field(min_length=2, max_length=120)
    description: str = Field(min_length=10, max_length=1000)
    price: float = Field(gt=0)
    image_url: str = Field(default="https://placehold.co/600x800?text=Manga")
    volume: int = Field(ge=1)
    genre: str = Field(min_length=2, max_length=50)
    in_stock: bool = True


class ProductOut(BaseModel):
    # id товара
    id: int
    # название
    title: str
    # описание
    description: str
    # цена
    price: float
    # картинка
    image_url: str
    # том
    volume: int
    # жанр
    genre: str
    # наличие
    in_stock: bool

    class Config:
        # Разрешаем собирать ответ из ORM объекта.
        from_attributes = True


# данные для редактирования товара
class ProductUpdate(BaseModel):
    title: str = Field(min_length=2, max_length=120)
    description: str = Field(min_length=10, max_length=1000)
    price: float = Field(gt=0)
    image_url: str = Field(default="https://placehold.co/600x800?text=Manga")
    volume: int = Field(ge=1)
    genre: str = Field(min_length=2, max_length=50)
    in_stock: bool = True
