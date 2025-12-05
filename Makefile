# Minimum coverage percentage required for tests to pass
COVERAGE_FAIL = 50

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

# Run tests with coverage enforcement (terminal output only)
coverage:
	poetry run pytest --cov=template --cov-report=term --cov-fail-under=$(COVERAGE_FAIL)

# Run tests with coverage and produce an HTML report
coverage-html:
	poetry run pytest --cov=template --cov-report=html --cov-fail-under=$(COVERAGE_FAIL)
	@echo "HTML coverage report generated at htmlcov/index.html"
