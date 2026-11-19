#!/usr/bin/env python3
"""
Test script to verify that config imports work correctly.
"""

import sys
import os

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(__file__))

try:
    # Test importing the config module directly
    from voice_commander.core.config import get_config
    print("✓ Successfully imported config")

    # Test getting a config value
    config = get_config()
    print(f"✓ Config loaded successfully: {config}")

    # Test importing close module
    from voice_commander.core.actions.close import Closer
    print("✓ Successfully imported Closer")

    # Test creating a closer instance
    closer = Closer()
    print("✓ Successfully created Closer instance")

    print("All imports working correctly!")

except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()