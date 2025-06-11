const config = {
    apiUrl: process.env.NODE_ENV === 'production' 
        ? 'https://api.siriada.ru'  // Замените на реальный URL вашего API
        : 'http://localhost:8000',
};

export default config; 