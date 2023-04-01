import unittest

from gemtoolsconfig.item import ConfigurationItem
from gemtoolsconfig.presets import source_loader


class TestPresetSource(unittest.TestCase):
    def test_valid(self):
        loader = source_loader()
        result = loader.load(text='key = "value"', format='.toml')
        self.assertEqual(ConfigurationItem({'key': 'value'}), result)
