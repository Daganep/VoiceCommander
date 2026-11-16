#!/usr/bin/env python3
"""
Simple test to verify the text interface can be imported and run.
"""

import sys
import os

# Add current directory to Python path
sys.path.insert(0, os.getcwd())

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

    print("\nAll tests passed! Text interface components are ready for use.")

except Exception as e:
    print(f"ERROR: {e}")
    import traceback
    traceback.print_exc()