"""
Command executor for voice commander.
This module maps command types to their corresponding action implementations.
"""

from ..actions.launch import Launcher
from ..actions.close import Closer
from ..actions.window import WindowManager
from ..feedback import speak_and_log

class CommandExecutor:
    """Execute commands by mapping them to their action implementations."""

    def __init__(self):
        """Initialize the command executor with action handlers."""
        self.launcher = Launcher()
        self.closer = Closer()
        self.window_manager = WindowManager()

    def execute_command(self, command_type, params):
        """
        Execute a command based on its type and parameters.

        Args:
            command_type (str): Type of command to execute
            params (dict): Parameters for the command

        Returns:
            dict: Result with success status and message
        """
        try:
            if command_type == 'launch':
                app_name = params.get('app_name', '')
                return self.launcher.launch_application(app_name)

            elif command_type == 'close':
                app_name = params.get('app_name', None)
                return self.closer.close_application(app_name)

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
                # Note: UI click functionality is not fully implemented yet
                return {
                    'success': False,
                    'message': 'UI click functionality not yet implemented'
                }

            elif command_type == 'type_text':
                element_text = params.get('element_text', '')
                text_to_type = params.get('text_to_type', '')
                # Note: UI typing functionality is not fully implemented yet
                return {
                    'success': False,
                    'message': 'UI typing functionality not yet implemented'
                }

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