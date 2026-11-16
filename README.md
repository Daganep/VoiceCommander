# Voice Commander for Windows

Voice Commander is an offline voice control application for Windows that allows users to control their computer through voice commands without internet connectivity.

## Features

- **Offline Speech Recognition**: Uses Vosk for fully offline speech-to-text processing
- **Russian Language Support**: Pre-configured for Russian language recognition
- **Push-to-Talk Activation**: Use Ctrl+Alt+V to activate voice recognition
- **Wake-word Support**: Configurable wake-word detection (basic implementation)
- **Application Control**: Launch and close applications
- **Window Management**: Minimize, maximize, bring to front, and close windows
- **OCR-based UI Interaction**: Click buttons and type text using screen reading
- **Text-to-Speech Feedback**: Voice feedback for commands and results

## Architecture

The application follows a modular architecture:

```
voice_commander/
├── requirements.txt          # Project dependencies
├── config.yaml               # Configuration file
├── voice_commander.py        # Main entry point and main loop
├── core/
│   ├── speech/
│   │   ├── stt.py            # Vosk speech-to-text implementation
│   │   └── tts.py            # SAPI text-to-speech implementation
│   ├── commands/
│   │   ├── parser.py         # Command parsing logic
│   │   └── schema.py         # Command definitions and validation
│   ├── actions/
│   │   ├── launch.py         # Application launching functionality
│   │   ├── close.py          # Process termination
│   │   ├── window.py         # Window management (minimize, maximize, etc.)
│   │   ├── ui_click.py       # Click UI elements using OCR
│   │   ├── ui_type.py        # Text input into fields using OCR
│   │   └── screen_ocr.py     # Screen text reading using OCR
│   ├── ui/
│   │   ├── automation.py     # pywinauto for UI automation
│   │   ├── ocr.py            # Tesseract/PaddleOCR integration
│   │   └── coords.py         # pyautogui for coordinates and input actions
│   ├── apps/
│   │   ├── registry.py       # Application alias mapping
│   │   └── processes.py      # Process management with psutil
│   ├── feedback.py           # Unified output: speak + log
│   └── logger.py             # Logging setup with rotation
├── models/                   # Vosk model directory (not in repo)
└── logs/                     # Log files directory (not in repo)
```

## Installation

1. Create a virtual environment:
   ```bash
   python -m venv venv
   ```

2. Activate the virtual environment:
   ```bash
   venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Install Tesseract OCR with Russian language data:
   ```bash
   winget install TesseractOCR
   ```

5. Download Vosk Russian model (~45 MB) and extract to `models/` directory

## Usage

### Running the Application

- **Voice Mode** (default): `python voice_commander.py`
- **Text Mode** (for testing): `python voice_commander.py --text`

### Voice Commands

1. Press **Ctrl+Alt+V** to activate push-to-talk
2. Speak your command clearly
3. The system will process and execute the command

### Configuration

The application uses `config.yaml` for configuration:

```yaml
# Voice Commander Configuration

# Language settings
language: ru  # Russian language support

# Voice engine settings
voice_engine: sapi  # SAPI for text-to-speech

# OCR engine settings
ocr_engine: tesseract  # Tesseract OCR engine

# Confirmation prompts
confirmations: true  # Enable confirmation prompts for destructive actions

# Push-to-talk key combination
push_to_talk_key: "Ctrl+Alt+V"  # Default push-to-talk key combination

# Wake-word support
wake_word_enabled: false  # Enable wake-word activation
wake_word: "командуй"  # Default wake word (Russian)

# Logging settings
log_level: "INFO"  # Logging level
log_rotation: true  # Enable log rotation
```

## Development

### STT Module Implementation

The STT module (`core/speech/stt.py`) provides:

- Vosk integration for offline speech recognition
- Push-to-talk functionality with Ctrl+Alt+V by default
- Wake-word detection support (basic implementation)
- Audio device detection and management
- Proper error handling and logging

### Testing

Run tests with:
```bash
python test_stt.py
python test_stt_integration.py
```

## License

This project is licensed under the MIT License.