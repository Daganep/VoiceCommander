# This file will be used to verify the fix for the close application command issue.

import sys
import os

def test_imports():
    """Test that all necessary imports work correctly."""

    # Add current directory to path
    sys.path.insert(0, os.path.dirname(__file__))

    try:
        # Test the exact imports that were mentioned in the error
        from voice_commander.core.config import get_config
        print("SUCCESS: Config module imported successfully")

        # Test the close functionality
        from voice_commander.core.actions.close import Closer
        print("SUCCESS: Close module imported successfully")

        # Test direct function call
        closer = Closer()
        result = closer.close_application('notepad.exe')
        print(f"SUCCESS: Close function works: {result}")

        print("All imports and functionality working correctly!")
        return True

    except Exception as e:
        print(f"ERROR in import test: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_imports()