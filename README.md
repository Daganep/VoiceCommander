# Voice Commander for Windows

Voice Commander is an offline voice control application for Windows that allows users to control their computer through voice commands without internet connectivity.

## Features

- Offline speech-to-text using Vosk
- Text-to-speech with SAPI engine
- Application launching and closing
- Window management (minimize, maximize, bring to front)
- UI element interaction through OCR-based clicking and text input
- Screen reading functionality using OCR
- Push-to-talk keyboard shortcut and wake-word support
- Configuration system with YAML settings

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
   pip install -r requirements.txt
   ```

4. Install Tesseract OCR with Russian language data:
   ```
   winget install TesseractOCR
   ```

5. Download Vosk Russian model and extract to `models/` directory

## Usage

### Running the Application

To run in voice mode (default):
```
python voice_commander.py
```

To run in text testing mode:
```
python voice_commander.py --text
```

### Text Interface Commands

When running in text mode, you can enter commands directly:

- `Запусти [приложение]` - запустить приложение (e.g., "Запусти блокнот")
- `Закрой [приложение]` - закрыть приложение (e.g., "Закрой браузер")
- `Сверни [окно]` - свернуть окно (e.g., "Сверни Chrome")
- `Разверни [окно]` - развернуть окно (e.g., "Разверни Notepad")
- `Прибери [окно]` - принести окно вперёд (e.g., "Прибери VS Code")
- `Кликни [текст элемента]` - кликнуть по элементу интерфейса (e.g., "Кликни OK")
- `Введи [текст элемента] [текст для ввода]` - ввести текст в поле (e.g., "Введи логин admin")
- `Прочти [регион]` - прочитать текст с экрана (e.g., "Прочти заголовок")
- `Помощь` - показать справку

## Project Structure

```
voice_commander/
├── requirements.txt          # Project dependencies
├── config.yaml               # Configuration file
├── voice_commander.py        # Main entry point and main loop
├── core/
│   ├── speech/
│   │   ├── stt.py            # Vosk speech-to-text implementation
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
│   └── logger.py            # Logging setup with rotation
├── models/                   # Vosk model directory (not in repo)
└── logs/                     # Log files directory (not in repo)
```

## Development

See `development_plan.md` for the complete development plan and progress tracking.

## License

This project is licensed under the MIT License.