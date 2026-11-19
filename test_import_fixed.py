#!/usr/bin/env python3

import sys
import os

# Run the test from within the project directory, but make sure we can import
try:
    # Test 1: Direct module import (this should work)
    from voice_commander.core.config import get_config
    print("SUCCESS: Direct import of config works")
    result = get_config('confirmations', True)
    print(f"SUCCESS: Config value retrieved: {result}")

    # Test 2: Import the Closer class
    from voice_commander.core.actions.close import Closer
    print("SUCCESS: Closer imported successfully")

    # Test 3: Run the close function directly to make sure it works
    closer = Closer()
    result = closer.close_application('notepad.exe')
    print(f"SUCCESS: Close function executed: {result}")

except Exception as e:
    print(f"ERROR: {e}")
    import traceback
    traceback.print_exc()