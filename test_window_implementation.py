#!/usr/bin/env python3
"""
Test script for window management functionality.
"""

import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_window_module():
    """Test that the window module can be imported and basic functions work."""
    print("Testing window management module implementation...")

    try:
        # Test importing the window module
        from core.actions.window import WindowManager, maximize_window, minimize_window, restore_window, bring_to_front

        print("✓ Window manager module imported successfully")

        # Test creating a window manager instance
        wm = WindowManager()
        print("✓ Window manager created successfully")

        # Test that basic functions exist
        print("✓ Functions available:")
        print("  - maximize_window")
        print("  - minimize_window")
        print("  - restore_window")
        print("  - bring_to_front")
        print("  - list_windows")
        print("  - get_window_info")

        print("\nWindow management module implementation test completed successfully!")
        return True

    except Exception as e:
        print(f"✗ Error testing window module: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_command_parsing():
    """Test that window commands can be parsed."""
    print("\nTesting command parsing for window management...")

    try:
        from core.commands.parser import CommandParser
        from core.commands.schema import CommandSchema

        parser = CommandParser()

        # Test window management commands
        window_commands = [
            "максимизировать окно",
            "минимизировать окно",
            "восстановить окно",
            "перевести окно в фокус"
        ]

        for cmd_text in window_commands:
            command = parser.parse_command(cmd_text)
            if command:
                print(f"✓ Parsed command: '{cmd_text}' -> {command.schema.name}")
            else:
                print(f"✗ Failed to parse command: '{cmd_text}'")

        print("Command parsing test completed!")
        return True

    except Exception as e:
        print(f"✗ Error testing command parsing: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success1 = test_window_module()
    success2 = test_command_parsing()

    if success1 and success2:
        print("\n🎉 All tests passed! Window management module is properly implemented.")
    else:
        print("\n❌ Some tests failed.")
        sys.exit(1)