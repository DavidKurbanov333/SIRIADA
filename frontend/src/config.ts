const config = {
    apiUrl: process.env.NODE_ENV === 'production' 
        ? 'https://api.siriada.ru'  // URL API в продакшене
        : 'http://localhost:8000',  // URL API в разработке
    environment: process.env.NODE_ENV || 'development',
    version: '1.0.0'
};

export default config; 