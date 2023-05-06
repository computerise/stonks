"""Application entry point."""

import time
import logging

from stonks.configuration import ApplicationSettings
from stonks.manager import ApplicationManager


def intro(version: str, authors: list[str]) -> None:
    """Introduce the application."""
    print(f"Launching 'stonks' version {version}.\nAuthored by:\n")
    print(*authors, sep=", ")


def main():
    """Launch application."""
    app_settings = ApplicationSettings()
    intro(
        app_settings.version,
        app_settings.authors,
    )
    manager = ApplicationManager(app_settings)
    manager.start()
    time.sleep(5)


if __name__ == "__main__":
    main()
