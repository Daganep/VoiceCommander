#!/usr/bin/env python3
"""
Test script for UI click functionality.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'voice_commander'))

from core.actions.ui_click import UIClicker

def test_ui_click():
    """Test the UI click functionality."""
    print("Testing UI click functionality...")

    # Create a UI clicker instance
    clicker = UIClicker()

    # Test with a non-existent element (should fail gracefully)
    result = clicker.click_element("NonExistentButton")
    print(f"Result for non-existent button: {result}")

    # Test with a simple text input
    result = clicker.click_element("OK")
    print(f"Result for 'OK' button: {result}")

if __name__ == "__main__":
    test_ui_click()