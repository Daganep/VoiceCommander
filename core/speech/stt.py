"""
Speech-to-Text (STT) module using Vosk for offline recognition.
"""

import os
import sys
import threading
import time
import queue
from typing import Optional, Callable

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    import pyaudio
    import vosk
    from core.logger import get_logger

    logger = get_logger(__name__)

except ImportError as e:
    logger = None
    print(f"Failed to import required modules: {e}")

class VoskSTT:
    """Vosk-based speech-to-text implementation for offline recognition."""

    def __init__(self, model_path: str = "models", lang: str = "ru"):
        """
        Initialize the Vosk STT engine.

        Args:
            model_path (str): Path to the Vosk model directory
            lang (str): Language code (default: "ru" for Russian)
        """
        self.model_path = model_path
        self.lang = lang
        self.recognizer = None
        self.audio_stream = None
        self.is_listening = False
        self.audio_queue = queue.Queue()

        # Initialize Vosk recognizer
        self._init_recognizer()

    def _init_recognizer(self):
        """Initialize the Vosk recognizer with the appropriate model."""
        try:
            # Check if model exists
            model_dir = os.path.join(self.model_path, f"vosk-model-small-{self.lang}-0.22")
            if not os.path.exists(model_dir):
                # Try alternative path for Russian model
                model_dir = os.path.join(self.model_path, "vosk-model-ru-0.22")

            if not os.path.exists(model_dir):
                raise FileNotFoundError(f"Vosk model not found at {model_dir}")

            self.recognizer = vosk.KaldiRecognizer(vosk.Model(model_dir), 16000)
            logger.info(f"Vosk STT initialized with model: {model_dir}")

        except Exception as e:
            logger.error(f"Failed to initialize Vosk STT: {e}")
            raise

    def start_listening(self, callback: Callable[[str], None]):
        """
        Start listening for speech input.

        Args:
            callback (Callable): Function to call with recognized text
        """
        if not self.recognizer:
            raise RuntimeError("STT not initialized")

        self.is_listening = True
        self.callback = callback

        # Create audio stream
        self.audio_stream = pyaudio.PyAudio()

        # Open audio stream
        stream = self.audio_stream.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=16000,
            input=True,
            frames_per_buffer=8192
        )

        logger.info("Starting voice recognition...")

        try:
            while self.is_listening:
                data = stream.read(2048, exception_on_overflow=False)

                if len(data) == 0:
                    break

                # Feed audio to Vosk
                if self.recognizer.AcceptWaveform(data):
                    result = self.recognizer.Result()
                    # Parse the JSON result
                    import json
                    result_json = json.loads(result)
                    text = result_json.get("text", "").strip()

                    if text:
                        logger.info(f"Recognized: {text}")
                        self.callback(text)

        except Exception as e:
            logger.error(f"Error in listening loop: {e}")
            raise
        finally:
            stream.stop_stream()
            stream.close()
            self.audio_stream.terminate()

    def stop_listening(self):
        """Stop the listening process."""
        self.is_listening = False

    def recognize_once(self, audio_data: bytes) -> str:
        """
        Recognize speech from a single audio buffer.

        Args:
            audio_data (bytes): Audio data in 16kHz PCM format

        Returns:
            str: Recognized text
        """
        if not self.recognizer:
            raise RuntimeError("STT not initialized")

        if self.recognizer.AcceptWaveform(audio_data):
            result = self.recognizer.Result()
            import json
            result_json = json.loads(result)
            return result_json.get("text", "").strip()
        else:
            return ""

    def is_model_available(self) -> bool:
        """Check if the Vosk model is available."""
        try:
            model_dir = os.path.join(self.model_path, f"vosk-model-small-{self.lang}-0.22")
            if not os.path.exists(model_dir):
                model_dir = os.path.join(self.model_path, "vosk-model-ru-0.22")

            return os.path.exists(model_dir)
        except Exception:
            return False

# Global STT instance
stt_instance: Optional[VoskSTT] = None

def get_stt_instance() -> VoskSTT:
    """Get or create the global STT instance."""
    global stt_instance

    if stt_instance is None:
        try:
            stt_instance = VoskSTT()
        except Exception as e:
            logger.error(f"Failed to initialize STT: {e}")
            raise

    return stt_instance