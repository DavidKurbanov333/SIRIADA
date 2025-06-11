import random
import string
from typing import Dict, List

gender_codes: Dict[str, List[str]] = {
    'мужской': ['Q', 'D'],
    'женский': ['V', 'H']
}

city_codes: Dict[str, List[str]] = {
    'Москва/МО': ['5', '9'],
    'Санкт-Петербург/ЛО': ['1', '3'],
    'Ярославль': ['0', '2']
}

def generate_id(gender: str, city: str) -> str:
    """
    Генерирует уникальный ID на основе пола и города.
    
    Args:
        gender: Пол пользователя ('мужской' или 'женский')
        city: Город пользователя
        
    Returns:
        str: Сгенерированный ID в формате {gender_code}{random_letters}{city_code}{random_digits}
    """
    gender_code = random.choice(gender_codes[gender.lower()])
    random_letters = ''.join(random.choices(string.ascii_uppercase, k=2))
    
    city_code = random.choice(city_codes[city])
    random_digits = ''.join(random.choices(string.digits, k=2))
    
    return f"{gender_code}{random_letters}{city_code}{random_digits}" 