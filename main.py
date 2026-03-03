from fastapi import FastAPI
from app.routers import items

app = FastAPI(title="fastapi-webapp")

app.include_router(items.router)