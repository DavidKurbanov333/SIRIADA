from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..models import user as user_model
from ..schemas import user as user_schema
from ..utils.id_generator import generate_id
from passlib.context import CryptContext

router = APIRouter(
    tags=["users"]
)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

@router.post("/register", response_model=user_schema.UserResponse)
def create_user(user: user_schema.UserCreate, db: Session = Depends(get_db)):
    # Генерируем user_id
    user_id = generate_id(user.gender, user.city)
    
    # Проверяем, не существует ли уже такой ID
    while db.query(user_model.User).filter(user_model.User.user_id == user_id).first():
        user_id = generate_id(user.gender, user.city)
    
    # Создаем хеш пароля
    hashed_password = get_password_hash(user.password)
    
    # Создаем пользователя
    db_user = user_model.User(
        user_id=user_id,
        birth_year=user.birth_year,
        city=user.city,
        gender=user.gender,
        citizenship=user.citizenship,
        phone_number=user.phone_number,
        password_hash=hashed_password
    )
    
    try:
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return {"user_id": user_id, "message": "Регистрация успешна"}
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ошибка при создании пользователя"
        )

@router.get("/", response_model=List[user_schema.User])
def get_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = db.query(user_model.User).offset(skip).limit(limit).all()
    return users

@router.get("/{user_id}", response_model=user_schema.User)
def get_user(user_id: str, db: Session = Depends(get_db)):
    user = db.query(user_model.User).filter(user_model.User.user_id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    return user 