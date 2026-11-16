#!/usr/bin/env python3
"""
Test script for STT module integration with configuration.
"""

import sys
import os

# Add the current directory to the Python path so we can import modules
sys.path.insert(0, os.path.dirname(__file__))

from voice_commander.core.speech.stt import STT
import yaml

def test_stt_with_config():
    """Test STT module with configuration."""
    print("Testing STT module with configuration...")

    # Load config
    try:
        with open('config.yaml', 'r') as f:
            config = yaml.safe_load(f)
        print("✓ Configuration loaded successfully")
        print(f"Configuration: {config}")
    except Exception as e:
        print(f"Warning: Could not load config.yaml: {e}")
        config = None

    # Create STT instance with config
    try:
        stt = STT(model_path="models", config=config)
        print("✓ STT object created successfully")

        # Test model loading
        if stt.load_model():
            print("✓ Vosk model loaded successfully")

            # Test configuration values
            if config:
                print(f"Push-to-talk key: {stt.push_to_talk_key}")
                print(f"Wake-word enabled: {stt.wake_word_enabled}")
                print(f"Wake-word: {stt.wake_word}")
            else:
                print("No configuration provided, using defaults")

            return True
        else:
            print("✗ Failed to load Vosk model")
            return False

    except Exception as e:
        print(f"✗ STT initialization failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Main test function."""
    print("Running STT integration tests...")
    print("=" * 40)

    success = test_stt_with_config()

    if success:
        print("\n✓ All integration tests passed!")
    else:
        print("\n✗ Some integration tests failed!")
        sys.exit(1)

if __name__ == "__main__":
    main()