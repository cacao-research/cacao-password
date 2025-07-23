"""Core password generation module using cryptographically secure random generators."""

from cacao_password_generator.core import generate
from typing import Dict, Any, Optional
from .config import PasswordConfig
# PasswordGenerationError import removed (module deleted)


class PasswordGenerator:
    """Secure password generator using cacao-password-generator."""

    def generate(
        self,
        config: Optional[PasswordConfig] = None,
        length: int = 12,
        uppercase: bool = True,
        lowercase: bool = True,
        numbers: bool = True,
        symbols: bool = True,
        all_characters: bool = False,
        easy_to_say: bool = False,
        easy_to_read: bool = False
    ) -> str:
        """
        Generate a secure password using cacao-password-generator.
        """
        if config:
            length = config.length
            uppercase = config.uppercase
            lowercase = config.lowercase
            numbers = config.numbers
            symbols = config.symbols
            all_characters = config.all_characters
            easy_to_say = config.easy_to_say
            easy_to_read = config.easy_to_read

        # Convert boolean flags to minimum character counts for cacao-password-generator API
        params = {
            'minuchars': 1 if uppercase else 0,  # minimum uppercase characters
            'minlchars': 1 if lowercase else 0,  # minimum lowercase characters
            'minnumbers': 1 if numbers else 0,   # minimum numbers
            'minschars': 1 if symbols else 0     # minimum special characters
        }
        
        return generate(params, length=length)

    def generate_multiple(self, count: int = 1, **kwargs) -> list[str]:
        """
        Generate multiple passwords with the same configuration.
        
        Args:
            count: Number of passwords to generate
            **kwargs: Password generation parameters
            
        Returns:
            list[str]: List of generated passwords
        """
        if not isinstance(count, int) or count < 1 or count > 100:
            raise ValueError(
                f"Count must be between 1 and 100, got {count}"
            )

        return [self.generate(**kwargs) for _ in range(count)]

    def generate_from_dict(self, settings: Dict[str, Any]) -> str:
        """
        Generate a password from a dictionary of settings.
        
        Args:
            settings: Dictionary containing password generation settings
            
        Returns:
            str: Generated password
        """
        try:
            config = PasswordConfig.from_dict(settings)
            return self.generate(config)
        except Exception as e:
            raise RuntimeError(f"Invalid settings provided: {str(e)}")


# Convenience function for simple password generation
def generate_password(
    length: int = 12,
    uppercase: bool = True,
    lowercase: bool = True,
    numbers: bool = True,
    symbols: bool = True
) -> str:
    """
    Simple function to generate a password with basic options.

    Args:
        length: Password length
        uppercase: Include uppercase letters
        lowercase: Include lowercase letters
        numbers: Include numbers
        symbols: Include symbols

    Returns:
        str: Generated password
    """
    # Convert boolean flags to minimum character counts for cacao-password-generator API
    params = {
        'minuchars': 1 if uppercase else 0,  # minimum uppercase characters
        'minlchars': 1 if lowercase else 0,  # minimum lowercase characters
        'minnumbers': 1 if numbers else 0,   # minimum numbers
        'minschars': 1 if symbols else 0     # minimum special characters
    }
    
    return generate(params, length=length)


# Default password generator instance
default_generator = PasswordGenerator()