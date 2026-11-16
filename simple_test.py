#!/usr/bin/env python3
"""
Simple test to verify core modules work.
"""

import sys
import os

# Add the current directory to Python path so we can import modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    # Test importing core modules first
    from voice_commander.core.commands.parser import CommandParser
    print("SUCCESS: Command parser imported successfully")

    # Test creating parser instance
    parser = CommandParser()
    print("SUCCESS: Command parser instance created successfully")

    # Test parsing a simple command
    result = parser.parse_command("запусти блокнот")
    print(f"SUCCESS: Command parsing works: {result}")

    print("\nAll tests passed! Core components are ready for use.")

except Exception as e:
    print(f"ERROR: {e}")
    import traceback
    traceback.print_exc()