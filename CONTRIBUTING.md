# Contributing to UnifoLM-WMA

Thank you for your interest in contributing to UnifoLM-WMA! This document provides guidelines for contributing to the project.

## How to Contribute

### Reporting Issues

If you find a bug or have a suggestion:

1. Check if the issue already exists in the [GitHub Issues](https://github.com/unitreerobotics/unifolm-world-model-action/issues)
2. If not, create a new issue with:
   - A clear, descriptive title
   - Detailed description of the problem
   - Steps to reproduce (for bugs)
   - Expected vs actual behavior
   - Your environment (OS, Python version, etc.)

### Submitting Changes

1. Fork the repository
2. Create a new branch (`git checkout -b feature/your-feature-name`)
3. Make your changes
4. Run tests to ensure nothing is broken
5. Commit your changes with clear commit messages
6. Push to your fork
7. Submit a pull request

## Development Setup

### Install Development Dependencies

```bash
# Create and activate conda environment
conda create -n unifolm-wma python==3.10.18
conda activate unifolm-wma

# Install project with development dependencies
pip install -e ".[dev]"
```

### Running Tests

Before submitting a pull request, make sure all tests pass:

```bash
# Run all tests
pytest

# Run tests with coverage
pytest --cov=unifolm_wma --cov-report=html

# Run specific test file
pytest tests/test_imports.py
```

## Code Style

### Python Code Style

- Follow [PEP 8](https://pep8.org/) style guide
- Use meaningful variable and function names
- Add docstrings to all functions and classes
- Maximum line length: 100 characters

### Code Formatting

We use the following tools for code quality:

```bash
# Format code with black
black src/

# Sort imports with isort
isort src/

# Check code quality with flake8
flake8 src/
```

## Commit Messages

Write clear, concise commit messages:

- Use present tense ("Add feature" not "Added feature")
- Start with a capital letter
- Limit first line to 72 characters
- Reference issues when applicable (#123)

### Examples

Good commit messages:
```
Add support for custom camera configurations
Fix memory leak in video processing
Update documentation for training pipeline
```

## Pull Request Process

1. Update README.md if you're adding new features
2. Add tests for new functionality
3. Ensure all tests pass
4. Update documentation as needed
5. Request review from maintainers

## Areas for Contribution

We welcome contributions in the following areas:

### High Priority

- Adding more unit tests and integration tests
- Improving documentation and examples
- Bug fixes and performance improvements
- Adding support for new robot models
- Improving error messages and logging

### Medium Priority

- Adding new training configurations
- Creating tutorials and guides
- Improving visualization tools
- Adding dataset converters

### Lower Priority

- Code refactoring
- Style improvements
- Documentation translations

## Questions?

If you have questions about contributing:

- Check existing documentation
- Look for similar issues or pull requests
- Open a discussion in GitHub Discussions
- Contact the maintainers

## Code of Conduct

### Our Standards

- Be respectful and inclusive
- Welcome newcomers and help them learn
- Focus on what is best for the community
- Show empathy towards other community members

### Unacceptable Behavior

- Harassment or discriminatory language
- Personal attacks or trolling
- Publishing private information
- Other conduct inappropriate for a professional setting

## License

By contributing, you agree that your contributions will be licensed under the BSD-3-Clause License.

## Recognition

Contributors will be recognized in:
- The project's contributors list
- Release notes for significant contributions
- The project's acknowledgments section

Thank you for helping make UnifoLM-WMA better!
