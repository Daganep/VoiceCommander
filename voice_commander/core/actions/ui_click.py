"""
UI element clicking functionality using OCR.
"""

import pyautogui
from ..ui.ocr import OCR

class UIClicker:
    """Click UI elements identified by OCR."""

    def __init__(self):
        """Initialize the UI clicker."""
        self.ocr = OCR()

    def click_element(self, element_text):
        """
        Click on a UI element identified by text.

        Args:
            element_text (str): Text that identifies the UI element

        Returns:
            dict: Result with success status and message
        """
        try:
            # Use OCR to find the element on screen
            coordinates = self.ocr.find_text_coordinates(element_text)

            if coordinates:
                x, y = coordinates
                pyautogui.click(x, y)
                return {
                    'success': True,
                    'message': f'Clicked on element: {element_text} at ({x}, {y})'
                }
            else:
                return {
                    'success': False,
                    'message': f'Could not find UI element with text: {element_text}'
                }

        except Exception as e:
            return {
                'success': False,
                'message': f'Error clicking UI element: {str(e)}'
            }