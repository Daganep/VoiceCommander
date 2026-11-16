#!/usr/bin/env python3
"""
Test script for Voice Recognition Module Development.
This script tests all aspects of the voice recognition functionality.
"""

import sys
import os
import time

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(__file__))

def test_stt_module():
    """Test the STT (Speech-to-Text) module."""
    print("Testing STT Module...")

    try:
        from voice_commander.core.speech.stt import get_stt_instance
        from voice_commander.core.config import load_config

        # Load configuration
        config = load_config()
        print(f"Configuration loaded: {config}")

        # Create STT instance
        stt = get_stt_instance(config=config)
        print("STT instance created successfully")

        # Check if model is loaded
        if stt.is_model_loaded():
            print("✓ Vosk model loaded successfully")
        else:
            print("✗ Vosk model not loaded")
            return False

        # Test audio device detection
        devices = stt.get_audio_devices()
        print(f"Audio devices detected: {len(devices)}")
        if devices:
            for device in devices:
                print(f"  - {device['name']} (index {device['index']})")

        print("✓ STT module test completed successfully")
        return True

    except Exception as e:
        print(f"✗ STT module test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_tts_module():
    """Test the TTS (Text-to-Speech) module."""
    print("\nTesting TTS Module...")

    try:
        from voice_commander.core.speech.tts import get_tts_instance

        # Create TTS instance
        tts = get_tts_instance()
        print("TTS instance created successfully")

        # Test speech functionality
        test_text = "Тестовая речь для проверки модуля синтеза речи"
        print(f"Testing speech: {test_text}")
        tts.speak(test_text)
        print("✓ TTS module test completed successfully")
        return True

    except Exception as e:
        print(f"✗ TTS module test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_integration():
    """Test integration between STT and TTS modules."""
    print("\nTesting Integration...")

    try:
        from voice_commander.core.speech.stt import get_stt_instance
        from voice_commander.core.speech.tts import get_tts_instance

        # Create instances
        stt = get_stt_instance()
        tts = get_tts_instance()

        print("✓ Integration test completed successfully")
        return True

    except Exception as e:
        print(f"✗ Integration test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run all tests."""
    print("Voice Recognition Module Testing")
    print("=" * 40)

    success = True

    # Test individual modules
    success &= test_stt_module()
    success &= test_tts_module()
    success &= test_integration()

    print("\n" + "=" * 40)
    if success:
        print("✓ All tests passed!")
        return 0
    else:
        print("✗ Some tests failed!")
        return 1

if __name__ == "__main__":
    sys.exit(main())