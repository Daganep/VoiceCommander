"""
Screen text reading functionality using OCR.
"""

import pyautogui
import cv2
import numpy as np
from PIL import Image
import pytesseract
import os
from ..ui.ocr import OCR

class ScreenOCR:
    """Read text from screen regions using OCR."""

    def __init__(self):
        """Initialize the screen OCR reader."""
        self.ocr = OCR()

    def capture_screen_region(self, region=None):
        """
        Capture a screenshot of a specific region or entire screen.

        Args:
            region (tuple): Region coordinates (left, top, width, height)
                           If None, captures entire screen

        Returns:
            PIL.Image: Screenshot image
        """
        try:
            if region:
                # Capture specific region
                screenshot = pyautogui.screenshot(region=region)
            else:
                # Capture entire screen
                screenshot = pyautogui.screenshot()

            return screenshot
        except Exception as e:
            raise Exception(f"Error capturing screenshot: {str(e)}")

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

    def get_screen_dimensions(self):
        """
        Get the dimensions of the primary screen.

        Returns:
            tuple: (width, height) of the screen
        """
        try:
            width, height = pyautogui.size()
            return (width, height)
        except Exception as e:
            raise Exception(f"Error getting screen dimensions: {str(e)}")

    def find_text_on_screen(self, search_text):
        """
        Find coordinates of text on screen.

        Args:
            search_text (str): Text to search for

        Returns:
            dict: Result with success status, message, and coordinates
        """
        try:
            # Capture screenshot of entire screen
            screenshot = pyautogui.screenshot()

            # Convert to OpenCV format for processing
            img = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

            # Get bounding box for the text
            data = pytesseract.image_to_data(img, lang=self.ocr.lang, output_type=pytesseract.Output.DICT)

            # Search for the text in the OCR results
            for i, word in enumerate(data['text']):
                if search_text.lower() in word.lower():
                    x = data['left'][i]
                    y = data['top'][i]
                    return {
                        'success': True,
                        'message': f'Found text at coordinates ({x}, {y})',
                        'coordinates': (x, y)
                    }

            return {
                'success': False,
                'message': f'Text "{search_text}" not found on screen',
                'coordinates': None
            }

        except Exception as e:
            return {
                'success': False,
                'message': f'Error searching for text: {str(e)}',
                'coordinates': None
            }

    def find_all_text_on_screen(self, search_text=None):
        """
        Find all occurrences of text on screen or all text if no search term provided.

        Args:
            search_text (str, optional): Text to search for. If None, returns all text.

        Returns:
            dict: Result with success status, message, and list of found text items
        """
        try:
            # Capture screenshot of entire screen
            screenshot = pyautogui.screenshot()

            # Convert to OpenCV format for processing
            img = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

            # Get all OCR data
            data = pytesseract.image_to_data(img, lang=self.ocr.lang, output_type=pytesseract.Output.DICT)

            results = []

            # If searching for specific text
            if search_text:
                for i, word in enumerate(data['text']):
                    if search_text.lower() in word.lower():
                        x = data['left'][i]
                        y = data['top'][i]
                        width = data['width'][i]
                        height = data['height'][i]
                        results.append({
                            'text': word,
                            'coordinates': (x, y),
                            'bounding_box': (x, y, width, height)
                        })
            else:
                # Return all text found
                for i in range(len(data['text'])):
                    if data['text'][i].strip():  # Only include non-empty text
                        x = data['left'][i]
                        y = data['top'][i]
                        width = data['width'][i]
                        height = data['height'][i]
                        results.append({
                            'text': data['text'][i],
                            'coordinates': (x, y),
                            'bounding_box': (x, y, width, height)
                        })

            if results:
                return {
                    'success': True,
                    'message': f'Found {len(results)} text items',
                    'items': results
                }
            else:
                return {
                    'success': False,
                    'message': f'No text found on screen' if not search_text else f'Text "{search_text}" not found',
                    'items': []
                }

        except Exception as e:
            return {
                'success': False,
                'message': f'Error searching for text: {str(e)}',
                'items': []
            }

    def find_ui_elements(self, element_labels):
        """
        Find UI elements (buttons, fields) by their labels using OCR.

        Args:
            element_labels (list): List of labels to search for

        Returns:
            dict: Result with success status, message, and found elements
        """
        try:
            # Capture screenshot of entire screen
            screenshot = pyautogui.screenshot()

            # Convert to OpenCV format for processing
            img = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

            # Get all OCR data
            data = pytesseract.image_to_data(img, lang=self.ocr.lang, output_type=pytesseract.Output.DICT)

            found_elements = []

            # Search for each element label in the OCR results
            for i, word in enumerate(data['text']):
                if word.strip():  # Only process non-empty text
                    x = data['left'][i]
                    y = data['top'][i]
                    width = data['width'][i]
                    height = data['height'][i]

                    # Check if this text matches any of our element labels (case insensitive)
                    for label in element_labels:
                        if label.lower() in word.lower():
                            found_elements.append({
                                'label': label,
                                'text': word,
                                'coordinates': (x, y),
                                'bounding_box': (x, y, width, height)
                            })
                            break  # Found match for this label, no need to check others

            if found_elements:
                return {
                    'success': True,
                    'message': f'Found {len(found_elements)} UI elements',
                    'elements': found_elements
                }
            else:
                return {
                    'success': False,
                    'message': f'No UI elements found matching labels: {element_labels}',
                    'elements': []
                }

        except Exception as e:
            return {
                'success': False,
                'message': f'Error finding UI elements: {str(e)}',
                'elements': []
            }