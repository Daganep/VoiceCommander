"""
UI automation functionality using pywinauto.
"""

import pywinauto
from pywinauto import Application

class UIAutomation:
    """Provide UI automation capabilities."""

    def __init__(self):
        """Initialize the UI automation system."""
        pass

    def connect_to_application(self, app_name):
        """
        Connect to an application by name.

        Args:
            app_name (str): Name of the application to connect to

        Returns:
            Application: Connected application object
        """
        try:
            app = Application(backend="uia").connect(title=app_name)
            return app
        except Exception as e:
            print(f"Error connecting to application {app_name}: {e}")
            return None

    def find_window(self, window_title):
        """
        Find a window by title.

        Args:
            window_title (str): Title of the window to find

        Returns:
            Window: Found window object
        """
        try:
            app = Application(backend="uia").connect(title=window_title)
            window = app.window(title=window_title)
            return window
        except Exception as e:
            print(f"Error finding window {window_title}: {e}")
            return None

    def click_button(self, window_title, button_text):
        """
        Click a button in a window.

        Args:
            window_title (str): Title of the window containing the button
            button_text (str): Text of the button to click

        Returns:
            bool: True if successful, False otherwise
        """
        try:
            app = Application(backend="uia").connect(title=window_title)
            window = app.window(title=window_title)
            button = window.child_window(title=button_text, control_type="Button")
            button.click()
            return True
        except Exception as e:
            print(f"Error clicking button {button_text}: {e}")
            return False