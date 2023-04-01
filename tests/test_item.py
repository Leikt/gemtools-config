import unittest
from types import MappingProxyType
from gemtoolsconfig.item import freeze_configuration


class TestFreezeConfiguration(unittest.TestCase):
    def test_freeze_configuration_with_dict(self):
        # Given
        obj = {"key": {"inner_key": "value"}}

        # When
        frozen_obj = freeze_configuration(obj)

        # Then
        self.assertIsInstance(frozen_obj, MappingProxyType)
        self.assertEqual(frozen_obj, MappingProxyType({"key": MappingProxyType({"inner_key": "value"})}))

    def test_freeze_configuration_with_list(self):
        # Given
        obj = ["value1", {"key": "value2"}]

        # When
        frozen_obj = freeze_configuration(obj)

        # Then
        self.assertIsInstance(frozen_obj, MappingProxyType)
        self.assertEqual(frozen_obj, MappingProxyType({"0": "value1", "1": MappingProxyType({"key": "value2"})}))

    def test_freeze_configuration_with_primitive_value(self):
        # Given
        obj = 42

        # When
        frozen_obj = freeze_configuration(obj)

        # Then
        self.assertEqual(frozen_obj, 42)
