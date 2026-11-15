"""
Process management with psutil.
"""

import psutil

class ProcessManager:
    """Manage processes using psutil."""

    def __init__(self):
        """Initialize the process manager."""
        pass

    def get_all_processes(self):
        """
        Get list of all running processes.

        Returns:
            list: List of process information dictionaries
        """
        processes = []
        for proc in psutil.process_iter(['pid', 'name', 'username']):
            try:
                processes.append(proc.info)
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass
        return processes

    def terminate_process_by_name(self, name):
        """
        Terminate all processes with a given name.

        Args:
            name (str): Name of the process to terminate

        Returns:
            int: Number of processes terminated
        """
        terminated_count = 0
        for proc in psutil.process_iter(['pid', 'name']):
            try:
                if name.lower() in proc.info['name'].lower():
                    proc.terminate()
                    proc.wait(timeout=5)  # Wait up to 5 seconds for graceful termination
                    terminated_count += 1
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass
        return terminated_count

    def kill_process_by_name(self, name):
        """
        Kill all processes with a given name.

        Args:
            name (str): Name of the process to kill

        Returns:
            int: Number of processes killed
        """
        killed_count = 0
        for proc in psutil.process_iter(['pid', 'name']):
            try:
                if name.lower() in proc.info['name'].lower():
                    proc.kill()
                    killed_count += 1
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass
        return killed_count

    def is_process_running(self, name):
        """
        Check if a process with given name is running.

        Args:
            name (str): Name of the process to check

        Returns:
            bool: True if process is running, False otherwise
        """
        for proc in psutil.process_iter(['name']):
            try:
                if name.lower() in proc.info['name'].lower():
                    return True
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass
        return False