# List available commands
default:
    @just --list

# Set up and run the project
up:
    python -m venv venv
    . venv/bin/activate
    pip install -r requirements.txt
    flask init-db
    flask run

# Run tests
test:
    pytest

# Run linters
lint:
    flake8 .
    black .
    isort .

# Format code
format:
    black .
    isort .

# Clean up python cache files
clean:
    find . -type d -name "__pycache__" -exec rm -r {} +
    find . -type f -name "*.pyc" -delete
    find . -type f -name "*.pyo" -delete
    find . -type f -name "*.pyd" -delete
    find . -type f -name ".coverage" -delete
    find . -type d -name "*.egg-info" -exec rm -r {} +
    find . -type d -name "*.egg" -exec rm -r {} +
    find . -type d -name ".pytest_cache" -exec rm -r {} +
    find . -type d -name ".tox" -exec rm -r {} +
    find . -type d -name ".eggs" -exec rm -r {} +

# Install pre-commit hooks
setup-hooks:
    pre-commit install

# Run all checks (tests and linting)
check: test lint 