#!/usr/bin/env python3
"""
Test script for window management functionality.
"""

import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from voice_commander.core.actions.window import WindowManager

def test_window_functions():
    """Test the window management functions."""
    print("Testing window management functionality...")

    # Create a window manager instance
    wm = WindowManager()

    # Test that we can create the object (basic check)
    print("✓ Window manager created successfully")

    # Test listing windows - this should not crash
    try:
        result = wm.list_windows()
        print(f"✓ List windows functionality works: {result['message']}")
    except Exception as e:
        print(f"✗ Error in list_windows: {e}")

    # Test get window info with a dummy title (should fail gracefully)
    try:
        result = wm.get_window_info("NonExistentWindow")
        print(f"✓ Get window info handled gracefully: {result['message']}")
    except Exception as e:
        print(f"✗ Error in get_window_info: {e}")

    print("Window management tests completed.")

if __name__ == "__main__":
    test_window_functions()