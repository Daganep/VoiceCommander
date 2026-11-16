# Voice Commander for Windows

Offline voice control application for Windows using Vosk and Tesseract OCR.

## Overview

Voice Commander is a Windows application that allows users to control their computer through voice commands without internet connectivity. It uses Vosk for speech recognition and Tesseract OCR for screen reading, enabling interaction with applications and UI elements through voice commands.

## Features

- Offline speech-to-text using Vosk
- Text-to-speech using SAPI
- Application launching and closing
- Window management (minimize, maximize, bring to front, close)
- UI element interaction through OCR-based clicking and text input
- Screen reading functionality using OCR
- Push-to-talk keyboard shortcut and wake-word support

## Configuration

The application uses a YAML configuration file (`config.yaml`) to control various settings:

### Configuration Options

- `language`: Language setting (default: 'ru' for Russian)
- `voice_engine`: Voice engine selection (default: 'sapi')
- `ocr_engine`: OCR engine choice (default: 'tesseract')
- `confirmations`: Enable confirmation prompts for destructive actions (default: true)
- `push_to_talk_key`: Push-to-talk key combination (default: 'Ctrl+Alt+V')
- `wake_word_enabled`: Enable wake-word activation (default: false)
- `wake_word`: Default wake word (default: 'командуй')
- `log_level`: Logging level (default: 'INFO')
- `log_rotation`: Enable log rotation (default: true)

### Configuration File Location

The configuration file is located at `config.yaml` in the project root directory. If the file doesn't exist when the application starts, it will be automatically created with default values.

## Installation

1. Create a virtual environment:
   ```
   python -m venv venv
   ```

2. Activate the virtual environment:
   ```
   venv\Scripts\activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.md
   ```

4. Install Tesseract OCR with Russian language data:
   ```
   winget install TesseractOCR
   ```

5. Download Vosk Russian model (~45 MB) and extract to `models/` directory

## Usage

Run the application:
```
python voice_commander.py
```

For testing without microphone:
```
python voice_commander.py --text
```

## Development

The project follows a modular architecture organized by functionality:

```
voice_commander/
├── requirements.md          # Project dependencies
├── config.yaml              # Configuration file
├── voice_commander.py       # Main entry point and main loop
├── core/
│   ├── speech/
│   │   ├── stt.py           # Vosk speech-to-text implementation
│   │   └── tts.py           # SAPI text-to-speech implementation
│   ├── commands/
│   │   ├── parser.py        # Command parsing logic
│   │   └── schema.py        # Command definitions and validation
│   ├── actions/
│   │   ├── launch.py        # Application launching functionality
│   │   ├── close.py         # Process termination
│   │   ├── window.py        # Window management (minimize, maximize, etc.)
│   │   ├── ui_click.py      # Click UI elements using OCR
│   │   ├── ui_type.py       # Text input into fields using OCR
│   │   └── screen_ocr.py    # Screen text reading using OCR
│   ├── ui/
│   │   ├── automation.py    # pywinauto for UI automation
│   │   ├── ocr.py           # Tesseract/PaddleOCR integration
│   │   └── coords.py        # pyautogui for coordinates and input actions
│   ├── apps/
│   │   ├── registry.py      # Application alias mapping
│   │   └── processes.py     # Process management with psutil
│   ├── feedback.py          # Unified output: speak + log
│   └── config.py            # Configuration system
└── models/                  # Vosk model directory (not in repo)
```

## License

This project is licensed under the MIT License.