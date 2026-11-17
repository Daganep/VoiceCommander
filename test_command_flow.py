#!/usr/bin/env python3
"""
Test script for end-to-end command execution with confirmation.
"""

import sys
import os

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(__file__))

from voice_commander.core.commands.parser import CommandParser
from voice_commander.core.feedback import Feedback
from voice_commander.core.speech.tts import get_tts_instance

def test_command_execution():
    """Test command execution with confirmation settings."""
    print("Testing command execution flow...")

    # Initialize components
    parser = CommandParser()

    # Create a simple feedback system (without TTS for this test)
    feedback = Feedback()

    # Test parsing commands
    commands_to_test = [
        "Закрой приложение notepad",
        "Запусти блокнот"
    ]

    for command in commands_to_test:
        print(f"\nTesting command: '{command}'")
        try:
            result = parser.parse_command(command, feedback)
            print(f"Result: {result}")
        except Exception as e:
            print(f"Error executing command: {e}")

if __name__ == "__main__":
    test_command_execution()
    print("\nCommand execution tests completed.")