# Time Tracker API

A Flask-based REST API for tracking employee work time across different projects.

## Features

- User authentication with JWT tokens
- Project management (CRUD operations)
- Time entry tracking
- Project time reports for managers
- Swagger UI documentation
- Role-based access control (regular users and managers)

## Tech Stack

- Python 3.8+
- Flask 3.0.2
- SQLAlchemy (Database ORM)
- Flask-JWT-Extended (Authentication)
- Flask-RESTX (API documentation)
- Marshmallow (Data validation)
- SQLite (Database)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/timetracker.git
cd timetracker
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
# On Windows
venv\Scripts\activate
# On Unix or MacOS
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables (create .env file):
```env
FLASK_APP=run.py
FLASK_ENV=development
SECRET_KEY=your-secret-key
DATABASE_URL=sqlite:///timetracker.db
```

5. Initialize the database:
```bash
flask init-db
```

## Running the Application

1. Start the development server:
```bash
flask run
```

2. Access the API documentation at `http://localhost:5000/`

## API Endpoints

### Authentication

- `POST /api/auth/register` - Register a new user
- `POST /api/auth/login` - Login and get JWT token

### Projects

- `GET /api/projects` - Get all projects
- `POST /api/projects` - Create a new project
- `GET /api/projects/{id}` - Get project details
- `PUT /api/projects/{id}` - Update project
- `DELETE /api/projects/{id}` - Delete project

### Time Entries

- `GET /api/time-entries` - Get user's time entries
- `POST /api/time-entries` - Create a new time entry
- `GET /api/time-entries/{id}` - Get time entry details
- `PUT /api/time-entries/{id}` - Update time entry
- `DELETE /api/time-entries/{id}` - Delete time entry

### Reports

- `GET /api/reports/project/{project_id}` - Get project time report (managers only)

## API Models

### User
```json
{
  "username": "string",
  "email": "string",
  "password": "string",
  "is_manager": false
}
```

### Project
```json
{
  "name": "string",
  "description": "string"
}
```

### Time Entry
```json
{
  "project_id": 1,
  "date": "2024-02-14",
  "hours": 8.0
}
```

## Authentication

The API uses JWT tokens for authentication. To access protected endpoints:

1. Login to get the token
2. Add the token to request headers:
```
Authorization: Bearer <your-token>
```

## Development

### Running Tests
```bash
pytest
```

### Code Style
The project uses:
- flake8 for linting
- black for code formatting
- isort for import sorting

To check code style:
```bash
flake8 .
black .
isort .
```

## Project Structure

```
timetracker/
├── app/
│   ├── __init__.py
│   ├── config.py
│   ├── models.py
│   ├── routes.py
│   ├── schemas.py
│   └── templates/
│       └── index.html
├── tests/
│   └── test_api.py
├── .env
├── .gitignore
├── README.md
├── README_ru.md
├── requirements.txt
└── run.py
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 