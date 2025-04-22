# Импорт необходимых модулей
import os
from datetime import timedelta

class Config:
    # Настройки Flask
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev')  # Секретный ключ для подписи сессий
    
    # Настройки базы данных
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///timetracker.db')  # URL базы данных
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # Отключение отслеживания изменений
    
    # Настройки JWT
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'jwt-secret-key')  # Секретный ключ для JWT
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)  # Время жизни токена
    
    # Другие настройки
    DEBUG = os.environ.get('FLASK_DEBUG', 'True').lower() == 'true'  # Режим отладки 