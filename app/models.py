# Импорт необходимых модулей
from app import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    # Модель пользователя
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)  # Уникальное имя пользователя
    email = db.Column(db.String(120), unique=True, nullable=False)  # Уникальный email
    password_hash = db.Column(db.String(128))  # Хеш пароля
    is_manager = db.Column(db.Boolean, default=False)  # Флаг менеджера
    time_entries = db.relationship('TimeEntry', backref='user', lazy=True)  # Связь с записями времени

    def set_password(self, password):
        # Хеширование пароля
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        # Проверка пароля
        return check_password_hash(self.password_hash, password)

class Project(db.Model):
    # Модель проекта
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)  # Название проекта
    description = db.Column(db.Text)  # Описание проекта
    time_entries = db.relationship('TimeEntry', backref='project', lazy=True)  # Связь с записями времени

class TimeEntry(db.Model):
    # Модель записи о времени
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # Связь с пользователем
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)  # Связь с проектом
    date = db.Column(db.Date, nullable=False)  # Дата записи
    hours = db.Column(db.Float, nullable=False)  # Количество часов
    created_at = db.Column(db.DateTime, default=datetime.utcnow)  # Время создания записи 