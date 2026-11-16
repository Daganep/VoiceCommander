#!/usr/bin/env python3
"""
Voice Commander for Windows - Main Entry Point
Offline voice control application for Windows using Vosk and Tesseract OCR.
"""

import sys
import os
import argparse

# Add the current directory to the Python path so we can import modules
sys.path.insert(0, os.path.dirname(__file__))

def main():
    """Main entry point for the Voice Commander application."""
    try:
        parser = argparse.ArgumentParser(description='Voice Commander for Windows')
        parser.add_argument('--text', action='store_true', help='Run in text mode for testing')

        args = parser.parse_args()

        if args.text:
            # Import and run text interface
            from voice_commander.text_interface import main as text_main
            text_main()
        else:
            print("Voice Commander initialized")
            # TODO: Implement main loop and command processing

    except Exception as e:
        print(f"Fatal error in main: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()