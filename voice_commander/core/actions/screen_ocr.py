"""
Screen text reading functionality using OCR.
"""

from ..ui.ocr import OCR

class ScreenOCR:
    """Read text from screen regions using OCR."""

    def __init__(self):
        """Initialize the screen OCR reader."""
        self.ocr = OCR()

    def read_screen_region(self, region=None):
        """
        Read text from a screen region.

        Args:
            region (tuple): Region coordinates (left, top, width, height)
                           If None, reads entire screen

        Returns:
            dict: Result with success status, message, and extracted text
        """
        try:
            if region:
                # Read specific region
                text = self.ocr.read_text_from_region(region)
            else:
                # Read entire screen
                text = self.ocr.read_entire_screen()

            return {
                'success': True,
                'message': 'Text read successfully',
                'text': text
            }

        except Exception as e:
            return {
                'success': False,
                'message': f'Error reading screen: {str(e)}',
                'text': ''
            }