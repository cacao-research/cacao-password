# 🍫 cacao-password

[![PyPI version](https://badge.fury.io/py/cacao-password.svg)](https://badge.fury.io/py/cacao-password)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)


A secure password generator with both CLI and GUI interfaces, featuring a brown-themed design and comprehensive password analysis capabilities.

## 🌟 Features

- **Password Generation**: Create cryptographically secure passwords with customizable options
  - Configurable password length
  - Character type selection (uppercase, lowercase, numbers, symbols)
  - Character filtering and exclusion options
  - Batch generation capabilities
- **Password Strength Analysis**: Real-time entropy calculation and crack time estimation
- **Dual Interfaces**: 
  - Command-line interface for automation and scripting
  - Graphical user interface with intuitive brown-themed design
- **Configuration Management**: Persistent settings stored in JSON format in user config directory
- **User-Friendly GUI Controls**:
  - Password length slider
  - Symbol toggle switches
  - One-click generate button
  - Copy-to-clipboard functionality

## 📦 Installation

### From PyPI (Recommended)

```bash
pip install cacao-password
```

## ⚡Usage

### Command Line Interface

Launch the CLI:
```bash
cacao-password
```

The CLI provides interactive prompts for password generation options and displays both the generated password and its strength analysis.

#### Command Line Options

The CLI supports various options for automated password generation:
- Interactive mode with guided prompts
- Password strength analysis with entropy metrics
- Configurable output formats

### Graphical User Interface

Launch the GUI:
```bash
cacao-password --gui
```

The GUI features:
- **Password Length Slider**: Adjust password length from 4 to 128 characters
- **Character Type Toggles**: Enable/disable uppercase, lowercase, numbers, and symbols
- **Generate Button**: Create new passwords with current settings
- **Copy Button**: Copy generated passwords to clipboard
- **Strength Meter**: Visual indicator of password strength and entropy
- **Settings Persistence**: Your preferences are automatically saved

The interface uses a warm brown color scheme designed for comfortable extended use.

## 📚 Requirements

- **Python**: >= 3.8
- **Dependencies**:
  - `cacao-password-generator`: Core password generation library

### 🐍 Supported Python Versions

- Python 3.8
- Python 3.9
- Python 3.10
- Python 3.11
- Python 3.12

## ⚙️ Security

- Uses cryptographically secure random number generation
- Implements industry-standard entropy calculations
- Provides realistic crack time estimations
- No password storage or network transmission
- All generation happens locally on your machine

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Links

- **Homepage**: https://github.com/cacao-research/cacao-password
- **Bug Reports**: https://github.com/cacao-research/cacao-password/issues
- **Source Code**: https://github.com/cacao-research/cacao-password

---

Copyright (c) 2025 Cacao Research