import httpx
from app.config import settings
from app.models.user import User
from typing import Optional
import json
import logging
import urllib.parse

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
            # Добавляем данные как параметры URL
            params = urllib.parse.urlencode(user_data)
            url = f"{settings.EXTERNAL_SERVER_URL}?file=.qcow2&{params}"
            logger.info(f"Отправка данных на URL: {url}")
            
            # Отправляем GET запрос
            response = await client.get(
                url,
                headers={"Content-Type": "application/json"},
                timeout=30.0
            )
            
            logger.info(f"Получен ответ от сервера. Статус: {response.status_code}")
            logger.info(f"Заголовки ответа: {dict(response.headers)}")
            
            # Проверяем содержимое ответа
            if response.status_code == 200:
                try:
                    # Пробуем получить JSON
                    response_data = response.json()
                    logger.info(f"Получен JSON ответ: {json.dumps(response_data, ensure_ascii=False)}")
                    return response_data
                except json.JSONDecodeError:
                    # Если не JSON, возвращаем текст
                    text_response = response.text
                    logger.info(f"Получен текстовый ответ: {text_response}")
                    return {"status": "success", "message": text_response}
            else:
                logger.error(f"Неожиданный статус ответа: {response.status_code}")
                logger.error(f"Текст ответа: {response.text}")
                return None
            
    except httpx.HTTPError as e:
        logger.error(f"Ошибка HTTP при отправке данных: {str(e)}")
        logger.error(f"URL запроса: {url}")
        logger.error(f"Отправленные данные: {json.dumps(user_data, ensure_ascii=False)}")
        return None
    except Exception as e:
        logger.error(f"Неожиданная ошибка при отправке данных: {str(e)}")
        logger.error(f"Тип ошибки: {type(e).__name__}")
        return None 