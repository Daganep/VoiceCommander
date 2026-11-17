#!/usr/bin/env python3
"""
Debug script for window management functions.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import pywinauto
from pywinauto import Application

def debug_window_list():
    """Debug what find_elements returns."""
    print("Debugging pywinauto find_elements")
    print("=" * 40)

    try:
        # Try to find windows
        windows = pywinauto.findwindows.find_elements(visible_only=True)
        print(f"Found {len(windows)} visible windows")

        for i, window in enumerate(windows[:5]):  # Show first 5
            print(f"Window {i+1}:")
            print(f"  Type: {type(window)}")
            print(f"  Attributes: {[attr for attr in dir(window) if not attr.startswith('_')]}")
            print(f"  Has text: {hasattr(window, 'text')}")
            if hasattr(window, 'text'):
                print(f"  Text value: {repr(window.text)}")
            print()

    except Exception as e:
        print(f"Error in debug: {e}")
        import traceback
        traceback.print_exc()

def test_simple_window_operations():
    """Test simple window operations."""
    print("Testing simple window operations")
    print("=" * 40)

    try:
        # Try connecting to a known application like Notepad if it's running
        app = Application(backend="uia").connect(title="Notepad")
        print("Successfully connected to Notepad")

        window = app.window(title="Notepad")
        print(f"Window title: {window.text}")
        print(f"Window object: {window}")

    except Exception as e:
        print(f"Could not connect to Notepad: {e}")

if __name__ == "__main__":
    debug_window_list()
    print()
    test_simple_window_operations()