"""
Command schema definitions for voice commander.
"""

class CommandSchema:
    """Define command schemas and validation rules."""

    def __init__(self):
        """Initialize the command schema."""
        self.commands = [
            {
                'type': 'launch',
                'required_words': ['запусти', 'открой'],
                'params': {
                    'app_name': {'type': 'string', 'required': True}
                },
                'description': 'Launch an application'
            },
            {
                'type': 'close',
                'required_words': ['закрой', 'закройте'],
                'params': {
                    'app_name': {'type': 'string', 'required': False}
                },
                'description': 'Close an application'
            },
            {
                'type': 'minimize',
                'required_words': ['сверни', 'свернуть'],
                'params': {
                    'window_title': {'type': 'string', 'required': False}
                },
                'description': 'Minimize a window'
            },
            {
                'type': 'maximize',
                'required_words': ['разверни', 'развернуть'],
                'params': {
                    'window_title': {'type': 'string', 'required': False}
                },
                'description': 'Maximize a window'
            },
            {
                'type': 'bring_to_front',
                'required_words': ['впереди', 'прибери'],
                'params': {
                    'window_title': {'type': 'string', 'required': False}
                },
                'description': 'Bring window to front'
            },
            {
                'type': 'click',
                'required_words': ['кликни', 'нажми'],
                'params': {
                    'element_text': {'type': 'string', 'required': True}
                },
                'description': 'Click on UI element by text'
            },
            {
                'type': 'type_text',
                'required_words': ['введи', 'напиши'],
                'params': {
                    'element_text': {'type': 'string', 'required': True},
                    'text_to_type': {'type': 'string', 'required': True}
                },
                'description': 'Type text into a field'
            },
            {
                'type': 'read_screen',
                'required_words': ['прочти', 'считай'],
                'params': {
                    'region': {'type': 'string', 'required': False}
                },
                'description': 'Read text from screen region'
            },
            {
                'type': 'help',
                'required_words': ['помощь', 'справка'],
                'params': {},
                'description': 'Show help information'
            }
        ]