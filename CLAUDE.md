# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Windows voice commander application designed for offline operation. It allows users to control their computer through voice commands without internet connectivity, using technologies like Vosk for speech recognition and Tesseract OCR for screen reading.

## Key Features
- Offline speech-to-text (Vosk) and text-to-speech (pyttsx3) capabilities
- Application launching and closing with process management
- Window control (minimize, maximize, bring to front, close)
- UI element interaction through OCR-based clicking and text input
- Screen reading functionality using OCR
- Push-to-talk keyboard shortcut and wake-word support for voice activation
- Configuration system with YAML settings

## Architecture and Structure

The project follows a modular architecture organized by functionality:

```
voice_commander/
├── requirements.md          # Project dependencies
├── config.yaml              # Configuration file (not in repo yet)
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
│   └── logger.py            # Logging setup with rotation
├── models/                  # Vosk model directory (not in repo)
└── logs/                    # Log files directory (not in repo)
```

## Development Setup

### Prerequisites
- Python 3.8+
- Windows operating system (required for pywin32, pywinauto)
- Tesseract OCR with Russian language data installed via winget
- Vosk Russian model (~45 MB) downloaded to models/ directory

### Installation Steps
1. Create a virtual environment: `python -m venv venv`
2. Activate the virtual environment: `venv\Scripts\activate`
3. Install dependencies: `pip install -r requirements.md`
4. Install Tesseract OCR with Russian language data: `winget install TesseractOCR`
5. Download Vosk Russian model and extract to models/ directory

## Common Development Tasks

### Running the Application
- Execute main script: `python voice_commander.py`
- For testing without microphone: `python voice_commander.py --text`

### Testing Commands
The application includes a text-based REPL interface for testing commands without audio input.

### Adding New Commands
1. Define command schema in `core/commands/schema.py`
2. Implement action logic in appropriate file under `core/actions/`
3. Update parser in `core/commands/parser.py` to recognize new commands

### Modifying OCR Functionality
OCR-related code is split between:
- `core/ui/ocr.py`: OCR engine integration (Tesseract/PaddleOCR)
- `core/actions/screen_ocr.py`: Screen reading functionality
- `core/actions/ui_click.py` and `core/actions/ui_type.py`: UI interaction using OCR

## Development Workflow

The development follows a staged approach outlined in `development_plan.md`:
1. Foundation: Project setup, basic logging, text interface
2. Voice recognition: Vosk integration, push-to-talk functionality, wake-word functionality
3. Application management: Launch/close functions
4. Window control: pywinauto integration
5. OCR functionality: Screen reading and UI interaction
6. Polishing: Error handling, confirmations, tray icon

## Key Implementation Details

- Uses push-to-talk key combination (Ctrl+Alt+V) by default for voice activation
- Implements confirmation prompts for destructive actions (closing applications)
- Follows unified feedback pattern through `feedback.py` module
- All modules return results that are processed by the feedback system for speaking and logging
- Error handling is centralized with global try/except in main loop to prevent crashes from single command failures
- Command execution system properly maps parsed commands to their action implementations

## Vosk Integration Details

The STT (Speech-to-Text) module has been successfully implemented with:

1. **Offline Recognition**: Uses Vosk library for fully offline speech recognition without internet connectivity
2. **Russian Language Support**: Configured for Russian language recognition using the appropriate model
3. **Push-to-Talk Activation**: Default key combination Ctrl+Alt+V activates voice recognition
4. **Wake-word Support**: Basic implementation with configuration support for wake-word activation
5. **Error Handling**: Robust error handling with logging for model loading and recognition failures
6. **Audio Management**: Proper audio stream management with device detection capabilities

The Vosk integration is located in `core/speech/stt.py` and follows the project's coding patterns and conventions.

## TTS Integration Details

The TTS (Text-to-Speech) module has been successfully implemented with:

1. **pyttsx3 Integration**: Uses pyttsx3 library for text-to-speech conversion
2. **SAPI Engine**: Configured to use Windows SAPI engine for high-quality voice output
3. **Russian Language Support**: Automatically selects Russian voices when available
4. **Voice Customization**: Supports configurable speech rate, volume, and voice selection
5. **Error Handling**: Robust error handling with logging for synthesis failures

The TTS integration is located in `core/speech/tts.py` and follows the project's coding patterns and conventions.

## TTS Integration Details

The TTS (Text-to-Speech) module has been successfully implemented with:

1. **pyttsx3 Integration**: Uses pyttsx3 library for text-to-speech conversion
2. **SAPI Engine**: Configured to use Windows SAPI engine for high-quality voice output
3. **Russian Language Support**: Automatically selects Russian voices when available
4. **Voice Customization**: Supports configurable speech rate, volume, and voice selection
5. **Error Handling**: Robust error handling with logging for synthesis failures

The TTS integration is located in `core/speech/tts.py` and follows the project's coding patterns and conventions.

## Testing Strategy

1. Unit tests for individual components (parser, actions)
2. Integration testing of complete command workflows
3. Manual testing with real Windows applications
4. Testing with various UI elements and screen layouts
5. Edge case testing for OCR ambiguity resolution

## Configuration

The application uses YAML configuration in `config.yaml` to control:
- Language settings (Russian by default)
- Voice engine selection (SAPI)
- OCR engine choice (Tesseract by default)
- Confirmation prompts setting
- Push-to-talk key combination
- Wake-word activation support

## Development Logging

All development work should be documented in a structured format to maintain clear progress tracking and knowledge sharing. The following format should be used for development log entries:

### Log Entry Format
Each log entry should follow this structure:
```
YYYY-MM-DD - [Task/Feature] - [Brief Description]
- Detailed explanation of what was accomplished
- Any challenges encountered and how they were resolved
- Code changes made (file names, key functions)
- Testing performed
- References to related issues or documentation
```

### Example Log Entry
```
2026-11-16 - Voice Recognition Integration - Implemented Vosk speech-to-text functionality with push-to-talk activation
- Integrated Vosk library for offline speech recognition
- Added push-to-talk key combination (Ctrl+Alt+V) 
- Implemented wake-word detection capability
- Created stt.py module with proper error handling
- Tested with various audio input sources and noise conditions
- Updated CLAUDE.md with documentation of new features
```

### Log Maintenance Guidelines
- Log entries should be added after each significant development task or feature implementation
- Entries should be written in Russian to match the project's default language
- All code changes should be reflected in the log with specific file names and function details
- Documentation updates should reference the corresponding CLAUDE.md modifications
- Log entries should be concise yet comprehensive enough for other developers to understand progress