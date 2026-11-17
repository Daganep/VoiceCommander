#!/usr/bin/env python3
"""
Test script for confirmation functionality.
"""

import sys
import os

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(__file__))

from voice_commander.core.config import get_config
from voice_commander.core.actions.close import Closer

def test_confirmation_config():
    """Test that configuration is loaded correctly."""
    print("Testing configuration loading...")

    confirmations = get_config('confirmations', True)
    print(f"Confirmations enabled: {confirmations}")

    # Test with default value
    non_existent = get_config('non_existent_key', 'default_value')
    print(f"Non-existent key with default: {non_existent}")

def test_closer_with_confirmation():
    """Test the closer with confirmation settings."""
    print("\nTesting Closer with confirmation...")

    closer = Closer()

    # Test that it handles missing app name
    result = closer.close_application(None)
    print(f"Close with None: {result}")

    # Test with a non-existent application
    result = closer.close_application('nonexistent_app')
    print(f"Close nonexistent app: {result}")

if __name__ == "__main__":
    test_confirmation_config()
    test_closer_with_confirmation()
    print("\nConfirmation functionality tests completed.")