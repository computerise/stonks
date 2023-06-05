"Test configuration."

from unittest import TestCase

from stonks.configuration import ApplicationSettings


class TestApplicationSettings(TestCase):
    """Test Application Settings."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.application_settings = ApplicationSettings()
