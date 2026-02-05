# Tests Directory

This directory contains tests for the UnifoLM-WMA package.

## Running Tests

### Install test dependencies

```bash
pip install -e ".[test]"
```

### Run all tests

```bash
pytest
```

### Run tests with coverage

```bash
pytest --cov=unifolm_wma --cov-report=html
```

### Run specific test file

```bash
pytest tests/test_imports.py
```

## Test Structure

- `test_imports.py` - Basic import tests to verify package structure
- Additional test files will be added as functionality is tested

## Writing Tests

- Test files should be named `test_*.py`
- Test functions should be named `test_*`
- Use pytest fixtures for common setup
- Add docstrings to explain what each test verifies
