# Run the test suite
test:
	poetry run pytest

# Format the code using Black
format:
	poetry run black .

# Lint the code using Flake8
lint:
	poetry run flake8 .

# Run all quality checks: formatting, linting, and tests
check: format lint test
