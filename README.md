# SIRIADA - Форма регистрации

Проект представляет собой форму регистрации пользователей для сайта SIRIADA, состоящую из:
- Backend API на FastAPI (Python)
- Frontend на React (TypeScript)
- База данных SQLite

## Структура проекта

```
SIRIADA_1/
├── backend/           # FastAPI backend
│   ├── app/
│   │   ├── models/    # SQLAlchemy модели
│   │   ├── routes/    # API endpoints
│   │   ├── schemas/   # Pydantic схемы
│   │   └── main.py    # Точка входа
│   └── requirements.txt
└── frontend/         # React frontend
    ├── src/
    │   ├── components/
    │   ├── types/
    │   └── App.tsx
    └── package.json
```

## Установка и запуск

### Backend

```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Frontend

```bash
cd frontend
npm install
npm start
```

## API Endpoints

- `POST /api/users/register` - Регистрация нового пользователя
- `GET /api/users/{user_id}` - Получение информации о пользователе

## Технологии

- Backend:
  - FastAPI
  - SQLAlchemy
  - Pydantic
  - SQLite

- Frontend:
  - React
  - TypeScript
  - Material-UI
  - Formik
  - Yup 