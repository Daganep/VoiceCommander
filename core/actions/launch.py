"""
Application launching module for Voice Commander.
Handles launching applications by name or path.
"""

import os
import subprocess
import sys
from typing import List, Dict, Optional
from pathlib import Path

from core.feedback import speak_and_log
from core.logger import get_logger
from core.apps.registry import AppRegistry
from core.apps.processes import ProcessManager

logger = get_logger(__name__)


class ApplicationLauncher:
    """Handles launching applications with various methods."""

    def __init__(self):
        """Initialize the application launcher."""
        self.registry = AppRegistry()
        self.process_manager = ProcessManager()
        logger.info("Application launcher initialized")

    def launch_application(self, app_name: str) -> str:
        """
        Launch an application by name or path.

        Args:
            app_name (str): Name or path of the application to launch

        Returns:
            str: Result message about the launch operation
        """
        try:
            # First check if it's a registered alias
            if app_name in self.registry.get_all_aliases():
                app_path = self.registry.get_app_path(app_name)
                logger.info(f"Launching registered application: {app_name} -> {app_path}")
                return self._launch_by_path(app_path, app_name)

            # Check if it's a full path to an executable
            if os.path.isabs(app_name) and app_name.endswith(('.exe', '.bat', '.cmd')):
                logger.info(f"Launching application by absolute path: {app_name}")
                return self._launch_by_path(app_name, app_name)

            # Check if it's a relative path to an executable
            if not os.path.isabs(app_name) and app_name.endswith(('.exe', '.bat', '.cmd')):
                # Try to resolve relative path
                full_path = Path(app_name).resolve()
                if full_path.exists() and full_path.suffix in ('.exe', '.bat', '.cmd'):
                    logger.info(f"Launching application by relative path: {app_name}")
                    return self._launch_by_path(str(full_path), app_name)

            # Try to find the application in PATH or common locations
            logger.info(f"Searching for application in PATH: {app_name}")
            return self._launch_by_name(app_name)

        except Exception as e:
            error_msg = f"Failed to launch application '{app_name}': {str(e)}"
            logger.error(error_msg)
            speak_and_log(f"Ошибка запуска приложения: {app_name}")
            return error_msg

    def _launch_by_path(self, app_path: str, app_name: str) -> str:
        """
        Launch an application by its full path.

        Args:
            app_path (str): Full path to the executable
            app_name (str): Name of the application

        Returns:
            str: Result message about the launch operation
        """
        try:
            if not os.path.exists(app_path):
                raise FileNotFoundError(f"Application not found: {app_path}")

            # Check if it's an executable file
            if not os.access(app_path, os.X_OK) and not app_path.endswith(('.exe', '.bat', '.cmd')):
                raise PermissionError(f"File is not executable: {app_path}")

            # Launch the application
            logger.info(f"Launching application from path: {app_path}")
            process = subprocess.Popen([app_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

            # Wait a bit to check if it started successfully
            process.wait(timeout=5)

            # Check if process started correctly
            if process.returncode == 0:
                speak_and_log(f"Приложение {app_name} запущено")
                return f"Успешно запущено: {app_name}"
            else:
                error_output = process.stderr.read().decode('utf-8') if process.stderr else "Unknown error"
                raise subprocess.SubprocessError(f"Process failed to start: {error_output}")

        except subprocess.TimeoutExpired:
            # Process started successfully, but we timed out waiting for it to finish
            speak_and_log(f"Приложение {app_name} запущено")
            return f"Успешно запущено: {app_name}"
        except Exception as e:
            error_msg = f"Failed to launch application from path '{app_path}': {str(e)}"
            logger.error(error_msg)
            speak_and_log(f"Ошибка запуска приложения: {app_name}")
            raise

    def _launch_by_name(self, app_name: str) -> str:
        """
        Launch an application by name using Windows search capabilities.

        Args:
            app_name (str): Name of the application to launch

        Returns:
            str: Result message about the launch operation
        """
        try:
            # Try to find in PATH first
            if self._is_in_path(app_name):
                logger.info(f"Found application in PATH: {app_name}")
                process = subprocess.Popen([app_name], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                return f"Запущено из PATH: {app_name}"

            # Try to find via Windows Start menu search (using PowerShell)
            logger.info(f"Attempting to launch application by name: {app_name}")

            # Use PowerShell to start the application
            ps_command = f'Start-Process -FilePath "{app_name}"'
            process = subprocess.Popen(['powershell', '-Command', ps_command],
                                     stdout=subprocess.PIPE, stderr=subprocess.PIPE)

            # Give it a moment to start
            process.wait(timeout=5)

            if process.returncode == 0:
                speak_and_log(f"Приложение {app_name} запущено")
                return f"Успешно запущено: {app_name}"
            else:
                error_output = process.stderr.read().decode('utf-8') if process.stderr else "Unknown error"
                raise subprocess.SubprocessError(f"Process failed to start: {error_output}")

        except Exception as e:
            # If PowerShell method fails, try with system PATH
            try:
                logger.warning(f"Failed to launch by name via PowerShell, trying PATH: {app_name}")
                process = subprocess.Popen([app_name], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                return f"Запущено из PATH: {app_name}"
            except Exception as e2:
                error_msg = f"Failed to launch application '{app_name}': {str(e2)}"
                logger.error(error_msg)
                speak_and_log(f"Ошибка запуска приложения: {app_name}")
                raise

    def _is_in_path(self, app_name: str) -> bool:
        """
        Check if an application exists in the system PATH.

        Args:
            app_name (str): Name of the application

        Returns:
            bool: True if application is found in PATH
        """
        try:
            # Try to find it using which (on Windows, this would be where)
            if sys.platform.startswith('win'):
                result = subprocess.run(['where', app_name],
                                      stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                      text=True, timeout=5)
                return result.returncode == 0
            else:
                # For non-Windows systems, use which
                result = subprocess.run(['which', app_name],
                                      stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                      text=True, timeout=5)
                return result.returncode == 0
        except Exception:
            return False


def launch_application(app_name: str) -> str:
    """
    Launch an application by name or path.

    This is the main function that can be called from command processing.

    Args:
        app_name (str): Name or path of the application to launch

    Returns:
        str: Result message about the launch operation
    """
    try:
        launcher = ApplicationLauncher()
        return launcher.launch_application(app_name)
    except Exception as e:
        error_msg = f"Failed to launch application '{app_name}': {str(e)}"
        logger.error(error_msg)
        speak_and_log(f"Ошибка запуска приложения: {app_name}")
        return error_msg