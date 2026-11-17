"""
Error handling system for Voice Commander.
Provides centralized error handling and recovery mechanisms.
"""

import logging
import traceback
from typing import Dict, Any

logger = logging.getLogger(__name__)

class ErrorHandler:
    """Centralized error handling for Voice Commander."""

    def __init__(self, logger_instance: logging.Logger):
        """
        Initialize the error handler.

        Args:
            logger_instance (logging.Logger): Logger instance to use for error logging
        """
        self.logger = logger_instance

    def handle_exception(self, exception: Exception, context: str, should_exit: bool = False) -> Dict[str, Any]:
        """
        Handle an exception by logging it and optionally exiting.

        Args:
            exception (Exception): The exception that occurred
            context (str): Context where the error occurred
            should_exit (bool): Whether to exit after handling the error

        Returns:
            Dict[str, Any]: Error details dictionary
        """
        error_details = {
            'exception': exception,
            'context': context,
            'traceback': traceback.format_exc()
        }

        self.logger.error(f"Error in {context}: {exception}")
        self.logger.debug(f"Full traceback: {error_details['traceback']}")

        if should_exit:
            self.logger.critical("Exiting due to critical error")
            return error_details

        return error_details

    def recover_from_error(self, error_details: Dict[str, Any]) -> None:
        """
        Attempt to recover from an error.

        Args:
            error_details (Dict[str, Any]): Error details dictionary
        """
        self.logger.info("Attempting to recover from error...")
        # In a real implementation, this might restart components or reset state
        # For now, just log that recovery was attempted
        pass

    def log_error(self, message: str, exception: Exception = None) -> None:
        """
        Log an error with optional exception details.

        Args:
            message (str): Error message to log
            exception (Exception, optional): Exception that occurred
        """
        if exception:
            self.logger.error(f"{message}: {exception}")
            self.logger.debug(f"Full traceback: {traceback.format_exc()}")
        else:
            self.logger.error(message)