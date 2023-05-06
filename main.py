"""Application entry point."""

import os
from sys import exit
from dotenv import load_dotenv

from stonks.configuration import ApplicationSettings, APIKeys
from stonks.manager import ApplicationManager
from stonks.command_line_interface import CommandLineInterface

# Load .env file.
load_dotenv()


def main():
    """Launch application."""
    app_settings = ApplicationSettings()
    CommandLineInterface.outro_duration_seconds = app_settings.outro_duration_seconds
    CommandLineInterface.intro(app_settings.version, app_settings.authors)
    manager = ApplicationManager(
        app_settings, api_keys=APIKeys(rapidapi_key=os.getenv("RAPIDAPI_KEY"))
    )
    manager.start()
    CommandLineInterface.outro("Program executed successfully.")
    exit(0)


if __name__ == "__main__":
    main()
