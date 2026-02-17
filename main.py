from fastapi import FastAPI

# Создаем экземпляр приложения
app = FastAPI(title="Мое FastAPI приложение")

# Корневой маршрут
@app.get("/")
async def root():
    return {"message": "Hello World from WSL and FastAPI!"}

# Маршрут с параметром
@app.get("/items/{item_id}")
async def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}
