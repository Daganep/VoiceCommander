"""
Speech-to-Text module using Vosk for offline recognition.
"""

import os
import sys
from vosk import Model, KaldiRecognizer
import pyaudio
import json

class STT:
    """Speech-to-text implementation using Vosk."""

    def __init__(self, model_path="models"):
        """
        Initialize the STT module.

        Args:
            model_path (str): Path to the Vosk model directory
        """
        self.model_path = model_path
        self.model = None
        self.recognizer = None
        self.audio_stream = None
        self.audio_format = pyaudio.paInt16
        self.channels = 1
        self.rate = 16000
        self.chunk = 2048

    def load_model(self):
        """Load the Vosk model."""
        if not os.path.exists(self.model_path):
            raise FileNotFoundError(f"Vosk model directory not found: {self.model_path}")

        try:
            self.model = Model(self.model_path)
            self.recognizer = KaldiRecognizer(self.model, self.rate)
            print("Vosk model loaded successfully")
            return True
        except Exception as e:
            print(f"Error loading Vosk model: {e}")
            return False

    def start_listening(self):
        """Start listening for speech input."""
        if not self.model:
            raise RuntimeError("Model not loaded. Call load_model() first.")

        audio = pyaudio.PyAudio()

        # Open audio stream
        stream = audio.open(
            format=self.audio_format,
            channels=self.channels,
            rate=self.rate,
            input=True,
            frames_per_buffer=self.chunk
        )

        print("Listening for speech...")
        try:
            while True:
                data = stream.read(self.chunk, exception_on_overflow=False)
                if len(data) == 0:
                    break

                if self.recognizer.AcceptWaveform(data):
                    result = json.loads(self.recognizer.Result())
                    return result.get("text", "")

        except KeyboardInterrupt:
            print("\nStopping listening...")
        finally:
            stream.stop_stream()
            stream.close()
            audio.terminate()

    def recognize_text(self, audio_data):
        """
        Recognize text from audio data.

        Args:
            audio_data (bytes): Audio data to recognize

        Returns:
            str: Recognized text
        """
        if not self.model:
            raise RuntimeError("Model not loaded. Call load_model() first.")

        if self.recognizer.AcceptWaveform(audio_data):
            result = json.loads(self.recognizer.Result())
            return result.get("text", "")
        else:
            # If no speech detected, return empty string
            return ""