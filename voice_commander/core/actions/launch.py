"""
Application launching functionality.
"""

import subprocess
import os
from ..apps.registry import AppRegistry

class Launcher:
    """Launch applications with alias support."""

    def __init__(self):
        """Initialize the launcher."""
        self.registry = AppRegistry()

    def launch_application(self, app_name):
        """
        Launch an application by name.

        Args:
            app_name (str): Name of the application to launch

        Returns:
            dict: Result with success status and message
        """
        try:
            # Check if it's an alias first
            if app_name in self.registry.aliases:
                app_path = self.registry.aliases[app_name]
            else:
                app_path = app_name

            # Try to launch the application
            if os.path.exists(app_path):
                subprocess.Popen([app_path])
                return {
                    'success': True,
                    'message': f'Launched application: {app_name}'
                }
            else:
                # Try to find the application in PATH or common locations
                try:
                    subprocess.Popen([app_name])
                    return {
                        'success': True,
                        'message': f'Launched application: {app_name}'
                    }
                except Exception as e:
                    return {
                        'success': False,
                        'message': f'Failed to launch {app_name}: {str(e)}'
                    }

        except Exception as e:
            return {
                'success': False,
                'message': f'Error launching application: {str(e)}'
            }