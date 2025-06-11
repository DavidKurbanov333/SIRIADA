from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import engine, Base
from .models import user as user_model
from .routes import users
import os

# Создаем таблицы в базе данных
Base.metadata.create_all(bind=engine)

app = FastAPI(title="SIRIADA API")

# Настройка CORS
origins = [
    "http://localhost:3000",  # Для разработки
    "https://siriada.ru",     # Основной домен
    "https://www.siriada.ru", # www поддомен
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключаем маршруты
app.include_router(users.router, prefix="/users", tags=["users"])

@app.get("/")
async def root():
    return {"message": "Welcome to SIRIADA API"} 