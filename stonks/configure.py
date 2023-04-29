"""Configures the application."""

from tomllib import load
from dataclasses import dataclass


class Configuration:
    def load_config(self):
        with open(self.path, "rb") as file:
            return load(file)


@dataclass
class ApplicationSettings(Configuration):
    path: str = "settings.toml"


@dataclass
class MetricAssumptions(Configuration):
    path: str = "assumptions.toml"
