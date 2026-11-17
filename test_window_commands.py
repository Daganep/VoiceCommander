#!/usr/bin/env python3
"""
Simple test for window management commands.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from voice_commander.core.commands.parser import CommandParser
from voice_commander.core.feedback import Feedback

def test_window_commands():
    """Test window management commands directly."""
    print("Testing Window Management Commands")
    print("=" * 40)

    # Initialize parser and feedback
    parser = CommandParser()
    feedback = Feedback()

    # Test some window commands
    test_commands = [
        "сверни окно",
        "разверни окно",
        "переведи окно в фокус"
    ]

    for command in test_commands:
        print(f"\nTesting: '{command}'")
        try:
            result = parser.parse_command(command, feedback)
            print(f"  Result: {result['success']}")
            print(f"  Message: {result['message']}")
        except Exception as e:
            print(f"  Error: {e}")

if __name__ == "__main__":
    test_window_commands()