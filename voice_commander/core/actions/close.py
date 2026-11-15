"""
Process termination functionality.
"""

import psutil
from ..apps.processes import ProcessManager

class Closer:
    """Close applications and processes."""

    def __init__(self):
        """Initialize the closer."""
        self.process_manager = ProcessManager()

    def close_application(self, app_name=None, confirm=True):
        """
        Close an application by name.

        Args:
            app_name (str): Name of the application to close
            confirm (bool): Whether to ask for confirmation

        Returns:
            dict: Result with success status and message
        """
        try:
            if app_name is None:
                # Close all processes (or implement specific logic)
                return {
                    'success': False,
                    'message': 'Application name required for closing'
                }

            # Try to close the application by name
            closed_processes = self.process_manager.terminate_process_by_name(app_name)

            if closed_processes > 0:
                return {
                    'success': True,
                    'message': f'Closed {closed_processes} process(es) matching: {app_name}'
                }
            else:
                return {
                    'success': False,
                    'message': f'No processes found matching: {app_name}'
                }

        except Exception as e:
            return {
                'success': False,
                'message': f'Error closing application: {str(e)}'
            }