"""
Unified feedback system for Voice Commander.
Handles both speech output and logging.
"""

import sys
import os
import logging

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.speech.tts import get_tts_instance
from core.logger import get_logger

logger = get_logger(__name__)

class Feedback:
    """Unified feedback system for Voice Commander that handles both speech output and logging."""

    def __init__(self):
        """Initialize the feedback system."""
        self._tts = None

    def set_tts(self, tts_instance):
        """Set the TTS instance to use for speech output."""
        self._tts = tts_instance

    def speak_and_log(self, message: str, level: int = logging.INFO):
        """
        Provide unified feedback by speaking the message and logging it.

        Args:
            message (str): Message to provide feedback for
            level (int): Logging level (default: INFO)
        """
        try:
            # Speak the message using TTS
            if self._tts is None:
                tts = get_tts_instance()
            else:
                tts = self._tts
            tts.speak(message)

            # Log the message
            logger.log(level, message)

        except Exception as e:
            # If there's an error with either speech or logging, log it
            logger.error(f"Failed to provide feedback for '{message}': {e}")

    def speak_async_and_log(self, message: str, level: int = logging.INFO):
        """
        Provide asynchronous feedback by speaking the message and logging it.

        Args:
            message (str): Message to provide feedback for
            level (int): Logging level (default: INFO)
        """
        try:
            # Speak the message asynchronously using TTS
            if self._tts is None:
                tts = get_tts_instance()
            else:
                tts = self._tts
            tts.speak_async(message)

            # Log the message
            logger.log(level, message)

        except Exception as e:
            # If there's an error with either speech or logging, log it
            logger.error(f"Failed to provide async feedback for '{message}': {e}")

    def log_only(self, message: str, level: int = logging.INFO):
        """
        Log a message without speaking.

        Args:
            message (str): Message to log
            level (int): Logging level (default: INFO)
        """
        logger.log(level, message)

# For backward compatibility with direct function calls
def speak_and_log(message: str, level: int = logging.INFO):
    """
    Provide unified feedback by speaking the message and logging it.

    Args:
        message (str): Message to provide feedback for
        level (int): Logging level (default: INFO)
    """
    try:
        # Speak the message using TTS
        tts = get_tts_instance()
        tts.speak(message)

        # Log the message
        logger.log(level, message)

    except Exception as e:
        # If there's an error with either speech or logging, log it
        logger.error(f"Failed to provide feedback for '{message}': {e}")

def speak_async_and_log(message: str, level: int = logging.INFO):
    """
    Provide asynchronous feedback by speaking the message and logging it.

    Args:
        message (str): Message to provide feedback for
        level (int): Logging level (default: INFO)
    """
    try:
        # Speak the message asynchronously using TTS
        tts = get_tts_instance()
        tts.speak_async(message)

        # Log the message
        logger.log(level, message)

    except Exception as e:
        # If there's an error with either speech or logging, log it
        logger.error(f"Failed to provide async feedback for '{message}': {e}")

def log_only(message: str, level: int = logging.INFO):
    """
    Log a message without speaking.

    Args:
        message (str): Message to log
        level (int): Logging level (default: INFO)
    """
    logger.log(level, message)