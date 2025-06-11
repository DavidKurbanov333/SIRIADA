from sqlalchemy import Column, Integer, String, Date, UniqueConstraint
from sqlalchemy.sql import func
from datetime import date
import enum
from ..database import Base

class City(str, enum.Enum):
    YAROSLAVL = "Ярославль"
    MOSCOW = "Москва/МО"
    SPB = "Санкт-Петербург/ЛО"

class Gender(str, enum.Enum):
    MALE = "мужской"
    FEMALE = "женский"

class Citizenship(str, enum.Enum):
    RF = "РФ"
    CIS = "СНГ"
    OTHER = "другое"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, unique=True, index=True, nullable=False)
    birth_year = Column(Integer, nullable=False)
    city = Column(String, nullable=False)
    gender = Column(String, nullable=False)
    citizenship = Column(String, nullable=False)
    phone_number = Column(String, nullable=False)
    password_hash = Column(String, nullable=False)
    registration_date = Column(Date, default=date.today)

    __table_args__ = (
        UniqueConstraint('user_id', name='unique_user_id'),
    )

    def __repr__(self):
        return f"<User(user_id={self.user_id}, birth_year={self.birth_year}, city={self.city}, gender={self.gender}, citizenship={self.citizenship}, phone_number={self.phone_number}, registration_date={self.registration_date})>"

    def is_adult(self):
        current_year = date.today().year
        return current_year - self.birth_year >= 18 