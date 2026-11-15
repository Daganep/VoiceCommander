"""
Application alias registry.
"""

class AppRegistry:
    """Manage application aliases and mappings."""

    def __init__(self):
        """Initialize the application registry."""
        # Default aliases for common applications
        self.aliases = {
            'explorer': 'explorer.exe',
            'notepad': 'notepad.exe',
            'calculator': 'calc.exe',
            'paint': 'mspaint.exe',
            'cmd': 'cmd.exe',
            'powershell': 'powershell.exe',
            'chrome': 'chrome.exe',
            'firefox': 'firefox.exe',
            'edge': 'msedge.exe',
            'word': 'winword.exe',
            'excel': 'excel.exe',
            'powerpoint': 'powerpnt.exe'
        }

    def add_alias(self, alias, path):
        """
        Add a new application alias.

        Args:
            alias (str): Alias name
            path (str): Full path to the executable
        """
        self.aliases[alias] = path

    def remove_alias(self, alias):
        """
        Remove an application alias.

        Args:
            alias (str): Alias name to remove
        """
        if alias in self.aliases:
            del self.aliases[alias]

    def get_path(self, alias):
        """
        Get the path for an alias.

        Args:
            alias (str): Alias name

        Returns:
            str: Path to the executable or None if not found
        """
        return self.aliases.get(alias)