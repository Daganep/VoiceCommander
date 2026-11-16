"""
Text-to-Speech (TTS) module using pyttsx3 with SAPI for Windows.
"""

import sys
import os
from typing import Optional

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    import pyttsx3
    from core.logger import get_logger

    logger = get_logger(__name__)

except ImportError as e:
    logger = None
    print(f"Failed to import required modules: {e}")

class SapiTTS:
    """SAPI-based text-to-speech implementation for Windows."""

    def __init__(self, voice_lang: str = "ru"):
        """
        Initialize the SAPI TTS engine.

        Args:
            voice_lang (str): Language code (default: "ru" for Russian)
        """
        self.voice_lang = voice_lang
        self.engine = None
        self._init_engine()

    def _init_engine(self):
        """Initialize the pyttsx3 engine with SAPI."""
        try:
            self.engine = pyttsx3.init()

            # Set properties
            self.engine.setProperty('rate', 150)  # Words per minute
            self.engine.setProperty('volume', 1.0)  # Volume (0.0 to 1.0)

            # Try to set Russian voice if available
            voices = self.engine.getProperty('voices')
            russian_voice = None

            for voice in voices:
                if 'ru' in voice.id.lower() or 'russian' in voice.name.lower():
                    russian_voice = voice
                    break

            if russian_voice:
                self.engine.setProperty('voice', russian_voice.id)
                logger.info(f"Using Russian voice: {russian_voice.name}")
            else:
                logger.warning("No Russian voice found, using default voice")

            logger.info("SAPI TTS initialized successfully")

        except Exception as e:
            logger.error(f"Failed to initialize SAPI TTS: {e}")
            raise

    def speak(self, text: str):
        """
        Speak the given text.

        Args:
            text (str): Text to speak
        """
        if not self.engine:
            raise RuntimeError("TTS engine not initialized")

        try:
            logger.info(f"Speaking: {text}")
            self.engine.say(text)
            self.engine.runAndWait()
        except Exception as e:
            logger.error(f"Failed to speak text: {e}")

    def speak_async(self, text: str):
        """
        Speak the given text asynchronously.

        Args:
            text (str): Text to speak
        """
        if not self.engine:
            raise RuntimeError("TTS engine not initialized")

        try:
            logger.info(f"Speaking async: {text}")
            self.engine.say(text)
        except Exception as e:
            logger.error(f"Failed to queue text for speaking: {e}")

    def set_rate(self, rate: int):
        """
        Set speech rate.

        Args:
            rate (int): Words per minute
        """
        if self.engine:
            self.engine.setProperty('rate', rate)

    def set_volume(self, volume: float):
        """
        Set speech volume.

        Args:
            volume (float): Volume level (0.0 to 1.0)
        """
        if self.engine:
            self.engine.setProperty('volume', volume)

# Global TTS instance
tts_instance: Optional[SapiTTS] = None

def get_tts_instance() -> SapiTTS:
    """Get or create the global TTS instance."""
    global tts_instance

    if tts_instance is None:
        try:
            tts_instance = SapiTTS()
        except Exception as e:
            logger.error(f"Failed to initialize TTS: {e}")
            raise

    return tts_instance