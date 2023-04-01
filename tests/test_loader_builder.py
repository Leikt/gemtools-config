import unittest
from typing import Dict, Callable

from gemtoolsconfig.loader import ConfigurationLoaderBuilder, ConfigurationLoader


class TestConfigurationLoaderBuilder(unittest.TestCase):
    def test_build(self):
        loading_handlers = [lambda x: x, lambda x: x]
        lazy_handlers = [lambda x: x, lambda x: x]

        builder = ConfigurationLoaderBuilder()
        for handler in loading_handlers:
            builder.add_loading_handler(handler)

        for handler in lazy_handlers:
            builder.add_lazy_handler(handler)

        loader: ConfigurationLoader = builder.build()
        self.assertIsInstance(loader, ConfigurationLoader)

        self.assertListEqual(loader._loading_handlers, loading_handlers)
        self.assertListEqual(loader._lazy_handlers, lazy_handlers)

    def test_add_loading_handler(self):
        loading_handler: Callable[[Dict], Dict] = lambda x: x
        builder = ConfigurationLoaderBuilder()
        builder.add_loading_handler(loading_handler)

        self.assertIn(loading_handler, builder._loading_handlers)

    def test_add_lazy_handler(self):
        lazy_handler: Callable[[Dict], Dict] = lambda x: x
        builder = ConfigurationLoaderBuilder()
        builder.add_lazy_handler(lazy_handler)

        self.assertIn(lazy_handler, builder._lazy_handlers)