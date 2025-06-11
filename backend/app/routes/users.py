from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import logging
from ..database import get_db
from ..models import user as user_model
from ..schemas import user as user_schema
from ..utils.id_generator import generate_id
from ..services.external_service import send_user_data_to_external_server
from passlib.context import CryptContext

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter(
    tags=["users"]
)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

@router.post("/register", response_model=user_schema.UserResponse)
async def create_user(user: user_schema.UserCreate, db: Session = Depends(get_db)):
    try:
        logger.info(f"Получены данные для регистрации: {user.dict(exclude={'password'})}")
        
        # Генерируем user_id
        user_id = generate_id(user.gender, user.city)
        logger.info(f"Сгенерирован user_id: {user_id}")
        
        # Проверяем, не существует ли уже такой ID
        while db.query(user_model.User).filter(user_model.User.user_id == user_id).first():
            user_id = generate_id(user.gender, user.city)
            logger.info(f"ID занят, сгенерирован новый: {user_id}")
        
        # Создаем хеш пароля
        hashed_password = get_password_hash(user.password)
        
        # Создаем пользователя
        db_user = user_model.User(
            user_id=user_id,
            birth_year=user.birth_year,
            city=user.city,
            gender=user.gender,
            citizenship=user.citizenship,
            password_hash=hashed_password
        )
        
        logger.info("Попытка сохранения пользователя в БД")
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        logger.info(f"Пользователь успешно создан с ID: {user_id}")

        # Отправляем данные на внешний сервер
        try:
            external_response = await send_user_data_to_external_server(db_user, user.password)
            if external_response:
                logger.info(f"Данные успешно отправлены на внешний сервер: {external_response}")
                # Добавляем информацию об отправке в ответ
                return {
                    "user_id": user_id, 
                    "message": "Регистрация успешна",
                    "external_server_status": "success"
                }
            else:
                logger.warning("Не удалось отправить данные на внешний сервер")
                # Возвращаем успешную регистрацию даже если внешний сервер недоступен
                return {
                    "user_id": user_id, 
                    "message": "Регистрация успешна (данные сохранены локально)",
                    "external_server_status": "failed"
                }
        except Exception as e:
            logger.error(f"Ошибка при отправке данных на внешний сервер: {str(e)}")
            # Возвращаем успешную регистрацию даже при ошибке внешнего сервера
            return {
                "user_id": user_id, 
                "message": "Регистрация успешна (данные сохранены локально)",
                "external_server_status": "error",
                "error_details": str(e)
            }
    except Exception as e:
        logger.error(f"Ошибка при создании пользователя: {str(e)}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Ошибка при создании пользователя: {str(e)}"
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