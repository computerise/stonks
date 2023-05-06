"""Application entry point."""

import os
import time
from dotenv import load_dotenv

from stonks.configuration import ApplicationSettings, APIKeys
from stonks.manager import ApplicationManager

# Load .env file.
load_dotenv()


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
    manager = ApplicationManager(
        app_settings, api_keys=APIKeys(rapidapi_key=os.getenv("RAPIDAPI_KEY"))
    )
    manager.start()
    time.sleep(5)


if __name__ == "__main__":
    main()
