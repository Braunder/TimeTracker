# Time Tracker API

API на Flask для учета рабочего времени сотрудников по проектам.

## Возможности

- Аутентификация и авторизация пользователей
- Управление проектами
- Учет рабочего времени
- Генерация отчетов для менеджеров
- Интерактивная документация API

## Требования

- Python 3.8+
- SQLite (для разработки)
- Just (управление командами)

## Установка

1. Клонируйте репозиторий
2. Создайте и активируйте виртуальное окружение:
```bash
python -m venv venv
source venv/bin/activate  # В Windows: .\venv\Scripts\activate
```

3. Установите зависимости:
```bash
pip install -r requirements.txt
```

4. Инициализируйте базу данных:
```bash
flask init-db
```

## Запуск приложения

Для запуска сервера разработки:
```bash
flask run
```

Приложение будет доступно по адресу `http://localhost:5000/api/`

## Документация API

Посетите `http://localhost:5000/api/` для просмотра интерактивной документации API.

### Аутентификация
- POST `/api/auth/register` - Регистрация нового пользователя
- POST `/api/auth/login` - Вход в систему и получение токена доступа

### Проекты
- GET `/api/projects` - Получение списка всех проектов
- POST `/api/projects` - Создание нового проекта

### Учет времени
- GET `/api/time-entries` - Получение записей о времени пользователя
- POST `/api/time-entries` - Создание новой записи о времени

### Отчеты
- GET `/api/reports/project/<project_id>` - Получение отчета по проекту (только для менеджеров)

## Тестирование

Запуск тестов:
```bash
pytest
```

## Качество кода

Запуск линтеров:
```bash
flake8 .
black . --check
isort . --check-only
```

Форматирование кода:
```bash
black .
isort .
```

## Структура проекта

```
.
├── app/
│   ├── __init__.py
│   ├── config.py
│   ├── models.py
│   ├── routes.py
│   ├── commands.py
│   └── templates/
│       └── index.html
├── tests/
│   └── test_api.py
├── requirements.txt
├── run.py
└── justfile
``` 