#!/usr/bin/env python3
"""
Test script for STT module functionality.
"""

import sys
import os

# Add the current directory to the Python path so we can import modules
sys.path.insert(0, os.path.dirname(__file__))

from voice_commander.core.speech.stt import STT

def test_stt_initialization():
    """Test that STT module initializes correctly."""
    print("Testing STT initialization...")

    try:
        stt = STT(model_path="models")
        print("✓ STT object created successfully")

        # Test model loading
        if stt.load_model():
            print("✓ Vosk model loaded successfully")
        else:
            print("✗ Failed to load Vosk model")
            return False

        print("✓ STT initialization test passed")
        return True

    except Exception as e:
        print(f"✗ STT initialization failed: {e}")
        return False

def main():
    """Main test function."""
    print("Running STT module tests...")
    print("=" * 40)

    success = test_stt_initialization()

    if success:
        print("\n✓ All tests passed!")
    else:
        print("\n✗ Some tests failed!")
        sys.exit(1)

if __name__ == "__main__":
    main()