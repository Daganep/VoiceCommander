"""
Process management for Voice Commander.
Handles application process operations like termination.
"""

import psutil
import os
import time
from typing import List, Optional
from core.logger import get_logger

logger = get_logger(__name__)


class ProcessManager:
    """Manages application processes."""

    def __init__(self):
        """Initialize the process manager."""
        logger.info("Process manager initialized")

    def get_running_processes(self) -> List[dict]:
        """
        Get list of all currently running processes.

        Returns:
            List[dict]: List of process information dictionaries
        """
        processes = []
        try:
            for proc in psutil.process_iter(['pid', 'name', 'exe']):
                try:
                    # Get process info
                    info = proc.info
                    if info['name'] and not info['name'].startswith('<'):
                        processes.append({
                            'pid': info['pid'],
                            'name': info['name'],
                            'exe': info['exe']
                        })
                except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                    # Process might have terminated or we don't have access
                    continue
        except Exception as e:
            logger.error(f"Error getting running processes: {e}")

        return processes

    def find_process_by_name(self, name: str) -> List[dict]:
        """
        Find processes by name (case-insensitive).

        Args:
            name (str): Name to search for

        Returns:
            List[dict]: List of matching process dictionaries
        """
        matching_processes = []
        try:
            # Normalize the search name
            search_name = name.lower()

            for proc in psutil.process_iter(['pid', 'name', 'exe']):
                try:
                    info = proc.info
                    if info['name'] and not info['name'].startswith('<'):
                        # Check if process name matches (case insensitive)
                        if search_name in info['name'].lower():
                            matching_processes.append({
                                'pid': info['pid'],
                                'name': info['name'],
                                'exe': info['exe']
                            })
                except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                    continue
        except Exception as e:
            logger.error(f"Error finding processes by name '{name}': {e}")

        return matching_processes

    def terminate_process(self, pid: int) -> bool:
        """
        Terminate a process by PID.

        Args:
            pid (int): Process ID to terminate

        Returns:
            bool: True if termination was successful, False otherwise
        """
        try:
            process = psutil.Process(pid)
            process.terminate()

            # Wait for process to terminate gracefully
            try:
                process.wait(timeout=5)
                logger.info(f"Process {pid} terminated successfully")
                return True
            except psutil.TimeoutExpired:
                # Force kill if it doesn't terminate gracefully
                process.kill()
                process.wait()
                logger.info(f"Process {pid} force killed")
                return True

        except (psutil.NoSuchProcess, psutil.AccessDenied) as e:
            logger.error(f"Failed to terminate process {pid}: {e}")
            return False
        except Exception as e:
            logger.error(f"Unexpected error terminating process {pid}: {e}")
            return False

    def terminate_process_by_name(self, name: str) -> int:
        """
        Terminate all processes matching a name.

        Args:
            name (str): Name of the process to terminate

        Returns:
            int: Number of processes terminated
        """
        try:
            processes = self.find_process_by_name(name)
            terminated_count = 0

            for proc in processes:
                if self.terminate_process(proc['pid']):
                    terminated_count += 1

            logger.info(f"Terminated {terminated_count} process(es) matching '{name}'")
            return terminated_count

        except Exception as e:
            logger.error(f"Error terminating processes by name '{name}': {e}")
            return 0

    def is_process_running(self, pid: int) -> bool:
        """
        Check if a process with given PID is running.

        Args:
            pid (int): Process ID to check

        Returns:
            bool: True if process is running, False otherwise
        """
        try:
            process = psutil.Process(pid)
            return process.is_running()
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            return False

    def get_process_info(self, pid: int) -> Optional[dict]:
        """
        Get detailed information about a specific process.

        Args:
            pid (int): Process ID to get info for

        Returns:
            Optional[dict]: Process information or None if not found
        """
        try:
            process = psutil.Process(pid)
            return {
                'pid': process.pid,
                'name': process.name(),
                'exe': process.exe(),
                'status': process.status(),
                'create_time': process.create_time(),
                'memory_info': process.memory_info(),
                'cpu_percent': process.cpu_percent()
            }
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            return None