"""
Unified feedback system for voice commander.
"""

from .logger import setup_logger

class Feedback:
    """Unified output system that handles both speech and logging."""

    def __init__(self):
        """Initialize the feedback system."""
        self.logger = setup_logger()
        self.tts = None  # Will be initialized when needed

    def set_tts(self, tts_engine):
        """
        Set the TTS engine for speech output.

        Args:
            tts_engine: TTS engine instance
        """
        self.tts = tts_engine

    def speak_and_log(self, message, level="INFO"):
        """
        Speak a message and log it.

        Args:
            message (str): Message to speak and log
            level (str): Log level
        """
        # Speak the message
        if self.tts:
            self.tts.speak(message)

        # Log the message
        if level == "DEBUG":
            self.logger.debug(message)
        elif level == "INFO":
            self.logger.info(message)
        elif level == "WARNING":
            self.logger.warning(message)
        elif level == "ERROR":
            self.logger.error(message)
        else:
            self.logger.info(message)

    def speak(self, message):
        """
        Speak a message.

        Args:
            message (str): Message to speak
        """
        if self.tts:
            self.tts.speak(message)

    def log(self, message, level="INFO"):
        """
        Log a message.

        Args:
            message (str): Message to log
            level (str): Log level
        """
        if level == "DEBUG":
            self.logger.debug(message)
        elif level == "INFO":
            self.logger.info(message)
        elif level == "WARNING":
            self.logger.warning(message)
        elif level == "ERROR":
            self.logger.error(message)
        else:
            self.logger.info(message)

    def info(self, message):
        """
        Log an info message.

        Args:
            message (str): Message to log
        """
        self.logger.info(message)

    def warning(self, message):
        """
        Log a warning message.

        Args:
            message (str): Message to log
        """
        self.logger.warning(message)

    def error(self, message):
        """
        Log an error message.

        Args:
            message (str): Message to log
        """
        self.logger.error(message)