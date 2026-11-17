#!/usr/bin/env python3
"""
Voice Commander for Windows - Main Entry Point
Offline voice control application for Windows using Vosk and Tesseract OCR.
"""

import sys
import os
import argparse
import threading
import time
from typing import Optional

# Add the current directory to the Python path so we can import modules
sys.path.insert(0, os.path.dirname(__file__))

# Import core modules
try:
    from core.speech.stt import get_stt_instance
    from core.speech.tts import get_tts_instance
    from core.commands.parser import CommandParser
    from core.feedback import Feedback
    from core.logger import setup_logger
    from core.error_handler import ErrorHandler

    logger = setup_logger()

except ImportError as e:
    print(f"Failed to import required modules: {e}")
    sys.exit(1)

class VoiceCommander:
    """Main Voice Commander class with voice command loop."""

    def __init__(self):
        """Initialize the Voice Commander."""
        self.stt = None
        self.tts = None
        self.parser = None
        self.feedback = None
        self.is_running = False
        self.tray_icon = None
        self.error_handler = ErrorHandler(logger)

    def initialize(self):
        """Initialize all components."""
        try:
            # Initialize speech components
            self.stt = get_stt_instance()
            self.tts = get_tts_instance()
            self.parser = CommandParser()
            self.feedback = Feedback()
            self.feedback.set_tts(self.tts)

            logger.info("Voice Commander initialized successfully")

        except Exception as e:
            error_details = self.error_handler.handle_exception(
                e, "initialization", should_exit=True)
            raise

    def handle_command(self, text: str):
        """
        Process a recognized command.

        Args:
            text (str): Recognized command text
        """
        try:
            if not text.strip():
                return

            logger.info(f"Processing command: '{text}'")

            # Parse and execute the command with feedback system
            result = self.parser.parse_command(text, self.feedback)

            if result:
                # Provide feedback about the result
                self.feedback.speak_and_log(f"Выполнено: {result['message']}")
            else:
                # Unknown command
                logger.warning(f"Unknown command: {text}")
                self.feedback.speak_and_log("Не понял, повторите")

        except Exception as e:
            error_details = self.error_handler.handle_exception(
                e, "command processing")
            # Try to recover from the error
            self.error_handler.recover_from_error(error_details)

    def voice_loop(self):
        """
        Main voice command loop with push-to-talk functionality.
        """
        logger.info("Starting voice command loop...")

        def on_speech_recognized(text: str):
            """Callback function called when speech is recognized."""
            self.handle_command(text)

        try:
            # Start listening for commands
            self.feedback.speak_and_log("Готов к работе. Нажмите Ctrl+Alt+V для активации")

            while self.is_running:
                # Wait for push-to-talk key press and then listen for speech
                logger.info("Waiting for push-to-talk key...")
                try:
                    # The STT module handles waiting for the key press and listening
                    recognized_text = self.stt.start_listening(on_speech_recognized)

                    if recognized_text is None:
                        # No text was recognized, continue loop
                        continue

                except Exception as e:
                    logger.error(f"Error in voice loop: {e}")
                    # Continue the loop to keep listening
                    continue

        except KeyboardInterrupt:
            logger.info("Voice command loop interrupted by user")
            self.feedback.speak_and_log("Завершение работы")
        except Exception as e:
            error_details = self.error_handler.handle_exception(
                e, "voice loop", should_exit=True)
            raise

    def start_tray_icon(self):
        """Start the system tray icon."""
        try:
            from core.tray import TrayIcon
            self.tray_icon = TrayIcon(self)
            # Run the tray icon in a separate thread
            tray_thread = threading.Thread(target=self.tray_icon.run, daemon=True)
            tray_thread.start()
            logger.info("System tray icon started")
        except ImportError as e:
            logger.error(f"Failed to import tray module: {e}")
            print("Warning: Could not start system tray icon. Install pystray for tray functionality.")

    def start(self):
        """Start the Voice Commander application."""
        try:
            self.initialize()

            # Start the system tray icon
            self.start_tray_icon()

            # Start the main voice loop in a separate thread
            self.is_running = True
            voice_thread = threading.Thread(target=self.voice_loop, daemon=True)
            voice_thread.start()

        except Exception as e:
            error_details = self.error_handler.handle_exception(
                e, "main application start", should_exit=True)
            raise

def main():
    """Main entry point for the Voice Commander application."""
    try:
        parser = argparse.ArgumentParser(description='Voice Commander for Windows')
        parser.add_argument('--text', action='store_true', help='Run in text mode for testing')

        args = parser.parse_args()

        if args.text:
            # Import and run text interface
            from voice_commander.text_interface import main as text_main
            text_main()
        else:
            print("Voice Commander initialized")
            # Start the voice commander
            commander = VoiceCommander()
            commander.start()

    except Exception as e:
        print(f"Fatal error in main: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()