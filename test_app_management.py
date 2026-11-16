#!/usr/bin/env python3
"""
Test script for application management module.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '.'))

from voice_commander.core.actions.launch import Launcher
from voice_commander.core.actions.close import Closer
from voice_commander.core.apps.registry import AppRegistry
from voice_commander.core.apps.processes import ProcessManager

def test_launcher():
    """Test the launcher functionality."""
    print("Testing Launcher...")

    launcher = Launcher()

    # Test with a known alias
    result = launcher.launch_application('notepad')
    print(f"Launch notepad: {result}")

    # Test with a direct path
    result = launcher.launch_application('calc.exe')
    print(f"Launch calculator: {result}")

def test_closer():
    """Test the closer functionality."""
    print("\nTesting Closer...")

    closer = Closer()

    # Test closing an application that's not running
    result = closer.close_application('nonexistent_app')
    print(f"Close nonexistent app: {result}")

    # Test closing a known application (should fail since it's not running)
    result = closer.close_application('notepad')
    print(f"Close notepad: {result}")

def test_registry():
    """Test the application registry."""
    print("\nTesting AppRegistry...")

    registry = AppRegistry()

    # Test getting an alias
    path = registry.get_path('notepad')
    print(f"Notepad alias path: {path}")

    # Test adding a new alias
    registry.add_alias('test_app', 'C:\\Windows\\System32\\cmd.exe')
    path = registry.get_path('test_app')
    print(f"Test app alias path: {path}")

    # Test removing an alias
    registry.remove_alias('test_app')
    path = registry.get_path('test_app')
    print(f"After removal - test app alias path: {path}")

def test_process_manager():
    """Test the process manager."""
    print("\nTesting ProcessManager...")

    pm = ProcessManager()

    # Test checking if a process is running
    is_running = pm.is_process_running('notepad.exe')
    print(f"Is notepad running: {is_running}")

    # Test getting all processes
    processes = pm.get_all_processes()
    print(f"Found {len(processes)} processes")

    # Test terminating a process (should be safe even if not found)
    terminated = pm.terminate_process_by_name('nonexistent_app')
    print(f"Terminated nonexistent app: {terminated}")

if __name__ == "__main__":
    test_registry()
    test_launcher()
    test_closer()
    test_process_manager()