"""
Tray icon implementation for Voice Commander.
This module provides a system tray icon with start/stop functionality.
"""

import sys
import threading
from typing import Optional

try:
    import pystray
    from PIL import Image, ImageDraw
    import tkinter as tk
    from tkinter import messagebox
except ImportError as e:
    print(f"Failed to import required modules for tray: {e}")
    sys.exit(1)

class TrayIcon:
    """System tray icon manager for Voice Commander."""

    def __init__(self, commander):
        """
        Initialize the tray icon.

        Args:
            commander: The main VoiceCommander instance
        """
        self.commander = commander
        self.tray_icon: Optional[pystray.Icon] = None
        self.icon_image: Optional[Image.Image] = None

    def create_icon(self) -> Image.Image:
        """
        Create a simple icon image for the tray.

        Returns:
            PIL Image object for the tray icon
        """
        # Create a simple 64x64 image with a microphone symbol
        image = Image.new('RGBA', (64, 64), color=(0, 0, 0, 0))
        draw = ImageDraw.Draw(image)

        # Draw a microphone shape
        draw.rectangle([20, 15, 44, 50], fill=(100, 100, 255, 255), outline=(0, 0, 0, 255))
        draw.rectangle([25, 50, 39, 60], fill=(100, 100, 255, 255), outline=(0, 0, 0, 255))
        draw.ellipse([30, 40, 34, 44], fill=(255, 255, 255, 255))

        return image

    def start_commander(self):
        """Start the voice commander."""
        if not self.commander.is_running:
            self.commander.is_running = True
            # Start in a separate thread to avoid blocking the GUI
            threading.Thread(target=self.commander.voice_loop, daemon=True).start()
            self.update_icon_tooltip("Voice Commander: Running")

    def stop_commander(self):
        """Stop the voice commander."""
        if self.commander.is_running:
            self.commander.is_running = False
            self.update_icon_tooltip("Voice Commander: Stopped")

    def toggle_commander(self):
        """Toggle the voice commander state."""
        if self.commander.is_running:
            self.stop_commander()
        else:
            self.start_commander()

    def quit_application(self):
        """Quit the application completely."""
        self.stop_commander()
        if self.tray_icon:
            self.tray_icon.stop()
        sys.exit(0)

    def update_icon_tooltip(self, tooltip: str):
        """Update the tray icon tooltip."""
        if self.tray_icon:
            self.tray_icon.tooltip = tooltip

    def create_tray_menu(self):
        """
        Create the context menu for the tray icon.

        Returns:
            pystray.Menu object
        """
        # Define menu items
        menu_items = [
            pystray.MenuItem(
                "Старт",
                lambda: self.start_commander(),
                enabled=not self.commander.is_running
            ),
            pystray.MenuItem(
                "Стоп",
                lambda: self.stop_commander(),
                enabled=self.commander.is_running
            ),
            pystray.MenuItem(
                "Переключить",
                lambda: self.toggle_commander()
            ),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem(
                "Выход",
                lambda: self.quit_application()
            )
        ]

        return pystray.Menu(*menu_items)

    def run(self):
        """
        Run the tray icon in a separate thread.
        """
        try:
            # Create the icon image
            self.icon_image = self.create_icon()

            # Create the tray icon
            self.tray_icon = pystray.Icon(
                "VoiceCommander",
                self.icon_image,
                "Voice Commander",
                self.create_tray_menu()
            )

            # Update tooltip
            self.update_icon_tooltip("Voice Commander: Stopped")

            # Run the tray icon
            self.tray_icon.run()

        except Exception as e:
            print(f"Error running tray icon: {e}")
            sys.exit(1)