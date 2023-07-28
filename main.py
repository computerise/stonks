#!/usr/bin/env python3
"""Application entry point."""

from stonks.configuration import ApplicationSettings, MetricAssumptions, APIKeys
from stonks.manager import ApplicationManager
from stonks.command_line_interface import CommandLineInterface

SETTINGS_FILE_PATH = "settings.toml"
METRIC_ASSUMPTIONS_FILE_PATH = "assumptions.toml"


def main() -> None:
    """Launch application."""
    app_settings = ApplicationSettings(SETTINGS_FILE_PATH)
    metric_assumptions = MetricAssumptions(METRIC_ASSUMPTIONS_FILE_PATH)
    CommandLineInterface.intro(app_settings.version, app_settings.authors)
    app_settings.configure_application()
    api_keys = APIKeys(app_settings.api_key_names)
    manager = ApplicationManager(app_settings, metric_assumptions, api_keys)
    manager.start()
    CommandLineInterface.outro("Program executed successfully.")


if __name__ == "__main__":
    main()
