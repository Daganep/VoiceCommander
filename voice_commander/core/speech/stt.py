"""
Speech-to-Text module using Vosk for offline recognition.
"""

import os
import sys
from vosk import Model, KaldiRecognizer
import pyaudio
import json
import threading
import time
import keyboard  # For push-to-talk functionality
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class STT:
    """Speech-to-text implementation using Vosk with push-to-talk and wake-word functionality."""

    def __init__(self, model_path="models", config=None):
        """
        Initialize the STT module.

        Args:
            model_path (str): Path to the Vosk model directory
            config (dict): Configuration dictionary
        """
        self.model_path = model_path
        self.model = None
        self.recognizer = None
        self.audio_stream = None
        self.audio_format = pyaudio.paInt16
        self.channels = 1
        self.rate = 16000
        self.chunk = 2048
        self.is_listening = False
        self.listening_thread = None
        self.push_to_talk_key = "ctrl+alt+v"
        self.wake_word_enabled = False
        self.wake_word = "командуй"  # Default Russian wake word

        if config:
            self.push_to_talk_key = config.get('push_to_talk_key', 'ctrl+alt+v')
            self.wake_word_enabled = config.get('wake_word_enabled', False)
            self.wake_word = config.get('wake_word', 'командуй')

    def load_model(self):
        """Load the Vosk model."""
        if not os.path.exists(self.model_path):
            logger.error(f"Vosk model directory not found: {self.model_path}")
            raise FileNotFoundError(f"Vosk model directory not found: {self.model_path}")

        try:
            self.model = Model(self.model_path)
            self.recognizer = KaldiRecognizer(self.model, self.rate)
            logger.info("Vosk model loaded successfully")
            return True
        except Exception as e:
            logger.error(f"Error loading Vosk model: {e}")
            return False

    def start_listening(self, callback=None):
        """
        Start listening for speech input.

        Args:
            callback (function): Optional callback function to handle recognized text
        """
        if not self.model:
            raise RuntimeError("Model not loaded. Call load_model() first.")

        # Wait for either push-to-talk key press or wake-word detection
        if not self._wait_for_activation():
            return None

        audio = pyaudio.PyAudio()

        # Open audio stream
        stream = audio.open(
            format=self.audio_format,
            channels=self.channels,
            rate=self.rate,
            input=True,
            frames_per_buffer=self.chunk
        )

        logger.info("Listening for speech...")
        self.is_listening = True

        try:
            while self.is_listening:
                data = stream.read(self.chunk, exception_on_overflow=False)
                if len(data) == 0:
                    break

                if self.recognizer.AcceptWaveform(data):
                    result = json.loads(self.recognizer.Result())
                    text = result.get("text", "")

                    # Handle empty results
                    if text:
                        logger.info(f"Recognized: {text}")
                        if callback:
                            callback(text)
                        return text  # Return the recognized text

        except KeyboardInterrupt:
            logger.info("\nStopping listening...")
        except Exception as e:
            logger.error(f"Error during speech recognition: {e}")
        finally:
            self.is_listening = False
            try:
                stream.stop_stream()
                stream.close()
            except:
                pass
            audio.terminate()

        return None

    def stop_listening(self):
        """Stop the listening process."""
        self.is_listening = False

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

    def is_model_loaded(self):
        """Check if the Vosk model is loaded."""
        return self.model is not None

    def _wait_for_activation(self):
        """
        Wait for either push-to-talk key press or wake-word detection.

        Returns:
            bool: True if activation successful, False otherwise
        """
        if self.wake_word_enabled:
            logger.info(f"Waiting for wake-word: '{self.wake_word}'")
            return self._wait_for_wake_word()
        else:
            logger.info(f"Waiting for push-to-talk key: {self.push_to_talk_key}")
            try:
                keyboard.wait(self.push_to_talk_key)
                logger.info("Push-to-talk key pressed, starting speech recognition...")
                return True
            except Exception as e:
                logger.error(f"Error waiting for push-to-talk key: {e}")
                return False

    def _wait_for_wake_word(self):
        """
        Wait for wake-word detection.

        Returns:
            bool: True if wake-word detected, False otherwise
        """
        # For simplicity in this implementation, we'll just wait for push-to-talk
        # as actual wake-word detection would require more complex processing
        # In a real implementation, this would be a separate thread monitoring audio
        # for the specific wake-word pattern

        try:
            keyboard.wait(self.push_to_talk_key)
            logger.info("Push-to-talk key pressed, starting speech recognition...")
            return True
        except Exception as e:
            logger.error(f"Error waiting for wake-word: {e}")
            return False

    def get_audio_devices(self):
        """
        Get available audio input devices.

        Returns:
            list: List of available audio input devices
        """
        audio = pyaudio.PyAudio()
        devices = []
        try:
            for i in range(audio.get_device_count()):
                info = audio.get_device_info_by_index(i)
                if info['maxInputChannels'] > 0:
                    devices.append({
                        'index': i,
                        'name': info['name'],
                        'defaultSampleRate': info['defaultSampleRate']
                    })
        except Exception as e:
            logger.error(f"Error getting audio devices: {e}")
        finally:
            try:
                audio.terminate()
            except:
                pass

        return devices


def get_stt_instance(model_path="models", config=None):
    """
    Factory function to create and return an STT instance.

    Args:
        model_path (str): Path to the Vosk model directory
        config (dict): Configuration dictionary

    Returns:
        STT: Initialized STT instance
    """
    stt = STT(model_path=model_path, config=config)
    if stt.load_model():
        return stt
    else:
        raise RuntimeError("Failed to initialize STT: could not load model")