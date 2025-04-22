# Импорт необходимых модулей
from app import create_app
from app.commands import init_db

# Создание приложения
app = create_app()

# Регистрация команды для инициализации базы данных
@app.cli.command('init-db')
def init_db_command():
    init_db() 