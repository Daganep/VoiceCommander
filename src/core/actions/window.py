"""
Window management module for Voice Commander.
Provides functions for minimizing, maximizing, bringing windows to front, and closing windows.
"""

import pywinauto
from pywinauto import Application
import psutil
import time
from typing import Optional, List
import logging

# Configure logging
logger = logging.getLogger(__name__)

def get_windows() -> List[pywinauto.controls.hwndwrapper.HwndWrapper]:
    """
    Get list of all visible windows.

    Returns:
        List of window handles (HwndWrapper objects)
    """
    try:
        # Connect to desktop and get all top-level windows
        app = Application(backend="uia").connect()
        desktop = app.top_window()
        return desktop.descendants()
    except Exception as e:
        logger.error(f"Error getting windows: {e}")
        return []

def minimize_window(window_title: str) -> bool:
    """
    Minimize a window by title.

    Args:
        window_title (str): Title of the window to minimize

    Returns:
        bool: True if successful, False otherwise
    """
    try:
        app = Application(backend="uia").connect(title=window_title)
        window = app.top_window()
        window.minimize()
        logger.info(f"Minimized window: {window_title}")
        return True
    except Exception as e:
        logger.error(f"Failed to minimize window '{window_title}': {e}")
        return False

def maximize_window(window_title: str) -> bool:
    """
    Maximize a window by title.

    Args:
        window_title (str): Title of the window to maximize

    Returns:
        bool: True if successful, False otherwise
    """
    try:
        app = Application(backend="uia").connect(title=window_title)
        window = app.top_window()
        window.maximize()
        logger.info(f"Maximized window: {window_title}")
        return True
    except Exception as e:
        logger.error(f"Failed to maximize window '{window_title}': {e}")
        return False

def bring_to_front(window_title: str) -> bool:
    """
    Bring a window to front by title.

    Args:
        window_title (str): Title of the window to bring to front

    Returns:
        bool: True if successful, False otherwise
    """
    try:
        app = Application(backend="uia").connect(title=window_title)
        window = app.top_window()
        window.set_focus()
        logger.info(f"Brought window to front: {window_title}")
        return True
    except Exception as e:
        logger.error(f"Failed to bring window '{window_title}' to front: {e}")
        return False

def close_window(window_title: str) -> bool:
    """
    Close a window by title.

    Args:
        window_title (str): Title of the window to close

    Returns:
        bool: True if successful, False otherwise
    """
    try:
        app = Application(backend="uia").connect(title=window_title)
        window = app.top_window()
        window.close()
        logger.info(f"Closed window: {window_title}")
        return True
    except Exception as e:
        logger.error(f"Failed to close window '{window_title}': {e}")
        return False

def get_window_info(window_title: str) -> dict:
    """
    Get information about a specific window.

    Args:
        window_title (str): Title of the window to get info for

    Returns:
        dict: Dictionary with window information
    """
    try:
        app = Application(backend="uia").connect(title=window_title)
        window = app.top_window()

        # Get window properties
        info = {
            'title': window.window_text(),
            'is_minimized': window.is_minimized(),
            'is_maximized': window.is_maximized(),
            'is_visible': window.is_visible(),
            'is_active': window.is_active(),
            'bounds': window.rectangle()
        }

        logger.info(f"Got window info for: {window_title}")
        return info
    except Exception as e:
        logger.error(f"Failed to get window info for '{window_title}': {e}")
        return {}

def list_all_windows() -> List[str]:
    """
    List all visible windows.

    Returns:
        List of window titles
    """
    try:
        windows = []
        app = Application(backend="uia").connect()
        desktop = app.top_window()

        # Get all descendant windows (including child windows)
        descendants = desktop.descendants()
        for desc in descendants:
            try:
                title = desc.window_text()
                if title and len(title) > 0:
                    windows.append(title)
            except Exception:
                continue

        logger.info(f"Found {len(windows)} windows")
        return list(set(windows))  # Remove duplicates
    except Exception as e:
        logger.error(f"Error listing windows: {e}")
        return []

def focus_window_by_process(process_name: str) -> bool:
    """
    Focus a window by process name.

    Args:
        process_name (str): Name of the process to focus

    Returns:
        bool: True if successful, False otherwise
    """
    try:
        # Find process by name
        for proc in psutil.process_iter(['pid', 'name']):
            if proc.info['name'] == process_name:
                # Try to find and focus the window
                app = Application(backend="uia").connect(process=proc.info['pid'])
                window = app.top_window()
                window.set_focus()
                logger.info(f"Focused window for process: {process_name}")
                return True

        logger.warning(f"Process '{process_name}' not found")
        return False
    except Exception as e:
        logger.error(f"Failed to focus window for process '{process_name}': {e}")
        return False

if __name__ == "__main__":
    # Example usage for testing
    print("Window management module loaded")
    print("Available functions:")
    print("- minimize_window(window_title)")
    print("- maximize_window(window_title)")
    print("- bring_to_front(window_title)")
    print("- close_window(window_title)")
    print("- get_window_info(window_title)")
    print("- list_all_windows()")
    print("- focus_window_by_process(process_name)")