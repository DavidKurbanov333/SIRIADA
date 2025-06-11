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

    @validator('birth_year')
    def validate_age(cls, v):
        current_year = date.today().year
        if current_year - v < 18:
            raise ValueError('Пользователь должен быть старше 18 лет')
        if v < 1900 or v > current_year:
            raise ValueError('Некорректный год рождения')
        return v

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