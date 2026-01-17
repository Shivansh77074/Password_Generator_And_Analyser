
# ============================================================================
# File: README.md
# ============================================================================
"""
# Secure Password Utility

A professional, enterprise-grade password generator and analyzer built with Python.

## 🔐 Security Features

### Zero Data Persistence
- **No logging** of passwords or user actions
- **No caching** or history tracking
- **No file storage** of sensitive data
- All operations performed **in-memory only**
- Passwords exist only during active operations

### Cryptographic Security
- Uses Python's `secrets` module (CSPRNG)
- Each password generation is completely independent
- Secure shuffling with Fisher-Yates algorithm
- Guaranteed character diversity
- No predictable patterns

## 📋 Features

### Password Generator
- **Customizable length**: 4-128 characters
- **Full character control**: Uppercase, lowercase, numbers, symbols
- **Real-time entropy calculation**: Shannon entropy in bits
- **Unlimited generation**: No restrictions or correlations
- **One-click copy**: Clipboard integration

### Password Analyzer
- **Comprehensive strength scoring**: 0-100 scale
- **Entropy calculation**: Measure randomness in bits
- **Pattern detection**: Common passwords, sequential chars, keyboard patterns
- **Character diversity analysis**: Type distribution
- **Crack time estimation**: Brute-force resistance
- **Policy validation**: Configurable security rules
- **Recommendations**: Actionable improvement suggestions

### Additional Features
- **Modular architecture**: Clean separation of concerns
- **Extensible design**: Easy to add new features
- **Cross-platform**: Works on Windows, macOS, Linux
- **No dependencies**: Uses only Python standard library

## 🚀 Installation

### Requirements
- Python 3.8 or higher
- No external dependencies required

### Quick Start
```bash
# Clone the repository
git clone https://github.com/yourusername/password-utility.git
cd password-utility

# Run the application
python main.py
```

### Installation via setup.py
```bash
python setup.py install
password-utility
```

## 📁 Project Structure

```
password_utility/
├── main.py                     # Entry point
├── setup.py                    # Installation config
├── requirements.txt            # Dependencies (none for core)
├── README.md                   # Documentation
├── config/                     # Configuration
│   ├── __init__.py
│   └── settings.py            # App-wide settings
├── src/                       # Source code
│   ├── __init__.py
│   ├── core/                  # Core security modules
│   │   ├── __init__.py
│   │   ├── security.py        # CSPRNG functions
│   │   ├── constants.py       # Security constants
│   │   └── exceptions.py      # Custom exceptions
│   ├── generator/             # Password generation
│   │   ├── __init__.py
│   │   ├── password_generator.py
│   │   ├── entropy_calculator.py
│   │   └── charset_builder.py
│   ├── analyzer/              # Password analysis
│   │   ├── __init__.py
│   │   ├── password_analyzer.py
│   │   ├── strength_scorer.py
│   │   ├── pattern_detector.py
│   │   └── crack_time_estimator.py
│   ├── validator/             # Policy validation
│   │   ├── __init__.py
│   │   ├── policy_validator.py
│   │   └── policy_rules.py
│   └── ui/                    # User interface
│       ├── __init__.py
│       ├── main_window.py
│       ├── generator_panel.py
│       ├── analyzer_panel.py
│       └── styles.py
└── tests/                     # Unit tests
    ├── __init__.py
    ├── test_generator.py
    ├── test_analyzer.py
    └── test_validator.py
```

## 🎯 Usage Examples

### Generating Passwords
1. Launch the application
2. Adjust password length using slider (4-64 chars)
3. Select character sets (uppercase, lowercase, numbers, symbols)
4. Click "Generate Password"
5. Click "Copy" to copy to clipboard

### Analyzing Passwords
1. Navigate to "Password Analyzer" section
2. Enter password to analyze
3. Optional: Toggle "Show password" checkbox
4. Click "Analyze Password"
5. Review comprehensive strength report

## 🔒 Security Guarantees

### Data Protection
- **Memory-only operations**: Passwords never written to disk
- **No logging**: Zero logging of sensitive data
- **Stateless design**: No session or history tracking
- **Secure clipboard**: Only external destination for passwords

### Cryptographic Strength
- **CSPRNG**: Uses `secrets.choice()` and `secrets.randbelow()`
- **Uniform distribution**: Statistically unbiased selection
- **No patterns**: Fisher-Yates shuffle eliminates predictability
- **Independence**: Each generation completely independent

## 📊 Password Strength Scoring

### Scoring Algorithm (0-100 points)
- **Length (30 pts)**: Longer passwords score higher
- **Diversity (25 pts)**: Using all character types
- **Entropy (30 pts)**: Measured randomness
- **No common patterns (10 pts)**: Avoid dictionary words
- **No sequential chars (5 pts)**: Prevent abc, 123 patterns

### Strength Levels
- **0-39**: Weak
- **40-59**: Medium
- **60-79**: Strong
- **80-100**: Very Strong

## 🛡️ Policy Validation

Default policy requirements:
- Minimum 8 characters
- At least one uppercase letter
- At least one lowercase letter
- At least one number
- No common weak patterns

Customize policies in `src/validator/policy_rules.py`

## 🧪 Testing

```bash
# Install test dependencies
pip install pytest pytest-cov

# Run all tests
pytest

# Run with coverage
pytest --cov=src tests/

# Run specific test module
pytest tests/test_generator.py
```

## 🤝 Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Add tests for new features
4. Ensure all tests pass
5. Submit a pull request

## 📝 License

MIT License - see LICENSE file for details

## ⚠️ Security Notice

This tool is designed for legitimate password security purposes only.
Always follow your organization's security