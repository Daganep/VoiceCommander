"""
Text-to-Speech module using SAPI for Windows.
"""

import pyttsx3

class TTS:
    """Text-to-speech implementation using pyttsx3 with SAPI."""

    def __init__(self, voice_engine="sapi"):
        """
        Initialize the TTS module.

        Args:
            voice_engine (str): Voice engine to use ("sapi" for Windows)
        """
        self.engine = pyttsx3.init()
        self.voice_engine = voice_engine

        # Set up voice properties
        self.set_voice_properties()

    def set_voice_properties(self):
        """Set up voice properties like rate, volume, and voice."""
        # Set speech rate (words per minute)
        self.engine.setProperty('rate', 150)

        # Set volume (0.0 to 1.0)
        self.engine.setProperty('volume', 0.9)

        # Select voice engine
        if self.voice_engine == "sapi":
            # For Windows SAPI, we can select different voices
            voices = self.engine.getProperty('voices')
            if voices:
                # Try to find a Russian voice or use the first available
                for voice in voices:
                    if 'ru' in voice.id.lower() or 'russian' in voice.name.lower():
                        self.engine.setProperty('voice', voice.id)
                        break

    def speak(self, text):
        """
        Speak the given text.

        Args:
            text (str): Text to speak
        """
        try:
            self.engine.say(text)
            self.engine.runAndWait()
        except Exception as e:
            print(f"Error in TTS: {e}")

    def set_rate(self, rate):
        """
        Set speech rate.

        Args:
            rate (int): Words per minute
        """
        self.engine.setProperty('rate', rate)

    def set_volume(self, volume):
        """
        Set speech volume.

        Args:
            volume (float): Volume level (0.0 to 1.0)
        """
        self.engine.setProperty('volume', volume)

    def set_voice(self, voice_id):
        """
        Set the voice to use.

        Args:
            voice_id (str): Voice identifier
        """
        self.engine.setProperty('voice', voice_id)