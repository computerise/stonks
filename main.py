#!/usr/bin/env python3
"""Application entry point."""

from stonks.configuration import ApplicationSettings, MetricAssumptions, APIKeys, URLs
from stonks.manager import ApplicationManager
from stonks.command_line_interface import CommandLineInterface

SETTINGS_FILE_PATH = "settings.toml"
METRIC_ASSUMPTIONS_FILE_PATH = "assumptions.toml"


def load_manager() -> ApplicationManager:
    """Load configuration and initialise the ApplicationManager."""
    app_settings = ApplicationSettings(SETTINGS_FILE_PATH)
    metric_assumptions = MetricAssumptions(METRIC_ASSUMPTIONS_FILE_PATH)
    CommandLineInterface.intro(app_settings.version, app_settings.authors)
    app_settings.configure_application()
    api_keys = APIKeys(app_settings.api_key_names)
    urls = URLs(app_settings.url_names)
    return ApplicationManager(app_settings, metric_assumptions, api_keys, urls)


def main() -> None:
    """Launch application."""
    manager = load_manager()
    manager.start()
    CommandLineInterface.outro("Program executed successfully.")


def upload_local_data() -> None:
    """Upload local JSON data to a database."""
    manager = load_manager()
    company_collection = manager.load_local_data()
    manager.insert_data(company_collection)


if __name__ == "__main__":
    main()
