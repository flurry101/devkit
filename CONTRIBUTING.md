# Contributing to DevKit
Thank you for your interest in contributing to DevKit!

## Development Setup
### Clone and install

```bash
git clone https://github.com/flurry101/devkit.git
cd devkit
python -m venv venv
source venv/bin/activate
pip install -e ".[dev]"
```

## Running Tests
```bash
pytest
pytest -v  # Verbose
pytest --cov=devkit  # With coverage
```

## Submitting Changes
- Fork the repository  
- Create a feature branch (`git checkout -b feature/amazing-feature`)  
- Make your changes  
- Add tests  
- Run tests (`pytest`)  
- Commit (`devkit commit --ai -s`)  
- Push and create a Pull Request  

## Commit Convention
We use conventional commits:

- `feat`: New features  
- `fix`: Bug fixes  
- `docs`: Documentation  
- `style`: Formatting  
- `refactor`: Code restructuring  
- `test`: Tests  
- `chore`: Maintenance  

Use `devkit commit` or `devkit commit --ai` for proper formatting!

## Adding Features
- Create module in `devkit/`  
- Import in `main.py`  
- Add CLI command  
- Update `README`  
- Add tests  

## Questions?
Open an issue or discussion on GitHub!
