"""
Command parser for Voice Commander.
Parses natural language commands into executable actions.
"""

import re
from typing import Optional
from core.commands.schema import CommandDefinition, CommandSchema
from core.feedback import speak_and_log
from core.logger import get_logger

logger = get_logger(__name__)

class CommandParser:
    """Parse natural language commands into executable actions."""

    def __init__(self):
        """Initialize the command parser."""
        self.command_schemas = CommandSchema.get_all_schemas()
        logger.info(f"Initialized command parser with {len(self.command_schemas)} command schemas")

    def parse_command(self, text: str) -> Optional['Command']:
        """
        Parse a natural language command into a Command object.

        Args:
            text (str): The command text to parse

        Returns:
            Optional[Command]: Parsed command object or None if unrecognized
        """
        if not text or not isinstance(text, str):
            return None

        text = text.strip().lower()

        # Try to match each command schema
        for schema in self.command_schemas:
            pattern = schema.pattern
            if re.match(pattern, text):
                logger.info(f"Matched command pattern: {pattern}")
                return Command(schema, text)

        logger.warning(f"No matching command pattern found for: {text}")
        return None

class Command:
    """Represents a parsed command with its arguments."""

    def __init__(self, schema: CommandDefinition, raw_text: str):
        """
        Initialize a command.

        Args:
            schema (CommandDefinition): The command schema
            raw_text (str): The original command text
        """
        self.schema = schema
        self.raw_text = raw_text
        self.arguments = {}

    def execute(self) -> str:
        """
        Execute the command and return result.

        Returns:
            str: Execution result message
        """
        try:
            # For now, we'll just return a placeholder result
            # In a real implementation, this would call the appropriate action
            logger.info(f"Executing command: {self.schema.name}")

            if self.schema.name == "help":
                return "Помощь показана"
            elif self.schema.name == "launch_app":
                app_name = self._extract_app_name()
                from core.actions.launch import launch_application
                return launch_application(app_name)
            elif self.schema.name == "close_app":
                app_name = self._extract_app_name()
                from core.actions.close import close_application
                return close_application(app_name)
            elif self.schema.name == "maximize_window":
                from core.actions.window import maximize_window
                return maximize_window()
            elif self.schema.name == "minimize_window":
                from core.actions.window import minimize_window
                return minimize_window()
            elif self.schema.name == "restore_window":
                from core.actions.window import restore_window
                return restore_window()
            elif self.schema.name == "bring_to_front":
                from core.actions.window import bring_to_front
                return bring_to_front()
            elif self.schema.name == "read_screen_text":
                from core.actions.screen_ocr import read_screen_text
                return read_screen_text()
            elif self.schema.name == "click_element":
                # For click_element, we would need to extract the element text
                # This is a simplified version - in practice this would be more sophisticated
                element_text = self.raw_text.replace("кликнуть на", "").strip()
                from core.actions.ui_click import click_element
                return click_element(element_text)
            elif self.schema.name == "type_text":
                # For type_text, we would need to extract the text to type
                # This is a simplified version - in practice this would be more sophisticated
                element_text = self.raw_text.replace("ввести в поле", "").strip()
                from core.actions.ui_type import type_text
                return type_text(element_text)
            else:
                return f"Выполнена команда: {self.schema.name}"

        except Exception as e:
            logger.error(f"Error executing command '{self.schema.name}': {e}")
            return "Ошибка выполнения команды"

    def _extract_app_name(self) -> str:
        """
        Extract application name from the command text.

        Returns:
            str: Extracted application name
        """
        # This is a simplified version - in practice this would be more sophisticated
        app_name = self.raw_text.replace("запустить приложение", "").strip()
        app_name = app_name.replace("закрыть приложение", "").strip()
        return app_name if app_name else "не указано"