"""
Text input into UI fields using OCR.
"""

import pyautogui
from ..ui.ocr import OCR
from ..actions.screen_ocr import ScreenOCR

class UITyper:
    """Type text into UI fields identified by OCR."""

    def __init__(self):
        """Initialize the UI typer."""
        self.ocr = OCR()

    def type_into_field(self, element_text, text_to_type, feedback=None):
        """
        Type text into a UI field identified by text.

        Args:
            element_text (str): Text that identifies the UI field
            text_to_type (str): Text to type into the field
            feedback (Feedback): Feedback system to provide user information

        Returns:
            dict: Result with success status and message
        """
        try:
            # First, let's check if there are multiple matches for this text
            screen_ocr = ScreenOCR()
            result = screen_ocr.find_all_text_on_screen(element_text)

            # Check if we found multiple matches
            if result['success'] and len(result['items']) > 1:
                # Handle ambiguity - let the user know about multiple options
                if feedback:
                    self._handle_ambiguous_command(element_text, result['items'], feedback)

                return {
                    'success': False,
                    'message': f'Found {len(result["items"])} matches for "{element_text}". Please be more specific.',
                    'ambiguous': True,
                    'options': result['items']
                }
            elif result['success'] and len(result['items']) == 1:
                # Single match - proceed with typing
                item = result['items'][0]
                x, y = item['coordinates']
                # Click to focus the field
                pyautogui.click(x, y)
                # Type the text
                pyautogui.typewrite(text_to_type)
                return {
                    'success': True,
                    'message': f'Typed "{text_to_type}" into field: {element_text}',
                    'item': item
                }
            else:
                # Try to find similar text
                coordinates = self.ocr.find_text_coordinates(element_text)

                if coordinates:
                    x, y = coordinates
                    # Click to focus the field
                    pyautogui.click(x, y)
                    # Type the text
                    pyautogui.typewrite(text_to_type)
                    return {
                        'success': True,
                        'message': f'Typed "{text_to_type}" into field: {element_text} (approximate match)'
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

    def _handle_ambiguous_command(self, element_text, items, feedback):
        """
        Handle ambiguous command by informing user about multiple matches.

        Args:
            element_text (str): The text that was searched for
            items (list): List of matching items found
            feedback (Feedback): Feedback system to provide user information
        """
        message = f'Найдено несколько полей с текстом "{element_text}". '
        message += 'Выберите один из вариантов:'

        # Add options with their coordinates for better context
        for i, item in enumerate(items[:5]):  # Limit to first 5 items
            x, y = item['coordinates']
            message += f' {i+1}. "{item["text"]}" в координатах ({x}, {y})'

        if len(items) > 5:
            message += f' и еще {len(items) - 5} вариантов.'

        feedback.speak_and_log(message, "WARNING")