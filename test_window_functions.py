#!/usr/bin/env python3
"""
Test script for window management functions.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from voice_commander.core.actions.window import WindowManager
from voice_commander.core.feedback import Feedback

def test_window_functions():
    """Test the window management functions."""
    print("Testing Window Management Functions")
    print("=" * 40)

    # Initialize the window manager
    wm = WindowManager()

    # Test listing windows (this should work without errors)
    print("1. Testing list_windows()...")
    try:
        result = wm.list_windows()
        print(f"   Result: {result['success']}")
        if result['success']:
            print(f"   Found {len(result.get('data', []))} windows")
            for i, window in enumerate(result.get('data', [])[:5]):  # Show first 5
                print(f"     {i+1}. {window}")
        else:
            print(f"   Error: {result['message']}")
    except Exception as e:
        print(f"   Exception: {e}")

    # Test window info for a non-existent window (should fail gracefully)
    print("\n2. Testing get_window_info() with non-existent window...")
    try:
        result = wm.get_window_info("NonExistentWindow123")
        print(f"   Result: {result['success']}")
        if not result['success']:
            print(f"   Expected error: {result['message']}")
    except Exception as e:
        print(f"   Exception: {e}")

    # Test window info for a potentially existing window (if any)
    print("\n3. Testing get_window_info() with existing window...")
    try:
        # Try to get info about the current window
        result = wm.get_window_info("Windows PowerShell")
        if result['success']:
            print(f"   Success: {result['message']}")
            print(f"   Window data: {result['data']}")
        else:
            print(f"   Error (expected): {result['message']}")
    except Exception as e:
        print(f"   Exception: {e}")

if __name__ == "__main__":
    test_window_functions()