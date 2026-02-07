.PHONY: help install install-dev test test-coverage lint format clean build docs

# Default target
help:
	@echo "UnifoLM-WMA-0 Makefile"
	@echo "======================"
	@echo ""
	@echo "Available targets:"
	@echo "  help           - Show this help message"
	@echo "  install        - Install the package"
	@echo "  install-dev    - Install the package with development dependencies"
	@echo "  test           - Run tests"
	@echo "  test-coverage  - Run tests with coverage report"
	@echo "  lint           - Run linters (flake8)"
	@echo "  format         - Format code with black and isort"
	@echo "  format-check   - Check code formatting without modifying"
	@echo "  clean          - Remove build artifacts and cache files"
	@echo "  build          - Build the package"
	@echo "  pre-commit     - Install pre-commit hooks"
	@echo "  check-all      - Run all checks (format-check, lint, test)"
	@echo ""

# Install the package
install:
	pip install -e .
	cd external/dlimp && pip install -e .

# Install with development dependencies
install-dev:
	pip install -e ".[dev]"
	cd external/dlimp && pip install -e .
	@echo ""
	@echo "Development dependencies installed!"
	@echo "Run 'make pre-commit' to install git hooks."

# Install pre-commit hooks
pre-commit:
	pip install pre-commit
	pre-commit install
	@echo "Pre-commit hooks installed successfully!"

# Run tests
test:
	pytest tests/ -v

# Run tests with coverage
test-coverage:
	pytest tests/ -v --cov=unifolm_wma --cov-report=html --cov-report=term
	@echo ""
	@echo "Coverage report generated in htmlcov/index.html"

# Run linters
lint:
	@echo "Running flake8..."
	flake8 src/ scripts/ tests/
	@echo "✓ Linting passed!"

# Format code
format:
	@echo "Formatting code with black..."
	black src/ scripts/ tests/ --line-length 100
	@echo "Sorting imports with isort..."
	isort src/ scripts/ tests/ --profile black --line-length 100
	@echo "✓ Code formatted!"

# Check formatting without modifying
format-check:
	@echo "Checking code formatting..."
	black src/ scripts/ tests/ --check --line-length 100
	isort src/ scripts/ tests/ --check-only --profile black --line-length 100
	@echo "✓ Format check passed!"

# Clean build artifacts and cache
clean:
	@echo "Cleaning build artifacts and cache files..."
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info
	rm -rf .eggs/
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.so" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	rm -rf .pytest_cache/
	rm -rf .coverage
	rm -rf htmlcov/
	rm -rf .mypy_cache/
	@echo "✓ Cleanup complete!"

# Build package
build: clean
	@echo "Building package..."
	python -m build
	@echo "✓ Build complete!"

# Run all checks
check-all: format-check lint test
	@echo ""
	@echo "================================"
	@echo "✓ All checks passed successfully!"
	@echo "================================"

# Quick setup for new contributors
setup: install-dev pre-commit
	@echo ""
	@echo "================================"
	@echo "✓ Setup complete!"
	@echo "================================"
	@echo ""
	@echo "You're ready to contribute!"
	@echo "Run 'make help' to see available commands."
	@echo "Run 'make check-all' before committing your changes."
