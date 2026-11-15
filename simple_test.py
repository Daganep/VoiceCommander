#!/usr/bin/env python3
"""
Simple test to verify the development environment setup.
"""

import sys
import os

# Add the core directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'core'))

def main():
    """Test that all required modules can be imported."""
    try:
        import vosk
        print("Vosk imported successfully")

        import pyttsx3
        print("Pyttsx3 imported successfully")

        import pytesseract
        print("Pytesseract imported successfully")

        import pywinauto
        print("Pywinauto imported successfully")

        import pyautogui
        print("Pyautogui imported successfully")

        import psutil
        print("Psutil imported successfully")

        import yaml
        print("PyYAML imported successfully")

        import pystray
        print("Pystray imported successfully")

        # Test importing core modules
        import core.speech.stt
        print("STT module imported successfully")

        import core.speech.tts
        print("TTS module imported successfully")

        import core.commands.parser
        print("Parser module imported successfully")

        import core.commands.schema
        print("Schema module imported successfully")

        print("\nAll modules imported successfully - setup complete!")
        return True

    except Exception as e:
        print(f"Error importing modules: {e}")
        return False

if __name__ == "__main__":
    main()