from .configurations import Configurations
from .exceptions import ConfigurationLoaderFoundError, ConfigurationNotFoundError, ConfigurationHandlerError, \
    ArgumentError, ConfigurationLoaderNotFoundError, ConfigurationLoadingError
from .item import ConfigurationItem
from .loader import ConfigurationLoader, LoadingHandler, LazyHandler, ConfigurationLoaderBuilder
from .presets import preset_source_loader, preset_file_loader


def quick_setup(directory: str = None) -> ConfigurationItem:
    """
    Initialize Configurations in the most standard way: a "config" file (toml, ini, yml, json, yaml) in the given
    directory. It adds a file loader and load the default configuration.

    :param directory: The directory where to find the configuration files. By default, it's the working directory.
    :type directory: str
    :return: the loaded configuration
    :rtype: ConfigurationItem
    """
    if directory is None:
        Configurations.add_loader(preset_file_loader())
    else:
        Configurations.add_loader(preset_file_loader(directory))
    Configurations.get_loader().load()
    return Configurations.get_config()
