#!/usr/bin/env python3
"""Application entry point."""

from sys import exit

from stonks.configuration import ApplicationSettings, MetricAssumptions
from stonks.manager import ApplicationManager
from stonks.command_line_interface import CommandLineInterface


def main():
    """Launch application."""
    app_settings = ApplicationSettings()
    metric_assumptions = MetricAssumptions()
    CommandLineInterface.intro(app_settings.version, app_settings.authors)
    manager = ApplicationManager(app_settings, metric_assumptions)
    manager.start()
    CommandLineInterface.outro("Program executed successfully.")
    exit(0)


if __name__ == "__main__":
    main()
