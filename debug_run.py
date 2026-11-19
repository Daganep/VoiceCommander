#!/usr/bin/env python3
"""
Debug script to reproduce the exact import error from the logs.
"""

import sys
import os

# Add current directory to Python path like the main script does
sys.path.insert(0, os.path.dirname(__file__))

try:
    print("Attempting to run voice commander modules...")

    # This is what happens in main.py
    from core.speech.stt import get_stt_instance
    from core.speech.tts import get_tts_instance
    from core.commands.parser import CommandParser
    from core.feedback import Feedback
    from core.logger import setup_logger
    from core.error_handler import ErrorHandler

    print("SUCCESS: Core modules imported successfully")

    # Try to import the config that's failing
    from voice_commander.core.config import get_config
    print("SUCCESS: Config module imported successfully")

    # Try importing close.py which has the relative import
    from voice_commander.core.actions.close import Closer
    print("SUCCESS: Closer module imported successfully")

    # Now test creating the command parser and executing a command
    parser = CommandParser()
    feedback = Feedback()

    print("Testing close command parsing...")

    # Try to execute the specific command that was failing
    result = parser.parse_command('закрыть приложение notepad.exe', feedback)
    print(f"Result: {result}")

except Exception as e:
    print(f"Error occurred: {e}")
    import traceback
    traceback.print_exc()