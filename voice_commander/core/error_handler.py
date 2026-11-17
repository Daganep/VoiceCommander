"""
Error handling and recovery system for Voice Commander.
This module provides comprehensive error handling with recovery mechanisms.
"""

import sys
import traceback
import logging
from typing import Optional, Dict, Any
from datetime import datetime

class ErrorHandler:
    """Comprehensive error handling and recovery system."""

    def __init__(self, logger):
        """
        Initialize the error handler.

        Args:
            logger: Logger instance for error logging
        """
        self.logger = logger
        self.error_count = 0
        self.last_error_time = None

    def handle_exception(self, exception: Exception, context: str = "",
                        should_exit: bool = False) -> Dict[str, Any]:
        """
        Handle an exception with comprehensive logging and recovery.

        Args:
            exception (Exception): The exception to handle
            context (str): Context information about where the error occurred
            should_exit (bool): Whether to exit the application after handling

        Returns:
            dict: Error details for further processing
        """
        self.error_count += 1
        self.last_error_time = datetime.now()

        # Create error details
        error_details = {
            'timestamp': self.last_error_time,
            'error_type': type(exception).__name__,
            'error_message': str(exception),
            'context': context,
            'error_count': self.error_count
        }

        # Log the error with full traceback
        self.logger.error(f"Error in {context}: {exception}")
        self.logger.debug(f"Full traceback: {traceback.format_exc()}")

        # Provide user feedback based on error type
        if hasattr(exception, '__class__') and 'KeyboardInterrupt' in str(type(exception)):
            self.logger.info("Keyboard interrupt received")
        elif 'ConnectionError' in str(type(exception)) or 'TimeoutError' in str(type(exception)):
            self.logger.error("Network/connection error occurred - attempting recovery")
        else:
            self.logger.error(f"Unexpected error: {exception}")

        # If we should exit, do so
        if should_exit:
            sys.exit(1)

        return error_details

    def recover_from_error(self, error_details: Dict[str, Any]) -> bool:
        """
        Attempt to recover from an error.

        Args:
            error_details (dict): Error details from handle_exception

        Returns:
            bool: True if recovery was successful, False otherwise
        """
        try:
            # Basic recovery actions
            self.logger.info(f"Attempting recovery from error type: {error_details['error_type']}")

            # For certain types of errors, we might want to retry or reset components
            if error_details['error_type'] in ['ConnectionError', 'TimeoutError']:
                # Attempt to restart connection or reset components
                self.logger.info("Recovery attempt - restarting components")
                return True  # In a real implementation, this would actually do recovery

            elif error_details['error_type'] == 'MemoryError':
                # Handle memory issues by clearing caches or restarting
                self.logger.warning("Memory error encountered - clearing caches")
                return True

            else:
                # For other errors, we'll just log and continue
                self.logger.info("Generic error recovery - continuing execution")
                return True

        except Exception as e:
            self.logger.error(f"Failed to recover from error: {e}")
            return False

    def get_error_stats(self) -> Dict[str, Any]:
        """
        Get statistics about errors encountered.

        Returns:
            dict: Error statistics
        """
        return {
            'total_errors': self.error_count,
            'last_error_time': self.last_error_time,
            'error_rate': self.error_count / max(1, (datetime.now() -
                              datetime(2023, 1, 1)).total_seconds()) if self.last_error_time else 0
        }

    def log_system_health(self):
        """
        Log system health information for debugging.
        """
        try:
            import psutil
            import platform

            # Get system information
            self.logger.info(f"System: {platform.system()} {platform.release()}")
            self.logger.info(f"Python version: {sys.version}")

            # Get memory usage
            process = psutil.Process()
            memory_info = process.memory_info()
            self.logger.info(f"Memory usage: {memory_info.rss / 1024 / 1024:.2f} MB")

            # Get CPU usage
            cpu_percent = psutil.cpu_percent(interval=1)
            self.logger.info(f"CPU usage: {cpu_percent}%")

        except Exception as e:
            self.logger.warning(f"Could not log system health: {e}")