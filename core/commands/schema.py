"""
Command schemas for Voice Commander.
Defines the structure and patterns for supported voice commands.
"""

import re
from typing import List, Dict, Any

class CommandDefinition:
    """Represents a command definition with its pattern and description."""

    def __init__(self, name: str, pattern: str, description: str, action: str = None):
        """
        Initialize a command definition.

        Args:
            name (str): Unique name for the command
            pattern (str): Regular expression pattern to match the command
            description (str): Description of what the command does
            action (str): Action associated with this command (optional)
        """
        self.name = name
        self.pattern = pattern
        self.description = description
        self.action = action

class CommandSchema:
    """Collection of command schemas."""

    # Define all supported commands
    COMMANDS = [
        CommandDefinition(
            name="help",
            pattern=r"^(помощь|помоги)$",
            description="Показать справку по командам"
        ),
        CommandDefinition(
            name="launch_app",
            pattern=r"^запустить приложение (.+)$",
            description="Запустить указанное приложение"
        ),
        CommandDefinition(
            name="close_app",
            pattern=r"^закрыть приложение (.+)$",
            description="Закрыть указанное приложение"
        ),
        CommandDefinition(
            name="maximize_window",
            pattern=r"^(максимизировать окно|развернуть окно)$",
            description="Максимизировать активное окно"
        ),
        CommandDefinition(
            name="minimize_window",
            pattern=r"^(минимизировать окно|свернуть окно)$",
            description="Свернуть активное окно"
        ),
        CommandDefinition(
            name="restore_window",
            pattern=r"^(восстановить окно|открыть окно)$",
            description="Восстановить активное окно"
        ),
        CommandDefinition(
            name="bring_to_front",
            pattern=r"^(перевести окно в фокус|переключить окно)$",
            description="Перевести активное окно в фокус"
        ),
        CommandDefinition(
            name="read_screen_text",
            pattern=r"^(прочитать текст с экрана|считать текст)$",
            description="Прочитать текст с текущего экрана"
        ),
        CommandDefinition(
            name="click_element",
            pattern=r"^кликнуть на (.+)$",
            description="Кликнуть на элемент с указанным текстом"
        ),
        CommandDefinition(
            name="type_text",
            pattern=r"^ввести в поле (.+)$",
            description="Ввести текст в поле"
        )
    ]

    @classmethod
    def get_all_schemas(cls) -> List[CommandDefinition]:
        """
        Get all command schemas.

        Returns:
            List[CommandDefinition]: List of all command definitions
        """
        return cls.COMMANDS

    @classmethod
    def get_schema_by_name(cls, name: str) -> CommandDefinition:
        """
        Get a specific command schema by name.

        Args:
            name (str): Name of the command to find

        Returns:
            CommandDefinition: The matching command definition or None
        """
        for schema in cls.COMMANDS:
            if schema.name == name:
                return schema
        return None

    @classmethod
    def get_supported_commands(cls) -> Dict[str, str]:
        """
        Get a dictionary of supported commands with their descriptions.

        Returns:
            Dict[str, str]: Dictionary mapping command names to descriptions
        """
        return {schema.name: schema.description for schema in cls.COMMANDS}