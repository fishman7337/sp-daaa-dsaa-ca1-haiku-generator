"""Application entry point for HaikuForge AI."""

from .menu import Menu


def main() -> None:
    """Launch the welcome screen and enter the interactive menu loop."""
    Menu.welcome()
    Menu.menu()
