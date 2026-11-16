"""
Unified feedback system for Voice Commander.
Handles both speech output and logging.
"""

import sys
import os

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.speech.tts import get_tts_instance
from core.logger import get_logger

logger = get_logger(__name__)

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