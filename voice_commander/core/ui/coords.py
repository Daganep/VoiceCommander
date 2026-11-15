"""
Coordinate and input actions using pyautogui.
"""

import pyautogui
import time

class Coordinates:
    """Provide coordinate-based actions and input."""

    def __init__(self):
        """Initialize the coordinates system."""
        # Set pyautogui pause between actions (in seconds)
        pyautogui.PAUSE = 0.1

    def click_at_coordinates(self, x, y):
        """
        Click at specific coordinates.

        Args:
            x (int): X coordinate
            y (int): Y coordinate

        Returns:
            dict: Result with success status and message
        """
        try:
            pyautogui.click(x, y)
            return {
                'success': True,
                'message': f'Clicked at coordinates ({x}, {y})'
            }
        except Exception as e:
            return {
                'success': False,
                'message': f'Error clicking at coordinates ({x}, {y}): {str(e)}'
            }

    def move_to_coordinates(self, x, y):
        """
        Move mouse to specific coordinates.

        Args:
            x (int): X coordinate
            y (int): Y coordinate

        Returns:
            dict: Result with success status and message
        """
        try:
            pyautogui.moveTo(x, y)
            return {
                'success': True,
                'message': f'Moved mouse to coordinates ({x}, {y})'
            }
        except Exception as e:
            return {
                'success': False,
                'message': f'Error moving mouse to coordinates ({x}, {y}): {str(e)}'
            }

    def type_text_at_coordinates(self, x, y, text):
        """
        Type text at specific coordinates.

        Args:
            x (int): X coordinate
            y (int): Y coordinate
            text (str): Text to type

        Returns:
            dict: Result with success status and message
        """
        try:
            # Move to coordinates
            pyautogui.moveTo(x, y)
            # Click to focus
            pyautogui.click(x, y)
            # Type the text
            pyautogui.typewrite(text)
            return {
                'success': True,
                'message': f'Typed "{text}" at coordinates ({x}, {y})'
            }
        except Exception as e:
            return {
                'success': False,
                'message': f'Error typing text at coordinates ({x}, {y}): {str(e)}'
            }

    def get_mouse_position(self):
        """
        Get current mouse position.

        Returns:
            tuple: (x, y) coordinates of mouse
        """
        try:
            x, y = pyautogui.position()
            return (x, y)
        except Exception as e:
            print(f"Error getting mouse position: {e}")
            return None

    def scroll(self, clicks):
        """
        Scroll the mouse.

        Args:
            clicks (int): Number of clicks to scroll (positive for up, negative for down)

        Returns:
            dict: Result with success status and message
        """
        try:
            pyautogui.scroll(clicks)
            return {
                'success': True,
                'message': f'Scrolled {clicks} clicks'
            }
        except Exception as e:
            return {
                'success': False,
                'message': f'Error scrolling: {str(e)}'
            }