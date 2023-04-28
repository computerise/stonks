"""Configures the application."""

from tomllib import load
from dataclasses import dataclass


class Configuration:
    def load_config(config_path):
        with open("pyproject.toml", "rb") as file:
            return load(file)


class ApplicationSettings(Configuration):
    # raise NotImplementedError
    pass


class MetricAssumptions(Configuration):
    # raise NotImplementedError
    pass


@dataclass
class ApplicationData:
    settings: ApplicationSettings
    assumptions: MetricAssumptions
