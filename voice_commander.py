#!/usr/bin/env python3
"""
Voice Commander for Windows - Main Entry Point
Offline voice control application for Windows using Vosk and Tesseract OCR.
"""

import sys
import os

# Add the core directory to the Python path so we can import modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'core'))

def main():
    """Main entry point for the Voice Commander application."""
    print("Voice Commander initialized")
    # TODO: Implement main loop and command processing

if __name__ == "__main__":
    main()