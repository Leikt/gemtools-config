from .configurations import Configurations
from .exceptions import ConfigurationLoaderFoundError, ConfigurationNotFoundError, ConfigurationHandlerError, \
    ArgumentError, ConfigurationLoaderNotFoundError, ConfigurationLoadingError
from .item import ConfigurationItem
from .loader import ConfigurationLoader, LoadingHandler, LazyHandler, ConfigurationLoaderBuilder
from .presets import preset_source_loader, preset_file_loader


def quick_setup(directory: str = '.') -> ConfigurationItem:
    Configurations.add_loader(preset_file_loader(directory))
    Configurations.get_loader().load()
    return Configurations.get_config()
