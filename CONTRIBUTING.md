# Contributing to AlertTime XSS Scanner

Thank you for your interest in contributing to AlertTime XSS Scanner! This document provides guidelines for contributing to the project.

## Author

**Orkhan Khalafi**  
LinkedIn: https://www.linkedin.com/in/orkhankhalafi/

## How to Contribute

### Reporting Issues

1. Check existing issues to avoid duplicates
2. Use the issue template when available
3. Provide detailed information about the bug or feature request
4. Include steps to reproduce for bugs

### Pull Requests

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Add tests if applicable
5. Ensure all tests pass
6. Update documentation if needed
7. Commit your changes (`git commit -m 'Add amazing feature'`)
8. Push to the branch (`git push origin feature/amazing-feature`)
9. Open a Pull Request

### Code Style

- Follow PEP 8 Python style guidelines
- Use meaningful variable and function names
- Keep functions focused and concise
- Use type hints where appropriate

### Testing

- Test your changes thoroughly
- Include test cases for new features
- Ensure existing tests still pass
- Test with different Python versions if possible

### Security Considerations

- This is a security testing tool - be mindful of security implications
- Never include real credentials or sensitive data in code
- Follow responsible disclosure practices
- Ensure new features don't introduce security vulnerabilities

## Development Setup

1. Clone the repository:
```bash
git clone https://github.com/orkhankhalafi/alerttime-xss-scanner.git
cd alerttime-xss-scanner
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run tests:
```bash
python alerttime.py -l targets.txt -t 3 --html-report
```

## Feature Requests

We welcome feature requests! Please:

1. Check if the feature already exists
2. Explain the use case and benefits
3. Provide examples if possible
4. Consider the security implications

## Code of Conduct

- Be respectful and professional
- Focus on constructive feedback
- Help create a welcoming environment
- Follow ethical hacking principles

## Legal Notice

- This tool is for authorized security testing only
- Contributors must ensure their code follows legal guidelines
- Do not contribute code that could be used maliciously
- Respect responsible disclosure practices

## Questions?

Feel free to reach out:
- Open an issue for technical questions
- Contact the author on LinkedIn for other inquiries

Thank you for contributing to AlertTime XSS Scanner!