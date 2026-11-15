"""
Command parser for voice commander.
"""

from .schema import CommandSchema

class CommandParser:
    """Parse spoken commands into Command objects."""

    def __init__(self):
        """Initialize the command parser."""
        self.schema = CommandSchema()

    def parse_command(self, text):
        """
        Parse a command from text.

        Args:
            text (str): Text to parse

        Returns:
            dict: Parsed command with type and parameters
        """
        # Normalize input
        text = text.strip().lower()

        # Check for known commands
        for command_def in self.schema.commands:
            if self._matches_command(text, command_def):
                return {
                    'type': command_def['type'],
                    'params': self._extract_params(text, command_def)
                }

        # If no command matched, return unknown command
        return {
            'type': 'unknown',
            'params': {'text': text}
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

        # Extract parameters based on the command definition
        for param_name, param_info in command_def.get('params', {}).items():
            # For now, we'll just return the text as a placeholder
            # In a more advanced implementation, this would extract specific values
            params[param_name] = text

        return params