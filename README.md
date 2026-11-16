# Voice Commander for Windows

Voice Commander is an offline voice control application for Windows that allows users to control their computer through voice commands without internet connectivity.

## Features

- **Offline Operation**: Fully offline speech recognition using Vosk
- **Voice Control**: Control applications, windows, and UI elements with voice commands
- **Text-to-Speech**: Voice feedback for commands and results using SAPI
- **OCR Integration**: Screen reading and UI element interaction using Tesseract OCR
- **Push-to-Talk**: Activate voice recognition with Ctrl+Alt+V key combination
- **Cross-Platform**: Designed specifically for Windows operating system

## Installation

### Prerequisites

1. Python 3.8 or higher
2. Windows operating system (required for pywin32, pywinauto)
3. Tesseract OCR with Russian language data installed via winget
4. Vosk Russian model (~45 MB) downloaded to models/ directory

### Setup Steps

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

5. Download Vosk Russian model and extract to models/ directory

## Usage

### Running the Application

- **Voice Mode**: `python voice_commander.py`
  - Use Ctrl+Alt+V to activate voice recognition
  - Speak commands like "запустить приложение браузер" or "закрыть приложение блокнот"

- **Text Mode**: `python voice_commander.py --text`
  - Test commands without audio input
  - Type commands directly in the console

### Available Commands

- `помощь` - Show help information
- `запустить приложение [имя]` - Launch an application by name
- `закрыть приложение [имя]` - Close an application
- `максимизировать окно` - Maximize active window
- `минимизировать окно` - Minimize active window
- `восстановить окно` - Restore active window
- `перевести окно в фокус` - Bring active window to front
- `прочитать текст с экрана` - Read text from screen using OCR
- `кликнуть на [текст]` - Click on UI element with matching text
- `ввести в поле [текст]` - Type text into a field

## Project Structure

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

## Development

The development follows a staged approach outlined in `development_plan.md`:
1. Foundation: Project setup, basic logging, text interface
2. Voice recognition: Vosk integration, push-to-talk functionality, wake-word functionality
3. Application management: Launch/close functions
4. Window control: pywinauto integration
5. OCR functionality: Screen reading and UI interaction
6. Polishing: Error handling, confirmations, tray icon

## License

This project is licensed under the MIT License.