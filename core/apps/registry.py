"""
Application registry for Voice Commander.
Manages application aliases and mappings.
"""

import os
import json
from typing import Dict, List, Optional
from pathlib import Path

from core.logger import get_logger

logger = get_logger(__name__)


class AppRegistry:
    """Manages application aliases and mappings."""

    def __init__(self, registry_file: str = None):
        """
        Initialize the application registry.

        Args:
            registry_file (str): Path to the registry file (optional)
        """
        self.registry_file = registry_file or "app_registry.json"
        self._registry_data = {}
        self._load_registry()

    def _load_registry(self):
        """Load registry data from file."""
        try:
            if os.path.exists(self.registry_file):
                with open(self.registry_file, 'r', encoding='utf-8') as f:
                    self._registry_data = json.load(f)
                logger.info(f"Loaded application registry from {self.registry_file}")
            else:
                # Create default registry
                self._create_default_registry()
                logger.info(f"Created default application registry at {self.registry_file}")
        except Exception as e:
            logger.error(f"Failed to load registry file {self.registry_file}: {e}")
            # Create empty registry if loading fails
            self._registry_data = {}

    def _create_default_registry(self):
        """Create a default registry with common applications."""
        self._registry_data = {
            "notepad": "notepad.exe",
            "calculator": "calc.exe",
            "explorer": "explorer.exe",
            "cmd": "cmd.exe",
            "powershell": "powershell.exe",
            "chrome": "chrome.exe",
            "firefox": "firefox.exe",
            "word": "winword.exe",
            "excel": "excel.exe",
            "powerpoint": "powerpnt.exe"
        }
        self._save_registry()

    def _save_registry(self):
        """Save registry data to file."""
        try:
            with open(self.registry_file, 'w', encoding='utf-8') as f:
                json.dump(self._registry_data, f, ensure_ascii=False, indent=2)
            logger.info(f"Saved application registry to {self.registry_file}")
        except Exception as e:
            logger.error(f"Failed to save registry file {self.registry_file}: {e}")

    def get_app_path(self, alias: str) -> Optional[str]:
        """
        Get the full path for an application by its alias.

        Args:
            alias (str): Application alias

        Returns:
            Optional[str]: Full path to the application or None if not found
        """
        return self._registry_data.get(alias)

    def get_all_aliases(self) -> List[str]:
        """
        Get all registered aliases.

        Returns:
            List[str]: List of all registered aliases
        """
        return list(self._registry_data.keys())

    def add_alias(self, alias: str, app_path: str):
        """
        Add a new alias to the registry.

        Args:
            alias (str): Alias name
            app_path (str): Full path to the application
        """
        self._registry_data[alias] = app_path
        self._save_registry()
        logger.info(f"Added alias '{alias}' -> '{app_path}'")

    def remove_alias(self, alias: str):
        """
        Remove an alias from the registry.

        Args:
            alias (str): Alias name to remove
        """
        if alias in self._registry_data:
            del self._registry_data[alias]
            self._save_registry()
            logger.info(f"Removed alias '{alias}'")

    def get_all_apps(self) -> Dict[str, str]:
        """
        Get all registered applications.

        Returns:
            Dict[str, str]: Dictionary mapping aliases to application paths
        """
        return self._registry_data.copy()

    def is_alias_registered(self, alias: str) -> bool:
        """
        Check if an alias is already registered.

        Args:
            alias (str): Alias name to check

        Returns:
            bool: True if alias is registered, False otherwise
        """
        return alias in self._registry_data