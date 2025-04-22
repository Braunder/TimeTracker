# Импорт необходимых модулей
import pytest
from app import create_app, db
from app.models import User, Project, TimeEntry
from datetime import datetime, date

@pytest.fixture
def app():
    # Создание тестового приложения
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    # Создание тестового клиента
    return app.test_client()

@pytest.fixture
def runner(app):
    # Создание тестового runner для CLI команд
    return app.test_cli_runner()

def test_register_user(client):
    # Тест регистрации пользователя
    response = client.post('/api/auth/register', json={
        'username': 'testuser',
        'email': 'test@example.com',
        'password': 'testpass',
        'is_manager': False
    })
    assert response.status_code == 201
    assert User.query.filter_by(username='testuser').first() is not None

def test_login_user(client):
    # Тест входа пользователя
    # Сначала регистрируем пользователя
    client.post('/api/auth/register', json={
        'username': 'testuser',
        'email': 'test@example.com',
        'password': 'testpass',
        'is_manager': False
    })
    
    # Затем пробуем войти
    response = client.post('/api/auth/login', json={
        'username': 'testuser',
        'password': 'testpass'
    })
    assert response.status_code == 200
    assert 'access_token' in response.json

def test_create_project(client):
    # Тест создания проекта
    # Регистрируем и входим как пользователь
    client.post('/api/auth/register', json={
        'username': 'testuser',
        'email': 'test@example.com',
        'password': 'testpass',
        'is_manager': False
    })
    login_response = client.post('/api/auth/login', json={
        'username': 'testuser',
        'password': 'testpass'
    })
    token = login_response.json['access_token']
    
    # Создаем проект
    response = client.post('/api/projects', 
        json={'name': 'Test Project', 'description': 'Test Description'},
        headers={'Authorization': f'Bearer {token}'}
    )
    assert response.status_code == 201
    assert Project.query.filter_by(name='Test Project').first() is not None 