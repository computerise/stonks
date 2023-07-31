"""Test management of the application."""

from unittest import TestCase

from stonks.configuration import ApplicationSettings, MetricAssumptions, APIKeys, URLs
from stonks.manager import ApplicationManager
from stonks.companies import CompanyCollection

SETTINGS_FILE_PATH = "settings.toml"
METRIC_ASSUMPTIONS_FILE_PATH = "assumptions.toml"


class TestApplicationManager(TestCase):
    """Test Application Manager."""

    @classmethod
    def setUpClass(cls) -> None:
        app_settings = ApplicationSettings(SETTINGS_FILE_PATH)
        metric_assumptions = MetricAssumptions(METRIC_ASSUMPTIONS_FILE_PATH)
        app_settings.configure_application()
        api_keys = APIKeys(app_settings.api_key_names)
        urls = URLs(app_settings.url_names)
        cls.manager = ApplicationManager(app_settings, metric_assumptions, api_keys, urls)

    def test_load_local_data(self) -> None:
        """Test loading local data."""
        company_collection = self.manager.load_local_data()
        self.assertIsInstance(company_collection, CompanyCollection)
