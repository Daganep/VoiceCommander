"""
Command parser for voice commander.
"""

from .schema import CommandSchema
from .executor import CommandExecutor

class CommandParser:
    """Parse spoken commands into Command objects."""

    def __init__(self):
        """Initialize the command parser."""
        self.schema = CommandSchema()
        self.executor = CommandExecutor()

    def parse_command(self, text, feedback=None):
        """
        Parse a command from text and execute it.

        Args:
            text (str): Text to parse
            feedback (Feedback): Feedback system for user interaction

        Returns:
            dict: Result of command execution
        """
        # Normalize input
        text = text.strip().lower()

        # Check for known commands
        for command_def in self.schema.commands:
            if self._matches_command(text, command_def):
                params = self._extract_params(text, command_def)
                # Execute the command and return result
                return self.executor.execute_command(command_def['type'], params, feedback)

        # If no command matched, return error
        return {
            'success': False,
            'message': f'Unknown command: {text}'
        }

    def _matches_command(self, text, command_def):
        """
        Check if text matches a command definition.

        Args:
            text (str): Text to check
            command_def (dict): Command definition

        Returns:
            bool: True if text matches the command
        """
        # Simple matching - check if all required words are in the text
        required_words = command_def.get('required_words', [])
        for word in required_words:
            if word.lower() not in text:
                return False
        return True

    def _extract_params(self, text, command_def):
        """
        Extract parameters from text based on command definition.

        Args:
            text (str): Text to extract parameters from
            command_def (dict): Command definition

        Returns:
            dict: Extracted parameters
        """
        params = {}

        # Extract meaningful parameters based on the command type
        if command_def['type'] in ['launch', 'close']:
            # For launch/close commands, extract the application name after the verb
            # This is a simple implementation - a more robust version would use NLP
            app_name = text.replace('запусти ', '').replace('открой ', '').replace('закрой ', '').replace('закройте ', '')
            app_name = app_name.strip()
            params['app_name'] = app_name if app_name else None

        elif command_def['type'] in ['minimize', 'maximize', 'bring_to_front']:
            # For window commands, extract the window title if specified
            # This is a placeholder - more sophisticated parsing would be needed
            params['window_title'] = None

        elif command_def['type'] == 'click':
            # For UI interaction commands, extract element text
            # Remove the command prefix and any additional words to get the element text
            if 'кликни' in text:
                element_text = text.replace('кликни ', '')
            elif 'нажми' in text:
                element_text = text.replace('нажми ', '')
            else:
                element_text = text

            params['element_text'] = element_text.strip()

        elif command_def['type'] == 'type_text':
            # For type text commands, we need to parse the element text and the text to type
            # Extract "ввести в [поле] текст [текст]" pattern
            if 'ввести' in text and 'текст' in text:
                # Split by "ввести" and "текст"
                parts = text.split('ввести')
                if len(parts) > 1:
                    element_part = parts[1].split('текст')
                    if len(element_part) > 1:
                        params['element_text'] = element_part[0].strip()
                        params['text_to_type'] = element_part[1].strip()
                    else:
                        # Fallback - just get the text after "ввести"
                        params['element_text'] = parts[1].strip()
                        params['text_to_type'] = ''
                else:
                    params['element_text'] = ''
                    params['text_to_type'] = ''
            elif 'напиши' in text and 'текст' in text:
                # Alternative pattern: "напиши текст [текст] в [поле]"
                parts = text.split('напиши текст')
                if len(parts) > 1:
                    text_part = parts[1].split('в ')
                    if len(text_part) > 1:
                        params['text_to_type'] = text_part[0].strip()
                        params['element_text'] = text_part[1].strip()
                    else:
                        # Fallback
                        params['element_text'] = ''
                        params['text_to_type'] = ''
                else:
                    params['element_text'] = ''
                    params['text_to_type'] = ''
            else:
                # If we can't parse it properly, use the whole text
                params['element_text'] = text
                params['text_to_type'] = ''

        elif command_def['type'] == 'read_screen':
            # For screen reading, we might extract region information
            params['region'] = None

        else:
            # Default: pass the full text
            params['text'] = text

        return params