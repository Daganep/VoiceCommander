#!/usr/bin/env python3

import sys
import os

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(__file__))

# Test the configuration system
from voice_commander.core.config import config, get_config

print("Configuration loaded successfully!")
print(f"Language: {config['language']}")
print(f"Voice engine: {config['voice_engine']}")
print(f"OCR engine: {config['ocr_engine']}")
print(f"Confirmations: {config['confirmations']}")
print(f"Push-to-talk key: {config['push_to_talk_key']}")
print(f"Wake word enabled: {config['wake_word_enabled']}")
print(f"Wake word: {config['wake_word']}")

# Test getting specific values
print(f"\nSpecific config values:")
print(f"Language (using get_config): {get_config('language')}")
print(f"Voice engine (using get_config): {get_config('voice_engine')}")
print(f"Non-existent key default: {get_config('non_existent', 'default_value')}")