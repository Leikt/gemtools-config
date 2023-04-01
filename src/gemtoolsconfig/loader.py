from __future__ import annotations
from typing import Any

from .exceptions import critical, ConfigurationHandlerError
from .item import freeze_configuration, ConfigurationItem
from .handlers import LazyHandler, LoadingHandler, KEY_RESULT


class ConfigurationLoader:
    def __init__(self,
                 lazy_handlers: list[LazyHandler],
                 loading_handlers: list[LoadingHandler]
                 ):
        """
        ConfigurationLoader constructor.

        :param lazy_handlers: List of lazy handlers.
        :type lazy_handlers: list[LazyHandler]
        :param loading_handlers: List of loading handlers.
        :type loading_handlers: list[LoadingHandler]
        """
        self._loading_handlers = loading_handlers
        self._lazy_handlers = lazy_handlers

    def load(self, **parameters: Any) -> ConfigurationItem:
        """
        Load configuration.

        :param parameters: Configuration parameters.
        :type parameters: dict
        :return: ConfigurationItem object.
        :rtype: ConfigurationItem
        :raises ConfigurationHandlerError: If the loader is not configured correctly.
        """
        for handler in self._loading_handlers:
            parameters = handler(parameters)

        if KEY_RESULT not in parameters:
            critical(f'The loader is not configured correctly. "{KEY_RESULT}" not found in the result: {parameters}',
                     ConfigurationHandlerError)

        configuration = parameters[KEY_RESULT]
        if not isinstance(configuration, list) and not isinstance(configuration, dict):
            critical(
                f'The loader gets a configuration with an invalid type: expect dict or list, got {type(configuration)}',
                ConfigurationHandlerError)

        return freeze_configuration(parameters[KEY_RESULT])

    def lazy_load(self, name: str) -> ConfigurationItem:
        """
        Lazy load configuration.

        :param name: Configuration name.
        :type name: str
        :return: ConfigurationItem object.
        :rtype: ConfigurationItem
        """
        parameters = {'name': name}
        for handler in self._lazy_handlers:
            parameters = handler(parameters)

        return self.load(**parameters)


class ConfigurationLoaderBuilder:
    """
    A builder class for constructing a `ConfigurationLoader` instance.
    """

    def __init__(self):
        """
        Initializes a new instance of the `ConfigurationLoaderBuilder` class.
        """
        self._loading_handlers = []
        self._lazy_handlers = []

    def build(self) -> ConfigurationLoader:
        """
        Builds a new `ConfigurationLoader` instance based on the current state of the builder.

        :return: A new `ConfigurationLoader` instance.
        """
        return ConfigurationLoader(
            self._lazy_handlers,
            self._loading_handlers
        )

    def add_loading_handler(self, handler: LoadingHandler) -> ConfigurationLoaderBuilder:
        """
        Adds a loading handler to the builder.

        :param handler: The loading handler to add.
        :type handler: Callable[[dict], dict]
        :return: The `ConfigurationLoaderBuilder` instance, to allow method chaining.
        """
        self._loading_handlers.append(handler)
        return self

    def add_lazy_handler(self, handler: LazyHandler) -> ConfigurationLoaderBuilder:
        """
        Adds a lazy loading handler to the builder.

        :param handler: The lazy loading handler to add.
        :type handler: Callable[[dict], dict]
        :return: The `ConfigurationLoaderBuilder` instance, to allow method chaining.
        """
        self._lazy_handlers.append(handler)
        return self
