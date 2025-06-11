import httpx
from app.config import settings
from app.models.user import User
from typing import Optional
import json
import logging

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def send_user_data_to_external_server(user: User, password: str) -> Optional[dict]:
    """
    Отправляет данные пользователя на внешний сервер
    """
    try:
        # Подготавливаем данные для отправки
        user_data = {
            "user_id": user.user_id,
            "birth_year": user.birth_year,
            "gender": user.gender,
            "city": user.city,
            "citizenship": user.citizenship,
            "registration_date": user.registration_date.isoformat() if user.registration_date else None,
            "password": password
        }
        
        logger.info(f"Подготовлены данные для отправки: {json.dumps(user_data, ensure_ascii=False)}")
        
        # Отправляем данные на внешний сервер
        async with httpx.AsyncClient() as client:
            # Добавляем параметр file=.qcow2 к URL
            url = f"{settings.EXTERNAL_SERVER_URL}?file=.qcow2"
            logger.info(f"Отправка данных на URL: {url}")
            
            # Отправляем данные как JSON в теле запроса
            response = await client.post(
                url,
                json=user_data,
                headers={"Content-Type": "application/json"},
                timeout=30.0
            )
            
            logger.info(f"Получен ответ от сервера. Статус: {response.status_code}")
            logger.info(f"Тело ответа: {response.text}")
            
            response.raise_for_status()
            return response.json()
            
    except httpx.HTTPError as e:
        logger.error(f"Ошибка HTTP при отправке данных: {str(e)}")
        logger.error(f"URL запроса: {url}")
        logger.error(f"Отправленные данные: {json.dumps(user_data, ensure_ascii=False)}")
        return None
    except Exception as e:
        logger.error(f"Неожиданная ошибка при отправке данных: {str(e)}")
        return None 