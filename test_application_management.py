#!/usr/bin/env python3
"""
Test script for Application Management Module Development.
This tests the launch and close functionality.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from voice_commander.core.actions.launch import Launcher
from voice_commander.core.actions.close import Closer
from voice_commander.core.apps.registry import AppRegistry
from voice_commander.core.apps.processes import ProcessManager

def test_launcher():
    """Test the launcher functionality."""
    print("Testing Launcher...")

    launcher = Launcher()

    # Test with an alias (should work)
    result = launcher.launch_application('notepad')
    print(f"Launch notepad: {result}")

    # Test with a system command
    result = launcher.launch_application('cmd')
    print(f"Launch cmd: {result}")

    # Test with non-existent application
    result = launcher.launch_application('nonexistentapp.exe')
    print(f"Launch nonexistent app: {result}")

def test_closer():
    """Test the closer functionality."""
    print("\nTesting Closer...")

    closer = Closer()

    # Test closing a non-existent process
    result = closer.close_application('nonexistentprocess')
    print(f"Close nonexistent process: {result}")

    # Test closing with None (should fail)
    result = closer.close_application(None)
    print(f"Close with None: {result}")

def test_registry():
    """Test the application registry."""
    print("\nTesting AppRegistry...")

    registry = AppRegistry()

    # Test getting existing aliases
    path = registry.get_path('notepad')
    print(f"Notepad alias path: {path}")

    # Test adding a new alias
    registry.add_alias('testapp', 'C:\\Windows\\System32\\cmd.exe')
    path = registry.get_path('testapp')
    print(f"Testapp alias path: {path}")

    # Test removing an alias
    registry.remove_alias('testapp')
    path = registry.get_path('testapp')
    print(f"After removal testapp path: {path}")

def test_process_manager():
    """Test the process manager functionality."""
    print("\nTesting ProcessManager...")

    pm = ProcessManager()

    # Test getting all processes (should work)
    processes = pm.get_all_processes()
    print(f"Found {len(processes)} processes")

    # Test checking if a process is running
    is_running = pm.is_process_running('notepad.exe')
    print(f"Notepad running: {is_running}")

    # Test terminating a non-existent process (should not crash)
    terminated = pm.terminate_process_by_name('nonexistentprocess')
    print(f"Terminated nonexistent processes: {terminated}")

if __name__ == "__main__":
    test_launcher()
    test_closer()
    test_registry()
    test_process_manager()
    print("\nAll tests completed.")