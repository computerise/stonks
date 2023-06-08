"Test configuration."

from unittest import TestCase

from stonks.configuration import APIKeys


class TestAPIKeys(TestCase):
    """Test Application Settings."""

    def test_set_api_keys(self):
        with self.assertRaises(ValueError):
            APIKeys("SAMPLE_UNSET_ENVIRONMENT_VARIABLE")
