from pydantic import BaseModel, validator, EmailStr
from datetime import date
from typing import Optional
from ..models.user import City, Gender, Citizenship
import re

class UserBase(BaseModel):
    birth_year: int
    city: City
    gender: Gender
    citizenship: Citizenship
    phone_number: str

    @validator('birth_year')
    def validate_age(cls, v):
        current_year = date.today().year
        if current_year - v < 18:
            raise ValueError('Пользователь должен быть старше 18 лет')
        if v < 1900 or v > current_year:
            raise ValueError('Некорректный год рождения')
        return v

    @validator('phone_number')
    def validate_phone(cls, v):
        # Удаляем все нецифровые символы
        phone = re.sub(r'\D', '', v)
        if len(phone) != 11:
            raise ValueError('Номер телефона должен содержать 11 цифр')
        if not phone.startswith('7') and not phone.startswith('8'):
            raise ValueError('Номер телефона должен начинаться с 7 или 8')
        return phone

class UserCreate(UserBase):
    password: str

class UserPassword(BaseModel):
    password: str
    confirm_password: str

    @validator('confirm_password')
    def passwords_match(cls, v, values, **kwargs):
        if 'password' in values and v != values['password']:
            raise ValueError('Пароли не совпадают')
        return v

class User(UserBase):
    id: int
    user_id: str
    registration_date: date

    class Config:
        from_attributes = True

class UserResponse(BaseModel):
    user_id: str
    message: str = "Регистрация успешна" 