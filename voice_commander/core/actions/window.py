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

    def focus_window(self, window_title):
        """
        Focus on a specific window by title.

        Args:
            window_title (str): Title of the window to focus

        Returns:
            dict: Result with success status and message
        """
        try:
            app = Application(backend="uia").connect(title=window_title)
            window = app.window(title=window_title)
            window.set_focus()
            return {
                'success': True,
                'message': f'Focused on window: {window_title}'
            }
        except Exception as e:
            return {
                'success': False,
                'message': f'Error focusing on window: {str(e)}'
            }

    def move_window(self, window_title, x, y):
        """
        Move a window to specific coordinates.

        Args:
            window_title (str): Title of the window to move
            x (int): X coordinate
            y (int): Y coordinate

        Returns:
            dict: Result with success status and message
        """
        try:
            app = Application(backend="uia").connect(title=window_title)
            window = app.window(title=window_title)
            window.move_window(x, y, None, None)
            return {
                'success': True,
                'message': f'Moved window "{window_title}" to ({x}, {y})'
            }
        except Exception as e:
            return {
                'success': False,
                'message': f'Error moving window: {str(e)}'
            }

    def resize_window(self, window_title, width, height):
        """
        Resize a window to specific dimensions.

        Args:
            window_title (str): Title of the window to resize
            width (int): New width
            height (int): New height

        Returns:
            dict: Result with success status and message
        """
        try:
            app = Application(backend="uia").connect(title=window_title)
            window = app.window(title=window_title)
            window.move_window(None, None, width, height)
            return {
                'success': True,
                'message': f'Resized window "{window_title}" to {width}x{height}'
            }
        except Exception as e:
            return {
                'success': False,
                'message': f'Error resizing window: {str(e)}'
            }

    def get_window_info(self, window_title):
        """
        Get information about a specific window.

        Args:
            window_title (str): Title of the window to get info for

        Returns:
            dict: Result with success status and window information
        """
        try:
            app = Application(backend="uia").connect(title=window_title)
            window = app.window(title=window_title)

            # Get window properties
            window_info = {
                'title': window_title,
                'is_maximized': window.is_maximized(),
                'is_minimized': window.is_minimized(),
                'is_visible': window.is_visible(),
                'rectangle': window.rectangle()
            }

            return {
                'success': True,
                'message': f'Window info for: {window_title}',
                'data': window_info
            }
        except Exception as e:
            return {
                'success': False,
                'message': f'Error getting window info: {str(e)}'
            }

    def restore_window_state(self, window_title):
        """
        Restore a window to its previous state (maximized, minimized, normal).

        Args:
            window_title (str): Title of the window to restore

        Returns:
            dict: Result with success status and message
        """
        try:
            app = Application(backend="uia").connect(title=window_title)
            window = app.window(title=window_title)

            # This function will restore window to its previous state
            # For now, we'll just ensure it's restored to normal state
            if window.is_maximized():
                window.restore()
            elif window.is_minimized():
                window.restore()

            return {
                'success': True,
                'message': f'Restored window state for: {window_title}'
            }
        except Exception as e:
            return {
                'success': False,
                'message': f'Error restoring window state: {str(e)}'
            }

    def list_windows(self):
        """
        List all visible windows.

        Returns:
            dict: Result with success status and list of window titles
        """
        try:
            # Find all visible windows
            windows = pywinauto.findwindows.find_elements(visible_only=True)
            window_titles = [window.text for window in windows if window.text]

            return {
                'success': True,
                'message': f'Found {len(window_titles)} visible windows',
                'data': window_titles
            }
        except Exception as e:
            return {
                'success': False,
                'message': f'Error listing windows: {str(e)}'
            }