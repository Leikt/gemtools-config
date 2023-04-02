import unittest
from unittest.mock import Mock

from gemtoolsconfig.configurations import Configurations
from gemtoolsconfig.exceptions import ConfigurationNotFoundError, ConfigurationLoaderNotFoundError, \
    ConfigurationLoaderFoundError


class TestConfigs(unittest.TestCase):
    def setUp(self) -> None:
        self.config_default = Mock()
        self.config_first = Mock()
        self.config_second = Mock()
        Configurations.configurations = {
            'config': self.config_default,
            'first': self.config_first,
            'second': self.config_second
        }

        self.loader_default = Mock()
        self.loader_default.configure_mock(**{
            'lazy_load.return_value': self.config_first,
            'load.return_value': self.config_first
        })

        self.loader_valid = Mock()
        self.loader_valid.configure_mock(**{'lazy_load.return_value': self.config_second})

        Configurations.loaders = {
            'default': self.loader_default,
            'valid': self.loader_valid
        }

    def test_clear(self):
        Configurations.clear()
        self.assertEqual({}, Configurations.configurations)
        self.assertEqual({}, Configurations.loaders)

    def test_unload(self):
        with self.assertRaises(ConfigurationNotFoundError):
            Configurations.unload('not_found')

        Configurations.unload('first')
        self.assertEqual({'config': self.config_default, 'second': self.config_second}, Configurations.configurations)

        Configurations.unload()
        self.assertEqual({'second': self.config_second}, Configurations.configurations)

    def test_add_loader(self):
        loader = Mock()
        Configurations.add_loader(loader, 'new')
        self.assertEqual({'default': self.loader_default, 'valid': self.loader_valid, 'new': loader},
                         Configurations.loaders)

        del Configurations.loaders['default']
        Configurations.add_loader(loader)
        self.assertEqual(Configurations.loaders['default'], loader)

        with self.assertRaises(ConfigurationLoaderFoundError):
            Configurations.add_loader(loader)

    def test_add_loader_overwrite_allowed(self):
        loader = Mock()
        Configurations.add_loader(loader, allow_overwrite=True)
        self.assertEqual({'default': loader, 'valid': self.loader_valid}, Configurations.loaders)

    def test_remove_loader(self):
        with self.assertRaises(ConfigurationLoaderNotFoundError):
            Configurations.remove_loader('not_found')

        Configurations.remove_loader('valid')
        self.assertEqual({'default': self.loader_default}, Configurations.loaders)

    def test_get_loader(self):
        self.assertEqual(self.loader_default, Configurations.get_loader())
        self.assertEqual(self.loader_valid, Configurations.get_loader('valid'))
        with self.assertRaises(ConfigurationLoaderNotFoundError):
            Configurations.get_loader('not_found')

    def test_get(self):
        self.assertEqual(self.config_default, Configurations.get_config(allow_lazy_load=False))
        self.assertEqual(self.config_first, Configurations.get_config('first', allow_lazy_load=False))
        with self.assertRaises(ConfigurationNotFoundError):
            Configurations.get_config('not_found', allow_lazy_load=False)

    def test_get_lazy_load_allowed(self):
        self.assertEqual(self.config_first, Configurations.get_config('new_first'))

        loader = Mock()
        loader.configure_mock(**{'lazy_load.side_effect': ConfigurationNotFoundError})
        Configurations.loaders['default'] = loader
        with self.assertRaises(ConfigurationNotFoundError):
            Configurations.get_config('not_found')

    def test_load(self):
        self.assertEqual(self.config_first, Configurations.load_config('other', path='./dummy.toml'))
        self.assertEqual(self.config_first, Configurations.get_config('other'))