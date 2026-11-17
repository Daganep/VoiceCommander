"""
Logging setup for Voice Commander with rotation.
"""

import logging
import os
from logging.handlers import RotatingFileHandler
from pathlib import Path

def setup_logger(log_file='logs/voice_commander.log', max_bytes=10*1024*1024, backup_count=5):
    """
    Set up the logger with rotation.

    Args:
        log_file (str): Path to the log file
        max_bytes (int): Maximum size of log file before rotation
        backup_count (int): Number of backup files to keep

    Returns:
        logging.Logger: Configured logger instance
    """
    # Create logs directory if it doesn't exist
    Path(log_file).parent.mkdir(parents=True, exist_ok=True)

    # Create logger
    logger = logging.getLogger('voice_commander')
    logger.setLevel(logging.DEBUG)

    # Prevent adding multiple handlers if function is called multiple times
    if not logger.handlers:
        # Create file handler with rotation
        file_handler = RotatingFileHandler(
            log_file,
            maxBytes=max_bytes,
            backupCount=backup_count,
            encoding='utf-8'
        )

        # Create console handler
        console_handler = logging.StreamHandler()

        # Create formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )

        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)

        # Add handlers to logger
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

    return logger

def get_logger(name):
    """
    Get a named logger instance.

    Args:
        name (str): Name of the logger

    Returns:
        logging.Logger: Logger instance
    """
    return logging.getLogger(name)