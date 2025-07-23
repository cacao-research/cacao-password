"""Simplified GUI interface for the cacao-password generator with minimal clean design."""

import cacao
from cacao import State, Component
from typing import Dict, Any, Optional
from .core import PasswordGenerator
from .config import PasswordConfig, ConfigManager
from cacao_password_generator.core import generate
from cacao_password_generator.rating import rating, detailed_rating

import sys
from typing import Tuple

# Optional dependency, but nice to have
try:
    import pyperclip  # pip install pyperclip
except ImportError:
    pyperclip = None

# Initialize cacao app
app = cacao.App()

# Simplified password state with only essential options
password_state = State({
    'length': 12,
    'include_symbols': True,
    'password': '',
    'copied': False,
    'strength_info': {
        'rating': '',
        'score': 0,
        'entropy': 0.0,
        'crack_time_formatted': ''
    }
})

# Initialize secure password generator
secure_generator = PasswordGenerator()


def analyze_password_strength(password: str, config: PasswordConfig) -> dict:
    """
    Analyze password strength using cacao_password_generator library.
    
    Args:
        password: The password to analyze
        config: Password configuration used to determine character pool
        
    Returns:
        dict: Dictionary containing rating, score, and entropy
    """
    if not password:
        return {
            'rating': 'N/A',
            'score': 0,
            'entropy': 0.0,
            'crack_time': {},
            'crack_time_formatted': 'N/A'
        }
    
    try:
        # Get basic rating from library
        basic_rating = rating(password)
        
        # Get detailed analysis including entropy and crack time
        detailed_analysis = detailed_rating(password)
        
        # Extract values from detailed analysis
        entropy = detailed_analysis.get('entropy', 0.0)
        crack_time_formatted = detailed_analysis.get('crack_time_formatted', 'Unknown')
        
        # Create crack_time dict for backward compatibility (though it might be empty)
        crack_time_estimates = detailed_analysis.get('crack_time', {})
        
        # Calculate score (0-100 based on entropy, capped at 100)
        score = min(100, int(entropy * 1.1)) if entropy > 0 else 0
        
        return {
            'rating': basic_rating,
            'score': score,
            'entropy': entropy,
            'crack_time': crack_time_estimates,
            'crack_time_formatted': crack_time_formatted
        }
    except Exception as e:
        print(f"Error analyzing password strength: {e}")
        # Fallback to basic analysis if library fails
        return {
            'rating': 'Unknown',
            'score': 0,
            'entropy': 0.0,
            'crack_time': {},
            'crack_time_formatted': 'Unknown'
        }


def generate_secure_password() -> str:
    """Generate a secure password using cacao_password_generator library."""
    state = password_state.value
    
    try:
        # Create configuration from simplified state
        config = PasswordConfig(
            length=state['length'],
            uppercase=True,  # Always include uppercase
            lowercase=True,  # Always include lowercase
            numbers=True,    # Always include numbers
            symbols=state['include_symbols']  # Only symbols is configurable
        )
        
        # Generate secure password using cacao_password_generator library
        # The generate function may have different parameters, let's use length only
        password = generate(length=config.length)
        
        # Calculate password strength using library functions
        strength_info = analyze_password_strength(password, config)
        
        # Print crack time estimation to console
        print(f"Estimated Crack Time: {strength_info['crack_time_formatted']}")
        
        # Update state with password and strength info
        current_state = password_state.value.copy()
        current_state['password'] = password
        current_state['copied'] = False
        current_state['strength_info'] = strength_info
        password_state.set(current_state)
        
        return password
        
    except Exception as e:
        print(f"Error generating password: {e}")
        return "Error generating password"


def regenerate_password() -> None:
    """Regenerate password and update state."""
    generate_secure_password()


# Subscribe to password state changes to automatically regenerate password
@password_state.subscribe
def on_password_state_change(new_state: Dict[str, Any]) -> None:
    """Handle password state changes and regenerate password when settings change."""
    print(f"Password state changed: {new_state}")
    
    if new_state['password'] == '':
        # If password is empty (initial state), generate one
        regenerate_password()


class CacaoPasswordGenerator(Component):
    """Simplified password generator component with clean design."""
    
    def __init__(self) -> None:
        super().__init__()
        self.id = id(self)
        self.component_type = "cacao_password_generator"
        
    def render(self, ui_state: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Render the simplified password generator component."""
        password_data = self._get_password_state(ui_state)
        
        return {
            "type": "section",
            "component_type": self.component_type,
            "props": {
                "style": {
                    "display": "flex",
                    "flexDirection": "column",
                    "alignItems": "center",
                    "padding": "20px",
                    "background": "#8D6E63",  # Subtle brown background
                    "maxWidth": "500px",
                    "width": "100%",
                    "margin": "0 auto",
                    "color": "white"
                },
                "children": [
                    # Simple title
                    {
                        "type": "h2",
                        "props": {
                            "content": "Password Generator",
                            "style": {
                                "fontSize": "24px",
                                "fontWeight": "600",
                                "marginBottom": "20px",
                                "textAlign": "center",
                                "color": "white"
                            }
                        }
                    },
                    
                    # Password display
                    {
                        "type": "div",
                        "props": {
                            "style": {
                                "width": "100%",
                                "marginBottom": "15px",
                                "background": "rgba(255,255,255,0.1)",
                                "padding": "15px",
                                "textAlign": "center"
                            },
                            "children": [
                                {
                                    "type": "text",
                                    "props": {
                                        "content": password_data.get('password', 'Click Generate to create password'),
                                        "style": {
                                            "fontSize": "16px",
                                            "fontFamily": "monospace",
                                            "wordBreak": "break-all",
                                            "color": "white",
                                            "fontWeight": "500"
                                        }
                                    }
                                }
                            ]
                        }
                    },
                    
                    # Copy button
                    {
                        "type": "div",
                        "props": {
                            "style": {
                                "display": "flex",
                                "alignItems": "center",
                                "justifyContent": "center",
                                "gap": "10px",
                                "marginBottom": "20px"
                            },
                            "children": [
                                {
                                    "type": "button",
                                    "props": {
                                        "label": "Copy",
                                        "action": "copy_password",
                                        "style": {
                                            "padding": "8px 16px",
                                            "backgroundColor": "rgba(255,255,255,0.2)",
                                            "color": "white",
                                            "border": "1px solid rgba(255,255,255,0.3)",
                                            "fontSize": "14px",
                                            "cursor": "pointer"
                                        }
                                    }
                                },
                                {
                                    "type": "text",
                                    "props": {
                                        "content": "Copied!" if password_data.get('copied', False) else "",
                                        "style": {
                                            "fontSize": "12px",
                                            "color": "#4CAF50",
                                            "fontWeight": "500"
                                        }
                                    }
                                }
                            ]
                        }
                    },
                    
                    # Length control
                    {
                        "type": "div",
                        "props": {
                            "style": {
                                "width": "100%",
                                "marginBottom": "15px"
                            },
                            "children": [
                                {
                                    "type": "div",
                                    "props": {
                                        "style": {
                                            "display": "flex",
                                            "alignItems": "center",
                                            "justifyContent": "space-between",
                                            "marginBottom": "8px"
                                        },
                                        "children": [
                                            {
                                                "type": "text",
                                                "props": {
                                                    "content": "Length",
                                                    "style": {
                                                        "fontSize": "14px",
                                                        "color": "white"
                                                    }
                                                }
                                            },
                                            {
                                                "type": "text",
                                                "props": {
                                                    "content": str(password_data.get('length', 12)),
                                                    "style": {
                                                        "fontSize": "14px",
                                                        "fontWeight": "600",
                                                        "color": "white",
                                                        "background": "rgba(255,255,255,0.2)",
                                                        "padding": "2px 8px"
                                                    }
                                                }
                                            }
                                        ]
                                    }
                                },
                                {
                                    "type": "slider",
                                    "props": {
                                        "min": 4,
                                        "max": 50,
                                        "step": 1,
                                        "value": password_data.get('length', 12),
                                        "onChange": {
                                            "action": "update_length"
                                        }
                                    }
                                }
                            ]
                        }
                    },
                    
                    # Simple symbols toggle
                    {
                        "type": "label",
                        "props": {
                            "style": {
                                "display": "flex",
                                "alignItems": "center",
                                "gap": "8px",
                                "cursor": "pointer",
                                "marginBottom": "20px"
                            },
                            "children": [
                                {
                                    "type": "checkbox",
                                    "props": {
                                        "checked": password_data.get('include_symbols', True),
                                        "action": "toggle_symbols",
                                        "style": {
                                            "width": "16px",
                                            "height": "16px",
                                            "cursor": "pointer"
                                        }
                                    }
                                },
                                {
                                    "type": "text",
                                    "props": {
                                        "content": "Include symbols",
                                        "style": {
                                            "fontSize": "14px",
                                            "color": "white"
                                        }
                                    }
                                }
                            ]
                        }
                    },
                    
                    # Generate button
                    {
                        "type": "button",
                        "props": {
                            "label": "Generate New Password",
                            "action": "generate_password",
                            "style": {
                                "padding": "12px 24px",
                                "backgroundColor": "#5D4037",
                                "color": "white",
                                "border": "none",
                                "fontSize": "14px",
                                "fontWeight": "600",
                                "cursor": "pointer",
                                "marginBottom": "15px"
                            }
                        }
                    },
                    
                    # Simple strength display
                    {
                        "type": "div",
                        "props": {
                            "style": {
                                "fontSize": "12px",
                                "color": "rgba(255,255,255,0.8)",
                                "textAlign": "center"
                            },
                            "children": [
                                {
                                    "type": "text",
                                    "props": {
                                        "content": f"Strength: {password_data.get('strength_info', {}).get('rating', 'Unknown')}"
                                    }
                                }
                            ]
                        }
                    },
                    
                    # Crack time display
                    {
                        "type": "div",
                        "props": {
                            "style": {
                                "fontSize": "11px",
                                "color": "rgba(255,255,255,0.7)",
                                "textAlign": "center",
                                "marginTop": "5px"
                            },
                            "children": [
                                {
                                    "type": "text",
                                    "props": {
                                        "content": f"Crack Time: {password_data.get('strength_info', {}).get('crack_time_formatted', 'Unknown')}"
                                    }
                                }
                            ]
                        }
                    }
                ]
            }
        }
    
    def _get_password_state(self, ui_state: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Get the current password state."""
        if ui_state and isinstance(ui_state, dict) and 'password_data' in ui_state:
            return ui_state['password_data']
        return password_state.value


# Simplified event handlers

@app.event("generate_password")
def handle_generate_password(event_data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Handle password generation button click."""
    print(f"Generate password event received with data: {event_data}")
    
    regenerate_password()
    
    print(f"New password generated: {password_state.value['password']}")
    
    return {
        "password_data": password_state.value
    }


@app.event("update_length")
def handle_update_length(event_data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Handle password length slider change."""
    print(f"Update length event received with data: {event_data}")
    
    new_length = 12  # Default fallback
    if event_data is not None:
        try:
            if isinstance(event_data, (int, float)):
                new_length = int(event_data)
            elif isinstance(event_data, dict) and 'value' in event_data:
                new_length = int(event_data['value'])
            
            new_length = max(4, min(50, new_length))
        except (ValueError, TypeError) as e:
            print(f"Invalid length value: {event_data}, using default: {new_length}. Error: {e}")
    
    current_state = password_state.value.copy()
    current_state['length'] = new_length
    current_state['copied'] = False
    password_state.set(current_state)
    
    regenerate_password()
    
    print(f"Length updated to: {new_length}")
    
    return {
        "password_data": password_state.value
    }


@app.event("toggle_symbols")
def handle_toggle_symbols(event_data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Handle symbols checkbox toggle."""
    print(f"Toggle symbols event received with data: {event_data}")
    
    checked = True  # Default to true
    if event_data and 'checked' in event_data:
        checked = bool(event_data['checked'])
    
    current_state = password_state.value.copy()
    current_state['include_symbols'] = checked
    current_state['copied'] = False
    password_state.set(current_state)
    
    regenerate_password()
    
    print(f"Symbols toggled to: {checked}")
    
    return {
        "password_data": password_state.value
    }


def copy_text(text: str) -> Tuple[bool, str]:
    """
    Copy `text` to the system clipboard.
    Returns (success, backend_used).
    """
    # 1) pyperclip if available
    if pyperclip:
        pyperclip.copy(text)
        return True, "pyperclip"

    # 2) Fallbacks per OS
    if sys.platform.startswith("win"):
        import subprocess
        subprocess.run("clip", text=True, input=text, check=False)
        return True, "clip"
    elif sys.platform == "darwin":
        import subprocess
        p = subprocess.Popen(["pbcopy"], stdin=subprocess.PIPE)
        p.communicate(input=text.encode("utf-8"))
        return True, "pbcopy"
    else:  # Linux/*nix
        import subprocess
        for cmd in ("xclip -selection clipboard", "xsel --clipboard"):
            try:
                p = subprocess.Popen(cmd.split(), stdin=subprocess.PIPE)
                p.communicate(input=text.encode("utf-8"))
                return True, cmd.split()[0]
            except FileNotFoundError:
                continue
        return False, "no-backend"


@app.event("copy_password")
def handle_copy_password(event_data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Handle copy password button click."""
    print(f"Copy password event received with data: {event_data}")

    current_state = password_state.value.copy()

    success, backend = copy_text(current_state["password"])
    current_state["copied"] = success
    password_state.set(current_state)

    print(f"Password copied ({backend}): {current_state['password']}")

    return {"password_data": password_state.value, "copied": success}


@app.mix("/")
def home() -> Dict[str, Any]:
    """Main page with simplified password generator."""
    # Initialize password if empty
    if not password_state.value['password']:
        regenerate_password()
    
    password_component = CacaoPasswordGenerator()
    
    return {
        "type": "div",
        "props": {
            "style": {
                "minHeight": "100vh",
                "background": "#8D6E63",  # Same brown background as component
                "display": "flex",
                "flexDirection": "column",
                "alignItems": "center",
                "padding": "40px 20px",
                "fontFamily": "system-ui, -apple-system, sans-serif"
            }
        },
        "children": [
            password_component.render()
        ]
    }


def launch_gui_app() -> None:
    """Launch the GUI application."""
    try:
        print("Starting Cacao Password Generator GUI...")
        app.brew(
            type="desktop",
            width=500,
            height=502,
        )
    except Exception as e:
        raise RuntimeError(f"Failed to launch GUI: {e}")


if __name__ == "__main__":
    launch_gui_app()