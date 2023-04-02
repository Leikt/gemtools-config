import unittest

from gemtoolsconfig.item import ConfigurationItem
from gemtoolsconfig.presets import preset_source_loader


class TestPresetSource(unittest.TestCase):
    def test_valid(self):
        loader = preset_source_loader()
        result = loader.load(text='key = "value"', format='.toml')
        self.assertEqual(ConfigurationItem({'key': 'value'}), result)
