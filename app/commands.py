# Импорт необходимых модулей
import click
from app import db
from app.models import User, Project, TimeEntry

def init_db():
    # Инициализация базы данных (создание таблиц)
    db.create_all()
    click.echo('Initialized the database.') 