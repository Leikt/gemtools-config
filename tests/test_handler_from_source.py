import unittest
from unittest.mock import MagicMock
from gemtoolsio import UnknownExtensionError

from gemtoolsconfig.handlers import from_source, KEY_RESULT
from gemtoolsconfig.exceptions import ArgumentError


class TestFromSource(unittest.TestCase):

    def setUp(self):
        self.params = {
            'text': 'some config',
            'format': 'json',
        }

    def test_from_source_loads_config(self):
        expected_result = {'key': 'value'}
        load_string_mock = MagicMock(return_value=expected_result)
        from_source_module = from_source.__module__
        with unittest.mock.patch(f'{from_source_module}.load_string', load_string_mock):
            result = from_source(self.params)
            self.assertEqual(result[KEY_RESULT], expected_result)
        load_string_mock.assert_called_once_with('some config', 'json')

    def test_from_source_missing_text_param_raises_error(self):
        del self.params['text']
        with self.assertRaises(ArgumentError):
            from_source(self.params)

    def test_from_source_missing_format_param_raises_error(self):
        del self.params['format']
        with self.assertRaises(ArgumentError):
            from_source(self.params)

    def test_from_source_missing_required_param_raises_error(self):
        self.params['key'] = 'value'
        with self.assertRaises(UnknownExtensionError):
            from_source(self.params)
