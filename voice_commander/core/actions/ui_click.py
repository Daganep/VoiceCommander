"""
UI element clicking functionality using OCR.
"""

import pyautogui
import time
from ..ui.ocr import OCR
from ..actions.screen_ocr import ScreenOCR

class UIClicker:
    """Click UI elements identified by OCR."""

    def __init__(self):
        """Initialize the UI clicker."""
        self.ocr = OCR()

    def click_element(self, element_text, confidence_threshold=0.8, feedback=None):
        """
        Click on a UI element identified by text.

        Args:
            element_text (str): Text that identifies the UI element
            confidence_threshold (float): Minimum confidence level for matching text
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
                # Single match - proceed with click
                item = result['items'][0]
                x, y = item['coordinates']
                # Add a small delay to ensure system is ready
                time.sleep(0.1)
                pyautogui.click(x, y)
                return {
                    'success': True,
                    'message': f'Clicked on element: {element_text} at ({x}, {y})',
                    'coordinates': (x, y),
                    'item': item
                }
            else:
                # Try to find similar text
                result = self._find_similar_text(element_text)
                if result['success']:
                    x, y = result['coordinates']
                    time.sleep(0.1)
                    pyautogui.click(x, y)
                    return {
                        'success': True,
                        'message': f'Clicked on element: {element_text} (approximate match) at ({x}, {y})',
                        'coordinates': (x, y),
                        'approximate_match': True
                    }
                else:
                    return {
                        'success': False,
                        'message': f'Could not find UI element with text: {element_text}',
                        'approximate_match': False
                    }

        except Exception as e:
            return {
                'success': False,
                'message': f'Error clicking UI element: {str(e)}',
                'error': str(e)
            }

    def _handle_ambiguous_command(self, element_text, items, feedback):
        """
        Handle ambiguous command by informing user about multiple matches.

        Args:
            element_text (str): The text that was searched for
            items (list): List of matching items found
            feedback (Feedback): Feedback system to provide user information
        """
        message = f'Найдено несколько элементов с текстом "{element_text}". '
        message += 'Выберите один из вариантов:'

        # Add options with their coordinates for better context
        for i, item in enumerate(items[:5]):  # Limit to first 5 items
            x, y = item['coordinates']
            message += f' {i+1}. "{item["text"]}" в координатах ({x}, {y})'

        if len(items) > 5:
            message += f' и еще {len(items) - 5} вариантов.'

        feedback.speak_and_log(message, "WARNING")

    def _find_similar_text(self, target_text, max_distance=3):
        """
        Find text that is similar to the target text.

        Args:
            target_text (str): Text to search for
            max_distance (int): Maximum character distance for similarity

        Returns:
            dict: Result with success status and coordinates
        """
        try:
            # This approach will be more robust - we'll look at all text on screen
            # and find the closest match
            screen_ocr = ScreenOCR()
            result = screen_ocr.find_all_text_on_screen()

            if not result['success']:
                return {
                    'success': False,
                    'message': 'Could not read screen text for similarity search'
                }

            # Find closest match
            best_match = None
            min_distance = float('inf')

            for item in result['items']:
                text = item['text']
                if text:
                    # Simple character distance calculation (could be improved)
                    distance = self._calculate_edit_distance(target_text.lower(), text.lower())
                    if distance < min_distance and distance <= max_distance:
                        min_distance = distance
                        best_match = item

            if best_match:
                return {
                    'success': True,
                    'message': f'Found approximate match: {best_match["text"]}',
                    'coordinates': best_match['coordinates']
                }
            else:
                return {
                    'success': False,
                    'message': f'No similar text found for "{target_text}"'
                }

        except Exception as e:
            return {
                'success': False,
                'message': f'Error in similarity search: {str(e)}'
            }

    def _calculate_edit_distance(self, s1, s2):
        """
        Calculate edit distance between two strings.

        Args:
            s1 (str): First string
            s2 (str): Second string

        Returns:
            int: Edit distance
        """
        if len(s1) < len(s2):
            return self._calculate_edit_distance(s2, s1)

        if len(s2) == 0:
            return len(s1)

        previous_row = list(range(len(s2) + 1))
        for i, c1 in enumerate(s1):
            current_row = [i + 1]
            for j, c2 in enumerate(s2):
                insertions = previous_row[j + 1] + 1
                deletions = current_row[j] + 1
                substitutions = previous_row[j] + (c1 != c2)
                current_row.append(min(insertions, deletions, substitutions))
            previous_row = current_row

        return previous_row[-1]