"""
Configuration module for Voice Commander.
Parses and provides access to application settings from config.yaml.
"""

import yaml
import os
from pathlib import Path

# Default configuration values
DEFAULT_CONFIG = {
    'language': 'ru',
    'voice_engine': 'sapi',
    'ocr_engine': 'tesseract',
    'confirmations': True,
    'push_to_talk_key': 'Ctrl+Alt+V',
    'wake_word_enabled': False,
    'wake_word': 'командуй',
    'log_level': 'INFO',
    'log_rotation': True
}

def load_config(config_path='config.yaml'):
    """
    Load configuration from YAML file.

    Args:
        config_path (str): Path to the configuration file

    Returns:
        dict: Configuration dictionary with all settings
    """
    # Check if config file exists
    if not os.path.exists(config_path):
        # Create default config file if it doesn't exist
        save_default_config(config_path)
        return DEFAULT_CONFIG

    try:
        with open(config_path, 'r', encoding='utf-8') as file:
            config = yaml.safe_load(file) or {}

        # Merge with defaults to ensure all keys are present
        merged_config = DEFAULT_CONFIG.copy()
        merged_config.update(config)

        return merged_config

    except Exception as e:
        print(f"Error loading configuration: {e}")
        return DEFAULT_CONFIG

def save_default_config(config_path):
    """
    Save the default configuration to a file.

    Args:
        config_path (str): Path where to save the default config
    """
    try:
        with open(config_path, 'w', encoding='utf-8') as file:
            yaml.dump(DEFAULT_CONFIG, file, default_flow_style=False, allow_unicode=True)
    except Exception as e:
        print(f"Error saving default configuration: {e}")

# Load configuration when module is imported
config = load_config()

def get_config(key=None, default=None):
    """
    Get a specific configuration value or the entire config.

    Args:
        key (str): Configuration key to retrieve
        default: Default value if key is not found

    Returns:
        Value of the configuration key or entire config dict
    """
    if key is None:
        return config

    return config.get(key, default)