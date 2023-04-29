"""Configures the application."""

from tomllib import load
from dataclasses import dataclass


class Configuration:
    """Base class for all TOML configuration objects."""

    def load_config(self):
        with open(self.path, "rb") as file:
            return load(file)


@dataclass
class ApplicationSettings(Configuration):
    """All settings associated with the operation of the application."""

    path: str = "settings.toml"


@dataclass
class MetricAssumptions(Configuration):
    """All assumptions of metrics used to processing."""

    path: str = "assumptions.toml"
