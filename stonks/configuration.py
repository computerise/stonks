"""Configures the application."""

from tomllib import load
from dataclasses import dataclass


class TOMLConfiguration:
    """Base class for all TOML configuration objects."""

    def load_config(self):
        """Load a TOML file."""
        with open(self.path, "rb") as file:
            return load(file)


@dataclass
class ApplicationSettings(TOMLConfiguration):
    """All settings associated with the operation of the application."""

    path: str = "settings.toml"


@dataclass
class MetricAssumptions(TOMLConfiguration):
    """All assumptions of metrics used to processing."""

    path: str = "assumptions.toml"
