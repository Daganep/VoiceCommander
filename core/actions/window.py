"""
Window management module for Voice Commander.
Handles window control operations like minimize, maximize, restore, and bring to front.
"""

import sys
import time
from typing import List, Dict, Optional
from pathlib import Path

# Try to import pywinauto - this is the main library for Windows automation
try:
    import pywinauto
    from pywinauto import Application
    from pywinauto.findwindows import find_windows
    from pywinauto.timings import Timeout
    PYWINAUTO_AVAILABLE = True
except ImportError:
    PYWINAUTO_AVAILABLE = False
    print("Warning: pywinauto not available for window management")

from core.feedback import speak_and_log
from core.logger import get_logger

logger = get_logger(__name__)


class WindowManager:
    """Handles window control operations."""

    def __init__(self):
        """Initialize the window manager."""
        self.applications = {}
        logger.info("Window manager initialized")

        # Set timeout for pywinauto operations
        Timeout.windows_open = 10.0
        Timeout.window_find = 5.0

    def _get_active_window(self):
        """
        Get the currently active window.

        Returns:
            Window object or None if no active window found
        """
        try:
            if not PYWINAUTO_AVAILABLE:
                return None

            # Get the foreground window (active window)
            from pywinauto import Desktop
            desktop = Desktop(backend="uia")
            active_window = desktop.windows()[0] if desktop.windows() else None
            return active_window
        except Exception as e:
            logger.error(f"Error getting active window: {e}")
            return None

    def _find_window_by_title(self, title: str) -> Optional['pywinauto.window']:
        """
        Find a window by its title.

        Args:
            title (str): Title of the window to find

        Returns:
            Window object or None if not found
        """
        try:
            if not PYWINAUTO_AVAILABLE:
                return None

            # Use pywinauto to find windows with matching titles
            windows = find_windows(title=title)
            if windows:
                app = Application(backend="uia").connect(handle=windows[0])
                return app.window(handle=windows[0])
            return None
        except Exception as e:
            logger.error(f"Error finding window by title '{title}': {e}")
            return None

    def _find_window_by_partial_title(self, partial_title: str) -> Optional['pywinauto.window']:
        """
        Find a window by partial title match.

        Args:
            partial_title (str): Partial title to search for

        Returns:
            Window object or None if not found
        """
        try:
            if not PYWINAUTO_AVAILABLE:
                return None

            # Search for windows with partial title match
            windows = find_windows(title_re=f".*{partial_title}.*")
            if windows:
                app = Application(backend="uia").connect(handle=windows[0])
                return app.window(handle=windows[0])
            return None
        except Exception as e:
            logger.error(f"Error finding window by partial title '{partial_title}': {e}")
            return None

    def maximize_window(self, window_title: str = None) -> str:
        """
        Maximize a window.

        Args:
            window_title (str): Title of the window to maximize. If None, maximizes active window.

        Returns:
            str: Result message
        """
        try:
            if not PYWINAUTO_AVAILABLE:
                error_msg = "pywinauto not available for window management"
                logger.error(error_msg)
                speak_and_log("Ошибка: библиотека управления окнами недоступна")
                return error_msg

            # If no window title specified, work with active window
            if window_title is None:
                window = self._get_active_window()
                if not window:
                    logger.warning("No active window found for maximizing")
                    speak_and_log("Ошибка: не удалось найти активное окно")
                    return "Не удалось найти активное окно для максимизации"
            else:
                # Try to find window by exact title first
                window = self._find_window_by_title(window_title)
                if not window:
                    # Try with partial title match
                    window = self._find_window_by_partial_title(window_title)

            if window:
                # Maximize the window
                window.maximize()
                logger.info(f"Window maximized: {window_title or 'active window'}")
                speak_and_log("Окно максимизировано")
                return "Окно успешно максимизировано"
            else:
                error_msg = f"Не удалось найти окно с заголовком: {window_title}"
                logger.error(error_msg)
                speak_and_log(f"Ошибка: не найдено окно '{window_title}'")
                return error_msg

        except Exception as e:
            error_msg = f"Failed to maximize window '{window_title}': {str(e)}"
            logger.error(error_msg)
            speak_and_log("Ошибка при максимизации окна")
            return error_msg

    def minimize_window(self, window_title: str = None) -> str:
        """
        Minimize a window.

        Args:
            window_title (str): Title of the window to minimize. If None, minimizes active window.

        Returns:
            str: Result message
        """
        try:
            if not PYWINAUTO_AVAILABLE:
                error_msg = "pywinauto not available for window management"
                logger.error(error_msg)
                speak_and_log("Ошибка: библиотека управления окнами недоступна")
                return error_msg

            # If no window title specified, work with active window
            if window_title is None:
                window = self._get_active_window()
                if not window:
                    logger.warning("No active window found for minimizing")
                    speak_and_log("Ошибка: не удалось найти активное окно")
                    return "Не удалось найти активное окно для минимизации"
            else:
                # Try to find window by exact title first
                window = self._find_window_by_title(window_title)
                if not window:
                    # Try with partial title match
                    window = self._find_window_by_partial_title(window_title)

            if window:
                # Minimize the window
                window.minimize()
                logger.info(f"Window minimized: {window_title or 'active window'}")
                speak_and_log("Окно свернуто")
                return "Окно успешно свернуто"
            else:
                error_msg = f"Не удалось найти окно с заголовком: {window_title}"
                logger.error(error_msg)
                speak_and_log(f"Ошибка: не найдено окно '{window_title}'")
                return error_msg

        except Exception as e:
            error_msg = f"Failed to minimize window '{window_title}': {str(e)}"
            logger.error(error_msg)
            speak_and_log("Ошибка при минимизации окна")
            return error_msg

    def restore_window(self, window_title: str = None) -> str:
        """
        Restore a minimized window.

        Args:
            window_title (str): Title of the window to restore. If None, restores active window.

        Returns:
            str: Result message
        """
        try:
            if not PYWINAUTO_AVAILABLE:
                error_msg = "pywinauto not available for window management"
                logger.error(error_msg)
                speak_and_log("Ошибка: библиотека управления окнами недоступна")
                return error_msg

            # If no window title specified, work with active window
            if window_title is None:
                window = self._get_active_window()
                if not window:
                    logger.warning("No active window found for restoring")
                    speak_and_log("Ошибка: не удалось найти активное окно")
                    return "Не удалось найти активное окно для восстановления"
            else:
                # Try to find window by exact title first
                window = self._find_window_by_title(window_title)
                if not window:
                    # Try with partial title match
                    window = self._find_window_by_partial_title(window_title)

            if window:
                # Restore the window (unminimize)
                window.restore()
                logger.info(f"Window restored: {window_title or 'active window'}")
                speak_and_log("Окно восстановлено")
                return "Окно успешно восстановлено"
            else:
                error_msg = f"Не удалось найти окно с заголовком: {window_title}"
                logger.error(error_msg)
                speak_and_log(f"Ошибка: не найдено окно '{window_title}'")
                return error_msg

        except Exception as e:
            error_msg = f"Failed to restore window '{window_title}': {str(e)}"
            logger.error(error_msg)
            speak_and_log("Ошибка при восстановлении окна")
            return error_msg

    def bring_to_front(self, window_title: str = None) -> str:
        """
        Bring a window to front (focus it).

        Args:
            window_title (str): Title of the window to bring to front. If None, brings active window to front.

        Returns:
            str: Result message
        """
        try:
            if not PYWINAUTO_AVAILABLE:
                error_msg = "pywinauto not available for window management"
                logger.error(error_msg)
                speak_and_log("Ошибка: библиотека управления окнами недоступна")
                return error_msg

            # If no window title specified, work with active window
            if window_title is None:
                window = self._get_active_window()
                if not window:
                    logger.warning("No active window found for bringing to front")
                    speak_and_log("Ошибка: не удалось найти активное окно")
                    return "Не удалось найти активное окно для перевода в фокус"
            else:
                # Try to find window by exact title first
                window = self._find_window_by_title(window_title)
                if not window:
                    # Try with partial title match
                    window = self._find_window_by_partial_title(window_title)

            if window:
                # Bring window to front
                window.set_focus()
                logger.info(f"Window brought to front: {window_title or 'active window'}")
                speak_and_log("Окно переведено в фокус")
                return "Окно успешно переведено в фокус"
            else:
                error_msg = f"Не удалось найти окно с заголовком: {window_title}"
                logger.error(error_msg)
                speak_and_log(f"Ошибка: не найдено окно '{window_title}'")
                return error_msg

        except Exception as e:
            error_msg = f"Failed to bring window '{window_title}' to front: {str(e)}"
            logger.error(error_msg)
            speak_and_log("Ошибка при переводе окна в фокус")
            return error_msg

    def list_windows(self) -> str:
        """
        List all available windows.

        Returns:
            str: Result message with window information
        """
        try:
            if not PYWINAUTO_AVAILABLE:
                error_msg = "pywinauto not available for window management"
                logger.error(error_msg)
                speak_and_log("Ошибка: библиотека управления окнами недоступна")
                return error_msg

            # Get all windows
            windows = find_windows()

            if not windows:
                logger.info("No windows found")
                speak_and_log("Окон не найдено")
                return "Окон не найдено"

            window_info = []
            for i, handle in enumerate(windows[:10]):  # Limit to first 10 windows
                try:
                    app = Application(backend="uia").connect(handle=handle)
                    window = app.window(handle=handle)
                    title = window.window_text() if window else "Unknown"
                    window_info.append(f"{i+1}. {title}")
                except Exception as e:
                    logger.warning(f"Could not get info for window handle {handle}: {e}")
                    window_info.append(f"{i+1}. Unknown window")

            result_msg = "Доступные окна:\n" + "\n".join(window_info)
            logger.info(f"Found {len(windows)} windows")
            return result_msg

        except Exception as e:
            error_msg = f"Failed to list windows: {str(e)}"
            logger.error(error_msg)
            speak_and_log("Ошибка при получении списка окон")
            return error_msg

    def get_window_info(self, window_title: str) -> str:
        """
        Get detailed information about a specific window.

        Args:
            window_title (str): Title of the window to get info for

        Returns:
            str: Result message with window information
        """
        try:
            if not PYWINAUTO_AVAILABLE:
                error_msg = "pywinauto not available for window management"
                logger.error(error_msg)
                speak_and_log("Ошибка: библиотека управления окнами недоступна")
                return error_msg

            # Try to find window by exact title first
            window = self._find_window_by_title(window_title)
            if not window:
                # Try with partial title match
                window = self._find_window_by_partial_title(window_title)

            if window:
                try:
                    title = window.window_text()
                    bounds = window.rectangle()
                    is_active = window.is_active()

                    info = f"Информация об окне:\n"
                    info += f"Заголовок: {title}\n"
                    info += f"Размеры: {bounds.width()}x{bounds.height()}\n"
                    info += f"Позиция: ({bounds.left}, {bounds.top})\n"
                    info += f"Активно: {'Да' if is_active else 'Нет'}"

                    logger.info(f"Got window info for: {window_title}")
                    return info
                except Exception as e:
                    error_msg = f"Could not get window information: {str(e)}"
                    logger.error(error_msg)
                    return error_msg
            else:
                error_msg = f"Не удалось найти окно с заголовком: {window_title}"
                logger.error(error_msg)
                speak_and_log(f"Ошибка: не найдено окно '{window_title}'")
                return error_msg

        except Exception as e:
            error_msg = f"Failed to get window info for '{window_title}': {str(e)}"
            logger.error(error_msg)
            speak_and_log("Ошибка при получении информации об окне")
            return error_msg


def maximize_window(window_title: str = None) -> str:
    """
    Maximize a window.

    Args:
        window_title (str): Title of the window to maximize. If None, maximizes active window.

    Returns:
        str: Result message
    """
    try:
        wm = WindowManager()
        return wm.maximize_window(window_title)
    except Exception as e:
        error_msg = f"Failed to maximize window: {str(e)}"
        logger.error(error_msg)
        speak_and_log("Ошибка при максимизации окна")
        return error_msg


def minimize_window(window_title: str = None) -> str:
    """
    Minimize a window.

    Args:
        window_title (str): Title of the window to minimize. If None, minimizes active window.

    Returns:
        str: Result message
    """
    try:
        wm = WindowManager()
        return wm.minimize_window(window_title)
    except Exception as e:
        error_msg = f"Failed to minimize window: {str(e)}"
        logger.error(error_msg)
        speak_and_log("Ошибка при минимизации окна")
        return error_msg


def restore_window(window_title: str = None) -> str:
    """
    Restore a minimized window.

    Args:
        window_title (str): Title of the window to restore. If None, restores active window.

    Returns:
        str: Result message
    """
    try:
        wm = WindowManager()
        return wm.restore_window(window_title)
    except Exception as e:
        error_msg = f"Failed to restore window: {str(e)}"
        logger.error(error_msg)
        speak_and_log("Ошибка при восстановлении окна")
        return error_msg


def bring_to_front(window_title: str = None) -> str:
    """
    Bring a window to front.

    Args:
        window_title (str): Title of the window to bring to front. If None, brings active window to front.

    Returns:
        str: Result message
    """
    try:
        wm = WindowManager()
        return wm.bring_to_front(window_title)
    except Exception as e:
        error_msg = f"Failed to bring window to front: {str(e)}"
        logger.error(error_msg)
        speak_and_log("Ошибка при переводе окна в фокус")
        return error_msg


def list_windows() -> str:
    """
    List all available windows.

    Returns:
        str: Result message with window information
    """
    try:
        wm = WindowManager()
        return wm.list_windows()
    except Exception as e:
        error_msg = f"Failed to list windows: {str(e)}"
        logger.error(error_msg)
        speak_and_log("Ошибка при получении списка окон")
        return error_msg


def get_window_info(window_title: str) -> str:
    """
    Get detailed information about a specific window.

    Args:
        window_title (str): Title of the window to get info for

    Returns:
        str: Result message with window information
    """
    try:
        wm = WindowManager()
        return wm.get_window_info(window_title)
    except Exception as e:
        error_msg = f"Failed to get window info: {str(e)}"
        logger.error(error_msg)
        speak_and_log("Ошибка при получении информации об окне")
        return error_msg