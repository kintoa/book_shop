from fastapi import FastAPI
from settings import settings
from shop_api import router
from db import database

app = FastAPI(title=settings.app_name)

app.include_router(router)

@app.on_event("startup")
async def startup_event():
    await database.init_db()  # Инициализация базы данных при старте приложения