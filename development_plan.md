# Development Plan: Voice Commander for Windows (Offline)

## Development Log
For detailed development history, see: [development_log.md](development_log.md)

**Note:** All entries in the development log must include timestamps in the format "HH:mm:ss DD.MM.YYYY" for each task completed.

## 1. Project Setup and Foundation

### 1.1 Create project structure
- [x] Initialize repository
- [x] Create directory structure:
  ```
  voice_commander/
    requirements.txt
    config.yaml
    voice_commander.py     # main entry point, main loop
    core/
      speech/
        stt.py             # Vosk for speech-to-text
        tts.py             # SAPI for text-to-speech
      commands/
        parser.py          # parse spoken commands into Command objects
        schema.py          # command definitions and validation
      actions/
        launch.py          # application launching
        close.py           # process termination
        window.py          # window management (minimize, maximize, bring to front, close)
        ui_click.py        # click UI elements using OCR
        ui_type.py         # text input into fields using OCR
        screen_ocr.py      # screen text reading using OCR
      ui/
        automation.py      # pywinauto for UI automation
        ocr.py             # Tesseract/PaddleOCR integration
        coords.py          # pyautogui for coordinates and input actions
      apps/
        registry.py        # application alias mapping
        processes.py       # process management with psutil
      feedback.py        # unified output: speak + log
      logger.py          # logging setup with rotation
    models/              # Vosk model directory
    logs/                # log files directory
  ```

### 1.2 Set up development environment
- [x] Create virtual environment
- [x] Install dependencies from requirements.txt
- [x] Configure Tesseract OCR and Russian language data
- [x] Download Vosk Russian model (~45 MB)
- [x] Test basic setup with sample commands

### 1.3 Create configuration system
- [x] Implement config.yaml parser
- [x] Define default settings for:
  - Language (Russian)
  - Voice engine (SAPI)
  - OCR engine (Tesseract)
  - Confirmation prompts (enabled by default)
  - Push-to-talk key combination

## 2. Text-based Command Module Development

### 2.1 Text command handling
- [x] Implement text-based REPL interface for testing
- [x] Create command parser that accepts text commands
- [x] Add basic command recognition logic

### 2.2 Text feedback system
- [x] Implement feedback.py module with unified output functions
- [x] Create logging functionality with console and file output
- [x] Test logging with different log levels

### 2.3 Testing text module
- [x] Write unit tests for command parsing
- [x] Test feedback and logging functionality
- [x] Verify REPL interface works correctly

## 3. Voice Recognition Module Development

### 3.1 Speech-to-text implementation
- [x] Integrate Vosk STT engine for offline recognition
- [x] Implement push-to-talk functionality (Ctrl+Alt+V)
- [x] Add wake-word support (basic implementation with push-to-talk as activation)

### 3.2 Text-to-speech implementation
- [x] Integrate pyttsx3 with SAPI for text-to-speech
- [x] Implement voice feedback for commands and results
- [x] Test different voice settings

### 3.3 Voice command loop
- [x] Create main listening loop with push-to-talk
- [x] Implement timeout handling ("Не понял, повторите")
- [x] Add error handling for recognition failures

## 4. Application Management Module Development

### 4.1 Launch applications
- [x] Implement launch.py with alias registry
- [x] Test application launching with different programs
- [x] Verify proper process management

### 4.2 Close applications
- [x] Implement close.py with psutil process termination
- [x] Add confirmation prompts for destructive actions
- [x] Test closing various types of applications

### 4.3 Command execution system
- [x] Implement command executor to map commands to actions
- [x] Fix text interface to properly execute commands
- [x] Update main voice commander loop to use command execution

## 5. Window Management Module Development

### 5.1 Window control functionality
- [x] Implement window.py with pywinauto automation
- [x] Create functions for minimize, maximize, bring to front, close
- [x] Test with real Windows applications

### 5.2 Window state management
- [x] Add window focus and positioning controls
- [x] Implement window state restoration
- [x] Test cross-application window management

## 6. OCR Text Reading Module Development

### 6.1 Screen capture and OCR processing
- [x] Implement screen_ocr.py with Tesseract/PaddleOCR
- [x] Create screenshot functionality
- [x] Add text extraction from screen regions

### 6.2 OCR-based UI element detection
- [x] Develop OCR search for button labels and field names
- [x] Test accuracy with various UI elements
- [x] Implement coordinate calculation from OCR results

## 7. UI Interaction Module Development

### 7.1 Click UI elements
- [x] Implement ui_click.py with OCR + pyautogui
- [x] Test clicking buttons identified by text
- [x] Add error handling for missing UI elements

### 7.2 Text input into fields
- [x] Implement ui_type.py with OCR + text input automation
- [x] Test typing into different field types (text boxes, combo boxes)
- [x] Add validation for field identification

## 8. Polishing and Enhancement

### 8.1 Handle ambiguous commands
- [x] Implement conflict resolution for multiple OCR matches
- [x] Add "say options" functionality when ambiguity exists
- [x] Improve command parsing for edge cases

### 8.2 Confirmation prompts
- [ ] Enhance confirmation system for destructive actions
- [ ] Add configurable confirmation thresholds
- [ ] Test user interaction with confirmations

### 8.3 User experience improvements
- [ ] Add tray icon (pystray) for start/stop functionality
- [ ] Implement graceful error handling and recovery
- [ ] Add comprehensive logging for debugging

## 9. Documentation and Packaging

### 9.1 Project documentation
- [ ] Create README.md with project overview
- [ ] Document installation instructions
- [ ] Write usage examples and command reference

### 9.2 Installation guide
- [ ] Create installation script or detailed manual steps
- [ ] Document required system dependencies
- [ ] Add troubleshooting section

### 9.3 Application packaging
- [ ] Package as .exe using PyInstaller or similar tool
- [ ] Test packaged application functionality
- [ ] Create distribution package with all necessary files

## 10. Final Testing and Validation

### 10.1 Integration testing
- [ ] Test complete workflow from voice input to execution
- [ ] Verify all modules work together seamlessly
- [ ] Test edge cases and error conditions

### 10.2 Performance optimization
- [ ] Optimize OCR processing for speed
- [ ] Reduce memory usage where possible
- [ ] Improve responsiveness of voice commands

### 10.3 User acceptance testing
- [ ] Validate against original requirements
- [ ] Test with various real-world scenarios
- [ ] Document final features and limitations

## Milestones Summary

**Milestone 1 (Week 1):** Foundation, text interface, basic logging
**Milestone 2 (Week 2):** Voice recognition, TTS, basic command execution  
**Milestone 3 (Week 3):** Application management, window controls
**Milestone 4 (Week 4):** OCR functionality, UI interaction
**Milestone 5 (Week 5):** Polishing, documentation, packaging