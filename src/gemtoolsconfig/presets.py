from os import PathLike
from pathlib import Path
from typing import Union

from .loader import ConfigurationLoader, ConfigurationLoaderBuilder
from .handlers import from_source, DEFAULT_PATH, get_file_handler, get_find_suitable_file_handler


def preset_source_loader() -> ConfigurationLoader:
    """
    Get a configuration loader that loads configuration data from a source string.

    :return: A ConfigurationLoader instance that can be used to load configuration data from a source string.
    :rtype: ConfigurationLoader
    """
    builder = ConfigurationLoaderBuilder()
    builder.add_loading_handler(from_source)
    return builder.build()


def preset_file_loader(directory: Union[PathLike, str] = DEFAULT_PATH,
                       key_file: Union[PathLike, str] = None
                       ) -> ConfigurationLoader:
    """
    Get a configuration loader that loads configuration data from a file.

    :param directory: The directory where the configuration file is located. Defaults to the current directory.
    :type directory: Union[PathLike, str]
    :param key_file: Optional path to the file containing the encryption key for encrypted configuration files.
                     Defaults to None.
    :type key_file: Union[PathLike, str], optional
    :return: A ConfigurationLoader instance that can be used to load configuration data from a file.
    :rtype: ConfigurationLoader
    :raises: NotADirectoryError if the specified directory does not exist.
    """
    key = None
    if key_file is not None:
        key = Path(key_file).read_bytes()

    builder = ConfigurationLoaderBuilder()
    builder.add_loading_handler(get_file_handler(directory, key))
    builder.add_lazy_handler(get_find_suitable_file_handler(directory))
    return builder.build()
