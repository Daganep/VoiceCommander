"""
Command executor for voice commander.
This module maps command types to their corresponding action implementations.
"""

from ..actions.launch import Launcher
from ..actions.close import Closer
from ..actions.window import WindowManager
from ..actions.ui_type import UITyper
from ..actions.ui_click import UIClicker
from ..feedback import speak_and_log
from ..core.config import get_config

class CommandExecutor:
    """Execute commands by mapping them to their action implementations."""

    def __init__(self):
        """Initialize the command executor with action handlers."""
        self.launcher = Launcher()
        self.closer = Closer()
        self.window_manager = WindowManager()
        self.ui_typer = UITyper()
        self.ui_clicker = UIClicker()

    def execute_command(self, command_type, params, feedback=None):
        """
        Execute a command based on its type and parameters.

        Args:
            command_type (str): Type of command to execute
            params (dict): Parameters for the command
            feedback (Feedback): Feedback system for user interaction

        Returns:
            dict: Result with success status and message
        """
        try:
            if command_type == 'launch':
                app_name = params.get('app_name', '')
                return self.launcher.launch_application(app_name)

            elif command_type == 'close':
                app_name = params.get('app_name', None)
                # Get confirmation setting from config
                confirmations_enabled = get_config('confirmations', True)
                return self.closer.close_application(app_name, confirm=confirmations_enabled)

            elif command_type == 'minimize':
                window_title = params.get('window_title', None)
                return self.window_manager.minimize_window(window_title)

            elif command_type == 'maximize':
                window_title = params.get('window_title', None)
                return self.window_manager.maximize_window(window_title)

            elif command_type == 'bring_to_front':
                window_title = params.get('window_title', None)
                return self.window_manager.bring_to_front(window_title)

            elif command_type == 'click':
                element_text = params.get('element_text', '')
                return self.ui_clicker.click_element(element_text, feedback=feedback)

            elif command_type == 'type_text':
                element_text = params.get('element_text', '')
                text_to_type = params.get('text_to_type', '')
                return self.ui_typer.type_into_field(element_text, text_to_type, feedback=feedback)

            elif command_type == 'read_screen':
                region = params.get('region', None)
                # Note: Screen reading functionality is not fully implemented yet
                return {
                    'success': False,
                    'message': 'Screen reading functionality not yet implemented'
                }

            elif command_type == 'help':
                help_text = (
                    "Доступные команды:\n"
                    "- Запустить приложение [имя]\n"
                    "- Закрыть приложение [имя]\n"
                    "- Свернуть окно\n"
                    "- Развернуть окно\n"
                    "- Перевести окно в фокус\n"
                    "- Прочитать текст с экрана\n"
                    "- Кликнуть на [текст]\n"
                    "- Ввести в поле [текст]\n"
                    "- Помощь"
                )
                speak_and_log(help_text)
                return {
                    'success': True,
                    'message': 'Help information displayed'
                }

            else:
                return {
                    'success': False,
                    'message': f'Unknown command type: {command_type}'
                }

        except Exception as e:
            return {
                'success': False,
                'message': f'Error executing command "{command_type}": {str(e)}'
            }