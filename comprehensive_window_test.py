#!/usr/bin/env python3
"""
Comprehensive test of window management functionality.
"""

import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_comprehensive_window_functions():
    """Test all window management functions."""
    print("Comprehensive Window Management Test")
    print("=" * 40)

    try:
        from voice_commander.core.actions.window import WindowManager

        # Create an instance
        wm = WindowManager()

        # Test all the functions that should be implemented according to the development plan
        functions_to_test = [
            ('list_windows', lambda: wm.list_windows()),
            ('minimize_window', lambda: wm.minimize_window()),  # Without title (active window)
            ('maximize_window', lambda: wm.maximize_window()),  # Without title (active window)
            ('bring_to_front', lambda: wm.bring_to_front()),    # Without title (active window)
        ]

        for func_name, func in functions_to_test:
            print(f"\nTesting {func_name}()...")
            try:
                result = func()
                print(f"   Success: {result['success']}")
                if result['success']:
                    print(f"   Message: {result['message']}")
                else:
                    print(f"   Error: {result['message']}")
            except Exception as e:
                print(f"   Exception: {e}")

        # Test with a specific window title (if any exist)
        print("\nTesting with existing window title...")
        try:
            # Try to get the first available window title
            list_result = wm.list_windows()
            if list_result['success'] and list_result.get('data'):
                window_title = list_result['data'][0]
                print(f"   Using window: {repr(window_title)}")

                # Test functions with specific window
                result = wm.minimize_window(window_title)
                print(f"   Minimize result: Success={result['success']}")

                result = wm.maximize_window(window_title)
                print(f"   Maximize result: Success={result['success']}")

                result = wm.bring_to_front(window_title)
                print(f"   Bring to front result: Success={result['success']}")
            else:
                print("   No windows available for testing with specific title")
        except Exception as e:
            print(f"   Error in specific window test: {e}")

        print("\n" + "=" * 40)
        print("Comprehensive test completed!")

    except Exception as e:
        print(f"Error during comprehensive testing: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_comprehensive_window_functions()