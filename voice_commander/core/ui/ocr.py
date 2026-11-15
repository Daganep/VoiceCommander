"""
OCR functionality using Tesseract.
"""

import pytesseract
import cv2
import numpy as np
from PIL import Image
import pyautogui
import os

class OCR:
    """Provide OCR capabilities using Tesseract."""

    def __init__(self):
        """Initialize the OCR system."""
        # Set Tesseract path (adjust if needed)
        # pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

        # For Russian language support
        self.lang = 'rus'

    def read_text_from_region(self, region):
        """
        Read text from a specific screen region.

        Args:
            region (tuple): Region coordinates (left, top, width, height)

        Returns:
            str: Extracted text
        """
        try:
            left, top, width, height = region
            # Capture screenshot of the region
            screenshot = pyautogui.screenshot(region=(left, top, width, height))

            # Convert to OpenCV format for better processing
            img = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

            # Perform OCR
            text = pytesseract.image_to_string(img, lang=self.lang)
            return text.strip()
        except Exception as e:
            print(f"Error reading text from region {region}: {e}")
            return ""

    def read_entire_screen(self):
        """
        Read text from the entire screen.

        Returns:
            str: Extracted text
        """
        try:
            # Capture screenshot of entire screen
            screenshot = pyautogui.screenshot()

            # Convert to OpenCV format for better processing
            img = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

            # Perform OCR
            text = pytesseract.image_to_string(img, lang=self.lang)
            return text.strip()
        except Exception as e:
            print(f"Error reading entire screen: {e}")
            return ""

    def find_text_coordinates(self, text):
        """
        Find coordinates of text on screen.

        Args:
            text (str): Text to search for

        Returns:
            tuple: (x, y) coordinates or None if not found
        """
        try:
            # Capture screenshot of entire screen
            screenshot = pyautogui.screenshot()

            # Convert to OpenCV format
            img = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

            # Get bounding box for the text
            data = pytesseract.image_to_data(img, lang=self.lang, output_type=pytesseract.Output.DICT)

            # Search for the text in the OCR results
            for i, word in enumerate(data['text']):
                if text.lower() in word.lower():
                    x = data['left'][i]
                    y = data['top'][i]
                    return (x, y)

            return None
        except Exception as e:
            print(f"Error finding text coordinates: {e}")
            return None