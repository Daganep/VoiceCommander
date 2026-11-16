#!/usr/bin/env python3
"""
Simple demonstration of TTS functionality in Voice Commander.
"""

import sys
import os

# Add the current directory to the Python path so we can import modules
sys.path.insert(0, os.path.dirname(__file__))

from voice_commander.core.speech.tts import TTS

def demo_tts():
    """Demonstrate TTS functionality."""
    print("Voice Commander TTS Demonstration")
    print("=" * 40)

    try:
        # Initialize TTS
        tts = TTS()
        print("✓ TTS module initialized successfully")

        # Test different voice settings
        print("\nTesting voice settings...")

        # Test basic speech
        tts.speak("Привет! Это демонстрация работы синтеза речи в Voice Commander.")
        print("✓ Basic speech test completed")

        # Test different rate
        tts.set_rate(120)
        tts.speak("Эта речь будет говориться медленнее.")
        print("✓ Slow speech test completed")

        # Test different volume
        tts.set_volume(0.5)
        tts.speak("Эта речь будет говориться тише.")
        print("✓ Low volume speech test completed")

        # Reset to normal settings
        tts.set_rate(150)
        tts.set_volume(0.9)

        print("\n🎉 TTS demonstration completed successfully!")
        print("The Voice Commander can now provide vocal feedback for all commands.")

    except Exception as e:
        print(f"✗ Error during TTS demonstration: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    demo_tts()