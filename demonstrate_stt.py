#!/usr/bin/env python3
"""
Demonstration script for STT module functionality.
This script shows how to use the Vosk speech-to-text functionality.
"""

import sys
import os

# Add the current directory to the Python path so we can import modules
sys.path.insert(0, os.path.dirname(__file__))

from voice_commander.core.speech.stt import STT
import logging

# Configure logging to see what's happening
logging.basicConfig(level=logging.INFO)

def main():
    """Demonstrate STT functionality."""
    print("Voice Commander - STT Demonstration")
    print("=" * 40)

    try:
        # Create STT instance
        stt = STT(model_path="models")

        # Load the model
        print("Loading Vosk model...")
        if stt.load_model():
            print("✓ Model loaded successfully")

            # Show available audio devices
            print("\nAvailable audio devices:")
            devices = stt.get_audio_devices()
            for i, device in enumerate(devices):
                print(f"  {i}: {device['name']} (Sample Rate: {device['defaultSampleRate']})")

            print("\nSTT module is ready to use.")
            print("To test voice recognition:")
            print("1. Press Ctrl+Alt+V to activate push-to-talk")
            print("2. Speak your command")
            print("3. The recognized text will be displayed")
            print("4. Press Ctrl+C to exit")

        else:
            print("✗ Failed to load model")
            return

    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()