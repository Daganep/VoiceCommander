"""
Application closing module for Voice Commander.
Handles closing applications by name or PID.
"""

import sys
from typing import Optional

from core.feedback import speak_and_log
from core.logger import get_logger
from core.apps.processes import ProcessManager
from voice_commander.core.config import get_config

logger = get_logger(__name__)


class ApplicationCloser:
    """Handles closing applications."""

    def __init__(self):
        """Initialize the application closer."""
        self.process_manager = ProcessManager()
        logger.info("Application closer initialized")

    def close_application(self, app_name: str, confirm: bool = True) -> str:
        """
        Close an application by name.

        Args:
            app_name (str): Name of the application to close
            confirm (bool): Whether to ask for confirmation before closing

        Returns:
            str: Result message about the closing operation
        """
        try:
            # Find processes matching the application name
            processes = self.process_manager.find_process_by_name(app_name)

            if not processes:
                logger.info(f"No processes found matching '{app_name}'")
                speak_and_log(f"Приложение {app_name} не запущено")
                return f"Приложение {app_name} не найдено"

            # Check if confirmation is enabled in config
            confirmations_enabled = get_config('confirmations', True)

            # If confirmation is enabled and we're asked to confirm, ask user
            if confirm and confirmations_enabled:
                # Ask for confirmation
                speak_and_log(f"Вы уверены, что хотите закрыть приложение {app_name}? Повторите команду для подтверждения")
                return f"Подтвердите закрытие приложения {app_name}"

            # Terminate all matching processes
            terminated_count = 0
            for proc in processes:
                if self.process_manager.terminate_process(proc['pid']):
                    terminated_count += 1
                    logger.info(f"Terminated process {proc['name']} (PID: {proc['pid']})")

            if terminated_count > 0:
                speak_and_log(f"Закрыто приложение: {app_name}")
                return f"Успешно закрыто: {app_name} ({terminated_count} процессов)"
            else:
                speak_and_log(f"Ошибка закрытия приложения: {app_name}")
                return f"Не удалось закрыть приложение: {app_name}"

        except Exception as e:
            error_msg = f"Failed to close application '{app_name}': {str(e)}"
            logger.error(error_msg)
            speak_and_log(f"Ошибка закрытия приложения: {app_name}")
            return error_msg


def close_application(app_name: str, confirm: bool = True) -> str:
    """
    Close an application by name.

    This is the main function that can be called from command processing.

    Args:
        app_name (str): Name of the application to close
        confirm (bool): Whether to ask for confirmation before closing

    Returns:
        str: Result message about the closing operation
    """
    try:
        closer = ApplicationCloser()
        return closer.close_application(app_name, confirm)
    except Exception as e:
        error_msg = f"Failed to close application '{app_name}': {str(e)}"
        logger.error(error_msg)
        speak_and_log(f"Ошибка закрытия приложения: {app_name}")
        return error_msg