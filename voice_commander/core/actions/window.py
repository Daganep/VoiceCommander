"""
Window management functionality using pywinauto.
"""

import pywinauto
from pywinauto import Application
import time

class WindowManager:
    """Manage window operations like minimize, maximize, etc."""

    def __init__(self):
        """Initialize the window manager."""
        pass

    def minimize_window(self, window_title=None):
        """
        Minimize a window.

        Args:
            window_title (str): Title of the window to minimize

        Returns:
            dict: Result with success status and message
        """
        try:
            if window_title:
                app = Application(backend="uia").connect(title=window_title)
                window = app.window(title=window_title)
                window.minimize()
                return {
                    'success': True,
                    'message': f'Minimized window: {window_title}'
                }
            else:
                # Minimize the active window
                app = Application(backend="uia").connect(handle=pywinauto.findwindows.find_elements(active_only=True)[0].handle)
                window = app.top_window()
                window.minimize()
                return {
                    'success': True,
                    'message': 'Minimized active window'
                }

        except Exception as e:
            return {
                'success': False,
                'message': f'Error minimizing window: {str(e)}'
            }

    def maximize_window(self, window_title=None):
        """
        Maximize a window.

        Args:
            window_title (str): Title of the window to maximize

        Returns:
            dict: Result with success status and message
        """
        try:
            if window_title:
                app = Application(backend="uia").connect(title=window_title)
                window = app.window(title=window_title)
                window.maximize()
                return {
                    'success': True,
                    'message': f'Maximized window: {window_title}'
                }
            else:
                # Maximize the active window
                app = Application(backend="uia").connect(handle=pywinauto.findwindows.find_elements(active_only=True)[0].handle)
                window = app.top_window()
                window.maximize()
                return {
                    'success': True,
                    'message': 'Maximized active window'
                }

        except Exception as e:
            return {
                'success': False,
                'message': f'Error maximizing window: {str(e)}'
            }

    def bring_to_front(self, window_title=None):
        """
        Bring a window to front.

        Args:
            window_title (str): Title of the window to bring to front

        Returns:
            dict: Result with success status and message
        """
        try:
            if window_title:
                app = Application(backend="uia").connect(title=window_title)
                window = app.window(title=window_title)
                window.set_focus()
                return {
                    'success': True,
                    'message': f'Brought window to front: {window_title}'
                }
            else:
                # Bring the active window to front
                app = Application(backend="uia").connect(handle=pywinauto.findwindows.find_elements(active_only=True)[0].handle)
                window = app.top_window()
                window.set_focus()
                return {
                    'success': True,
                    'message': 'Brought active window to front'
                }

        except Exception as e:
            return {
                'success': False,
                'message': f'Error bringing window to front: {str(e)}'
            }