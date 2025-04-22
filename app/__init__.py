# Импорт необходимых модулей
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_restx import Api
from datetime import timedelta
import os

# Инициализация расширений Flask
db = SQLAlchemy()  # ORM для работы с базой данных
migrate = Migrate()  # Миграции базы данных
jwt = JWTManager()  # JWT аутентификация

# Определение авторизации для Swagger UI
authorizations = {
    'Bearer': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization',
        'description': 'Введите токен в формате: Bearer <token>'
    }
}

# Инициализация API с авторизацией
api = Api(
    title='Time Tracker API',
    version='1.0',
    description='API для учета рабочего времени сотрудников',
    authorizations=authorizations,
    security='Bearer',
    doc='/'
)

def create_app():
    # Создание экземпляра приложения Flask
    app = Flask(__name__)
    app.config.from_object('app.config.Config')
    
    # Установка пути к папке с шаблонами
    app.template_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')

    # Инициализация расширений
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    # Регистрация namespace
    from app.routes import ns
    api.add_namespace(ns)
    
    # Инициализация API
    api.init_app(app)

    return app 