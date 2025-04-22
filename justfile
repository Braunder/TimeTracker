# Project management commands
set dotenv-load := true
set shell := ["powershell.exe", "-Command"]

# Start the application
up:
    @echo "Starting the application..."
    flask run

# Run tests
test:
    @echo "Running tests..."
    pytest

# Run linters
lint:
    @echo "Running linters..."
    flake8 .
    black . --check
    isort . --check-only

# Format code
format:
    @echo "Formatting code..."
    black .
    isort .

# Install dependencies
install:
    @echo "Installing dependencies..."
    pip install -r requirements.txt

# Initialize database
init-db:
    @echo "Initializing database..."
    flask init-db 