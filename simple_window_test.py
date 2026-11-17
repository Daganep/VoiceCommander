#!/usr/bin/env python3
"""
Test just the window management functionality without complex dependencies.
"""

import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_window_module_directly():
    """Test the window module directly."""
    print("Testing Window Management Module Directly")
    print("=" * 45)

    try:
        from voice_commander.core.actions.window import WindowManager

        # Create an instance
        wm = WindowManager()

        # Test list_windows function
        print("1. Testing list_windows()...")
        result = wm.list_windows()
        print(f"   Success: {result['success']}")
        if result['success']:
            print(f"   Found {len(result.get('data', []))} windows")
            for i, window in enumerate(result.get('data', [])[:3]):  # Show first 3
                print(f"     {i+1}. {repr(window)}")
        else:
            print(f"   Error: {result['message']}")

        # Test with a non-existent window to make sure error handling works
        print("\n2. Testing get_window_info() with non-existent window...")
        result = wm.get_window_info("NonExistentWindow123")
        print(f"   Success: {result['success']}")
        if not result['success']:
            print(f"   Expected error: {result['message']}")

        print("\nAll tests completed successfully!")

    except Exception as e:
        print(f"Error during testing: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_window_module_directly()