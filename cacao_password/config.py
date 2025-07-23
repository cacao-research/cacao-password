"""Configuration management for password generation settings."""

import json
import os
from typing import Dict, Any, Optional
from dataclasses import dataclass, asdict

@dataclass
class PasswordConfig:
    """Configuration class for password generation settings."""
    
    # Core settings
    length: int = 12
    uppercase: bool = True
    lowercase: bool = True
    numbers: bool = True
    symbols: bool = True
    all_characters: bool = False
    
    # Filtering options
    easy_to_say: bool = False
    easy_to_read: bool = False
    
    # Additional options
    exclude_similar: bool = False
    exclude_ambiguous: bool = False
    
    def __post_init__(self) -> None:
        """Validate configuration after initialization."""
        self.validate()
    
    def validate(self) -> None:
        """
        Validate configuration settings.
        
        Raises:
            ValueError: If any setting is invalid
        """
        # Validate length
        if not isinstance(self.length, int) or self.length < 4 or self.length > 128:
            raise ValueError(
                f"Password length must be between 4 and 128, got {self.length}"
            )
        
        # Validate boolean settings
        bool_settings = [
            'uppercase', 'lowercase', 'numbers', 'symbols', 'all_characters',
            'easy_to_say', 'easy_to_read', 'exclude_similar', 'exclude_ambiguous'
        ]
        
        for setting in bool_settings:
            value = getattr(self, setting)
            if not isinstance(value, bool):
                raise ValueError(
                    f"Setting '{setting}' must be a boolean, got {type(value).__name__}"
                )
        
        # Ensure at least one character type is selected when not using all_characters
        if not self.all_characters:
            if not any([self.uppercase, self.lowercase, self.numbers, self.symbols]):
                raise ValueError(
                    "At least one character type must be enabled when 'all_characters' is False"
                )
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert configuration to dictionary.
        
        Returns:
            Dict[str, Any]: Configuration as dictionary
        """
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'PasswordConfig':
        """
        Create configuration from dictionary.
        
        Args:
            data: Dictionary containing configuration data
            
        Returns:
            PasswordConfig: New configuration instance
            
        Raises:
            RuntimeError: If data is invalid
        """
        try:
            # Filter out unknown keys
            valid_keys = {
                'length', 'uppercase', 'lowercase', 'numbers', 'symbols',
                'all_characters', 'easy_to_say', 'easy_to_read',
                'exclude_similar', 'exclude_ambiguous'
            }
            
            filtered_data = {k: v for k, v in data.items() if k in valid_keys}
            return cls(**filtered_data)
            
        except TypeError as e:
            raise RuntimeError(f"Invalid configuration data: {str(e)}")
        except ValueError:
            # Re-raise validation errors as-is
            raise
        except Exception as e:
            raise RuntimeError(f"Failed to create configuration: {str(e)}")
    
    def to_json(self, indent: int = 2) -> str:
        """
        Convert configuration to JSON string.
        
        Args:
            indent: JSON indentation level
            
        Returns:
            str: Configuration as JSON string
        """
        try:
            return json.dumps(self.to_dict(), indent=indent)
        except Exception as e:
            raise RuntimeError(f"Failed to serialize configuration to JSON: {str(e)}")
    
    @classmethod
    def from_json(cls, json_str: str) -> 'PasswordConfig':
        """
        Create configuration from JSON string.
        
        Args:
            json_str: JSON string containing configuration
            
        Returns:
            PasswordConfig: New configuration instance
            
        Raises:
            RuntimeError: If JSON is invalid
        """
        try:
            data = json.loads(json_str)
            return cls.from_dict(data)
        except json.JSONDecodeError as e:
            raise RuntimeError(f"Invalid JSON: {str(e)}")
        except Exception as e:
            raise RuntimeError(f"Failed to load configuration from JSON: {str(e)}")
    
    def save_to_file(self, filepath: str) -> None:
        """
        Save configuration to file.
        
        Args:
            filepath: Path to save configuration file
            
        Raises:
            RuntimeError: If file cannot be saved
        """
        try:
            with open(filepath, 'w') as f:
                f.write(self.to_json())
        except Exception as e:
            raise RuntimeError(f"Failed to save configuration to {filepath}: {str(e)}")
    
    @classmethod
    def load_from_file(cls, filepath: str) -> 'PasswordConfig':
        """
        Load configuration from file.
        
        Args:
            filepath: Path to configuration file
            
        Returns:
            PasswordConfig: Loaded configuration
            
        Raises:
            RuntimeError: If file cannot be loaded
        """
        try:
            with open(filepath, 'r') as f:
                json_str = f.read()
            return cls.from_json(json_str)
        except FileNotFoundError:
            raise RuntimeError(f"Configuration file not found: {filepath}")
        except Exception as e:
            raise RuntimeError(f"Failed to load configuration from {filepath}: {str(e)}")
    
    def copy(self, **changes) -> 'PasswordConfig':
        """
        Create a copy of the configuration with optional changes.
        
        Args:
            **changes: Configuration changes to apply
            
        Returns:
            PasswordConfig: New configuration with changes applied
        """
        data = self.to_dict()
        data.update(changes)
        return self.from_dict(data)


class ConfigManager:
    """Manages configuration loading, saving, and defaults."""
    
    DEFAULT_CONFIG_NAME = "cacao_password_config.json"
    
    def __init__(self, config_dir: Optional[str] = None) -> None:
        """
        Initialize configuration manager.
        
        Args:
            config_dir: Directory to store configuration files (default: user home)
        """
        if config_dir is None:
            config_dir = os.path.expanduser("~/.config/cacao-password")
        
        self.config_dir = config_dir
        self.config_file = os.path.join(config_dir, self.DEFAULT_CONFIG_NAME)
        
        # Ensure config directory exists
        os.makedirs(config_dir, exist_ok=True)
    
    def load_default_config(self) -> PasswordConfig:
        """
        Load default configuration.
        
        Returns:
            PasswordConfig: Default configuration
        """
        return PasswordConfig()
    
    def load_user_config(self) -> PasswordConfig:
        """
        Load user configuration from file, falling back to defaults.
        
        Returns:
            PasswordConfig: User configuration or defaults
        """
        if os.path.exists(self.config_file):
            try:
                return PasswordConfig.load_from_file(self.config_file)
            except RuntimeError:
                # Fall back to defaults if user config is corrupted
                return self.load_default_config()
        else:
            return self.load_default_config()
    
    def save_user_config(self, config: PasswordConfig) -> None:
        """
        Save user configuration to file.
        
        Args:
            config: Configuration to save
            
        Raises:
            RuntimeError: If configuration cannot be saved
        """
        try:
            config.save_to_file(self.config_file)
        except Exception as e:
            raise RuntimeError(f"Failed to save user configuration: {str(e)}")
    
    def reset_to_defaults(self) -> PasswordConfig:
        """
        Reset configuration to defaults and save.
        
        Returns:
            PasswordConfig: Default configuration
        """
        default_config = self.load_default_config()
        self.save_user_config(default_config)
        return default_config


# Global configuration manager instance
default_config_manager = ConfigManager()