import unittest
from unittest.mock import MagicMock, patch

from gemtoolsconfig.exceptions import ConfigurationHandlerError
from gemtoolsconfig.loader import ConfigurationLoader, KEY_RESULT


class TestConfigurationLoader(unittest.TestCase):
    def setUp(self):
        self.loader = ConfigurationLoader(
            lazy_handlers=[],
            loading_handlers=[]
        )

    def test_load_with_invalid_configuration(self):
        # Test that a ConfigurationHandlerError is raised when load() is called with an invalid configuration.
        parameters = {KEY_RESULT: 42}
        with self.assertRaises(ConfigurationHandlerError):
            self.loader.load(**parameters)

    def test_load_with_missing_key_result(self):
        # Test that a ConfigurationHandlerError is raised when load() is called with a missing KEY_RESULT key.
        parameters = {'invalid_key': {}}
        with self.assertRaises(ConfigurationHandlerError):
            self.loader.load(**parameters)

    def test_load_with_valid_configuration(self):
        # Test that load() returns a ConfigurationItem when called with a valid configuration.
        configuration = {'key': 'value'}
        parameters = {KEY_RESULT: configuration}
        self.assertEqual(self.loader.load(**parameters), configuration)

    def test_lazy_load_with_invalid_parameters(self):
        # Test that a ConfigurationHandlerError is raised when lazy_load() is called with invalid parameters.
        name = 'test'
        parameters = {'invalid_key': name}
        with self.assertRaises(ConfigurationHandlerError):
            self.loader.lazy_load(name)

    def test_lazy_load_with_valid_parameters(self):
        # Test that lazy_load() returns a ConfigurationItem when called with valid parameters.
        name = 'test'
        configuration = {'key': 'value'}

        with patch.object(self.loader, 'load', MagicMock(return_value=configuration)):
            self.assertEqual(self.loader.lazy_load(name), configuration)
