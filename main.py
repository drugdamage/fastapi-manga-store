from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.routers import items, pages

app = FastAPI(title="Manga Store MVP")

app.mount("/static", StaticFiles(directory="app/static"), name="static")

app.include_router(pages.router)
app.include_router(items.router, prefix="/api")