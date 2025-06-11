# Сириада - Система Регистрации

Система для регистрации, предоставляющая уникальные идентификаторы для каждого пользователя.

## Технологии

### Backend
- FastAPI
- SQLAlchemy
- SQLite
- Python 3.8+

### Frontend
- React
- Material-UI
- Axios
- Node.js 14+

## Установка и запуск

### Backend

1. Перейдите в директорию backend:
```bash
cd backend
```

2. Создайте виртуальное окружение и активируйте его:
```bash
python -m venv venv
source venv/bin/activate  # для Linux/Mac
venv\Scripts\activate     # для Windows
```

3. Установите зависимости:
```bash
pip install -r requirements.txt
```

4. Запустите сервер:
```bash
uvicorn app.main:app --reload
```

Сервер будет доступен по адресу: http://localhost:8000

### Frontend

1. Перейдите в директорию frontend:
```bash
cd frontend
```

2. Установите зависимости:
```bash
npm install
```

3. Запустите сервер разработки:
```bash
npm start
```

Приложение будет доступно по адресу: http://localhost:3000

## API Endpoints

- `POST /users/register` - Регистрация нового пользователя
- `GET /users/{user_id}` - Получение информации о пользователе
- `GET /docs` - Swagger документация API

## Деплой

### Backend
Для деплоя бэкенда рекомендуется использовать:
- PythonAnywhere
- Heroku
- DigitalOcean

### Frontend
Для деплоя фронтенда рекомендуется использовать:
- Vercel
- Netlify
- GitHub Pages

## Лицензия

MIT 
