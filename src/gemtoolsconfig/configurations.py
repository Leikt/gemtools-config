from .item import ConfigurationItem
from .loader import ConfigurationLoader

from .exceptions import ConfigurationLoaderFoundError, ConfigurationNotFoundError, \
    ConfigurationLoaderNotFoundError, critical, ConfigurationLoadingError

DEFAULT_CONFIGURATION_NAME = 'config'
DEFAULT_LOADER_NAME = 'default'


class Configurations:
    """
    A class representing a collection of configurations and configuration loaders.
    """
    configurations: dict[str, ConfigurationItem] = {}
    loaders: dict[str, ConfigurationLoader] = {}

    @classmethod
    def clear(cls):
        """
        Clears all configurations and configuration loaders.

        :return: None
        """
        cls.loaders.clear()
        cls.configurations.clear()

    @classmethod
    def unload(cls,
               config_name: str = None
               ):
        """
        Unloads the configuration with the given name.

        :param config_name: The name of the configuration to unload.
        :type config_name: str
        :raises ConfigurationNotFoundError: If the specified configuration does not exist.
        :return: None
        """
        if config_name is None:
            config_name = DEFAULT_CONFIGURATION_NAME
        if config_name not in cls.configurations:
            critical(f'Configuration "{config_name}" cannot be found.', ConfigurationNotFoundError)
        del cls.configurations[config_name]

    @classmethod
    def add_loader(cls,
                   loader: ConfigurationLoader,
                   loader_name: str = None,
                   allow_overwrite: bool = False
                   ):
        """
        Adds a configuration loader to the collection.

        :param loader: The configuration loader to add.
        :type loader: ConfigurationLoader
        :param loader_name: The name of the configuration loader.
        :type loader_name: str
        :param allow_overwrite: Whether to allow overwriting an existing loader with the same name.
        :type allow_overwrite: bool
        :raises ConfigurationLoaderFoundError: If a loader with the specified name already exists and `allow_overwrite` is `False`.
        :return: None
        """
        if loader_name is None:
            loader_name = DEFAULT_LOADER_NAME
        if loader_name in cls.loaders and not allow_overwrite:
            critical(f'A loader named "{loader_name}" already exists.', ConfigurationLoaderFoundError)
        cls.loaders[loader_name] = loader

    @classmethod
    def remove_loader(cls,
                      loader_name: str = None
                      ):
        """
        Removes the configuration loader with the given name.

        :param loader_name: The name of the configuration loader to remove.
        :type loader_name: str
        :raises ConfigurationLoaderNotFoundError: If the specified loader does not exist.
        :return: None
        """
        if loader_name is None:
            loader_name = DEFAULT_LOADER_NAME
        if loader_name not in cls.loaders:
            critical(f'Loader "{loader_name}" cannot be found.', ConfigurationLoaderNotFoundError)
        del cls.loaders[loader_name]

    @classmethod
    def load_config(cls,
                    config_name: str = None,
                    loader_name: str = None,
                    allow_overwrite: bool = False,
                    **parameters,
                    ) -> ConfigurationItem:
        if config_name is None:
            config_name = DEFAULT_CONFIGURATION_NAME
        if loader_name is None:
            loader_name = DEFAULT_LOADER_NAME
        config = cls.get_loader(loader_name).load(**parameters)
        cls.add_config(config, config_name=config_name, allow_overwrite=allow_overwrite)
        return config

    @classmethod
    def add_config(cls, config: ConfigurationItem, config_name: str = None, allow_overwrite: bool = False):
        if config_name is None:
            config_name = DEFAULT_CONFIGURATION_NAME
        if config_name in cls.configurations and not allow_overwrite:
            critical(f'Configuration "{config_name}" is already loaded. Allow overwrite to erase the old one.',
                     ConfigurationLoadingError)
        cls.configurations[config_name] = config

    @classmethod
    def get_config(cls,
                   config_name: str = None,
                   allow_lazy_load: bool = True
                   ) -> ConfigurationItem:
        """
        Gets the configuration with the given name.

        :param config_name: The name of the configuration to get.
        :type config_name: str
        :param allow_lazy_load: Whether to allow lazy loading of the configuration if it does not exist.
        :type allow_lazy_load: bool
        :raises ConfigurationNotFoundError: If the specified configuration does not exist and `allow_lazy_load` is `False`.
        :return: The requested configuration.
        :rtype: ConfigurationItem
        """
        if config_name is None:
            config_name = DEFAULT_CONFIGURATION_NAME
        if config_name not in cls.configurations:
            if not allow_lazy_load:
                critical(f'Configuration "{config_name}" cannot be found. Lazy load is not allowed in this context.',
                         ConfigurationNotFoundError)
            config = cls.get_loader().lazy_load(config_name)
            cls.add_config(config, config_name)
        return cls.configurations[config_name]

    @classmethod
    def get_loader(cls,
                   loader_name: str = None
                   ) -> ConfigurationLoader:
        """
        Get the configuration loader instance associated with the given loader name.

        :param loader_name: A string representing the name of the configuration loader.
                            Default is 'default'.
        :type loader_name: str
        :raises ConfigurationLoaderNotFoundError: If a configuration loader with the given name is not found.
        :return: The configuration loader instance associated with the given name.
        :rtype: ConfigurationLoader
        """
        if loader_name is None:
            loader_name = DEFAULT_LOADER_NAME
        if loader_name not in cls.loaders:
            critical(f'Loader "{loader_name}" cannot be found.', ConfigurationLoaderNotFoundError)
        return cls.loaders[loader_name]

    @classmethod
    def is_configuration_loaded(cls, name: str) -> bool:
        """
        Checks if a configuration with the given name has already been loaded.

        :param name: A string representing the name of the configuration.
        :type name: str
        :return: A boolean value indicating whether the configuration is loaded.
        :rtype: bool
        """
        return name in cls.configurations

    @classmethod
    def has_loader(cls, name: str) -> bool:
        """
        Checks if a configuration loader with the given name exists in the collection.

        :param name: A string representing the name of the configuration loader.
        :type name: str
        :return: A boolean value indicating whether the configuration loader exists.
        :rtype: bool
        """
        return name in cls.loaders
