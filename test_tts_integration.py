#!/usr/bin/env python3
"""
Integration test for STT and TTS modules.
"""

import sys
import os

# Add the current directory to the Python path so we can import modules
sys.path.insert(0, os.path.dirname(__file__))

from voice_commander.core.speech.stt import STT
from voice_commander.core.speech.tts import TTS
from voice_commander.core.feedback import Feedback
from voice_commander.core.commands.parser import CommandParser

def test_tts_integration():
    """Test that TTS module works correctly."""
    print("Testing TTS integration...")

    try:
        # Initialize TTS
        tts = TTS()
        print("✓ TTS initialized successfully")

        # Test speaking
        tts.speak("Тестовая речь для проверки работы синтеза речи")
        print("✓ TTS speech test completed")

        return True

    except Exception as e:
        print(f"✗ TTS integration test failed: {e}")
        return False

def main():
    """Main test function."""
    print("Running STT/TTS integration tests...")
    print("=" * 50)

    success = test_tts_integration()

    if success:
        print("\n✓ All TTS integration tests passed!")
    else:
        print("\n✗ Some TTS integration tests failed!")
        sys.exit(1)

if __name__ == "__main__":
    main()