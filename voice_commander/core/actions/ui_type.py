"""
Text input into UI fields using OCR.
"""

import pyautogui
from ..ui.ocr import OCR

class UITyper:
    """Type text into UI fields identified by OCR."""

    def __init__(self):
        """Initialize the UI typer."""
        self.ocr = OCR()

    def type_into_field(self, element_text, text_to_type):
        """
        Type text into a UI field identified by text.

        Args:
            element_text (str): Text that identifies the UI field
            text_to_type (str): Text to type into the field

        Returns:
            dict: Result with success status and message
        """
        try:
            # Use OCR to find the element on screen
            coordinates = self.ocr.find_text_coordinates(element_text)

            if coordinates:
                x, y = coordinates
                # Click to focus the field
                pyautogui.click(x, y)
                # Type the text
                pyautogui.typewrite(text_to_type)
                return {
                    'success': True,
                    'message': f'Typed "{text_to_type}" into field: {element_text}'
                }
            else:
                return {
                    'success': False,
                    'message': f'Could not find UI field with text: {element_text}'
                }

        except Exception as e:
            return {
                'success': False,
                'message': f'Error typing into UI field: {str(e)}'
            }