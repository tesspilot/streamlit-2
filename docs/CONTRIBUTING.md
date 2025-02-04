# Contributing Guidelines

## Development Setup

1. Clone the repository
2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Project Structure

```
gemeente-mvp/
├── src/                    # Source code
│   ├── vervangingsinvestering.py  # Main Streamlit app
│   └── data_loader.py     # Data loading utilities
├── data/                  # Data files
│   ├── csv/              # CSV data files
│   └── excel/            # Excel data files
├── docs/                  # Documentation
├── tests/                # Test files
└── requirements.txt      # Project dependencies
```

## Development Workflow

1. Create a new branch for your feature
2. Make your changes
3. Run tests
4. Submit a pull request

## Code Style

- Follow PEP 8 guidelines
- Use meaningful variable names
- Add docstrings to functions and classes
- Keep functions small and focused

## Testing

- Add tests for new features
- Run existing tests before submitting changes
- Use pytest for testing
