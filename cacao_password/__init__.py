"""
Cacao Password Generator - A secure password generator with GUI and CLI interfaces.

This package provides cryptographically secure password generation using Python's
secrets module, with both command-line and graphical user interfaces featuring
a brown/chocolate theme.
"""

__version__ = "1.0.1"
__author__ = "Juan Denis"
__email__ = "juan@vene.co"
__description__ = "A secure password generator with brown-themed GUI and CLI interfaces"

# Import core functionality
from .core import (
    PasswordGenerator,
    generate_password,
    default_generator
)

# Import configuration classes
from .config import (
    PasswordConfig,
    ConfigManager,
    default_config_manager
)

# Define what gets imported with "from cacao_password import *"
__all__ = [
    # Version info
    '__version__',
    '__author__',
    '__email__',
    '__description__',

    # Core classes and functions
    'PasswordGenerator',
    'generate_password',
    'default_generator',

    # Configuration
    'PasswordConfig',
    'ConfigManager',
    'default_config_manager'
]


def get_version() -> str:
    """
    Get the package version.
    
    Returns:
        str: Package version string
    """
    return __version__


def quick_generate(length: int = 12, **kwargs) -> str:
    """
    Quick password generation function with sensible defaults.
    
    Args:
        length: Password length (default: 12)
        **kwargs: Additional password generation options
        
    Returns:
        str: Generated password
        
    Example:
        >>> import cacao_password
        >>> password = cacao_password.quick_generate(16, symbols=True)
        >>> print(f"Generated password: {password}")
    """
    return generate_password(length=length, **kwargs)


# Removed quick_analyze since analyze_password_strength is no longer available


def create_config(**kwargs) -> PasswordConfig:
    """
    Create a password configuration with custom settings.

    Args:
        **kwargs: Configuration options

    Returns:
        PasswordConfig: Configuration object

    Example:
        >>> import cacao_password
        >>> config = cacao_password.create_config(length=16, symbols=True, easy_to_read=True)
        >>> password = cacao_password.generate_password(config=config)
    """
    return PasswordConfig(**kwargs)


# Package metadata for introspection
def get_package_info() -> dict:
    """
    Get comprehensive package information.
    
    Returns:
        dict: Package metadata
    """
    return {
        'name': 'cacao-password',
        'version': __version__,
        'author': __author__,
        'email': __email__,
        'description': __description__,
        'python_requires': '>=3.8',
        'dependencies': [],
        'optional_dependencies': {
            'dev': ['pytest', 'black', 'flake8', 'mypy']
        },
        'entry_points': {
            'console_scripts': ['cacao-password = cacao_password.cli:main']
        }
    }