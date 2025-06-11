from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import engine, Base
from .models import user as user_model
from .routes import users

# Создаем таблицы в базе данных
Base.metadata.create_all(bind=engine)

app = FastAPI(title="User Registration System")

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Разрешаем все origins для отладки
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключаем маршруты
app.include_router(users.router)

@app.get("/")
async def root():
    return {"message": "Добро пожаловать в систему регистрации пользователей!"} 