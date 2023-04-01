from os import PathLike
from pathlib import Path
from typing import Union

from .loader import ConfigurationLoader, ConfigurationLoaderBuilder
from .handlers import from_source, DEFAULT_PATH, get_file_handler, get_find_suitable_file_handler


def source_loader() -> ConfigurationLoader:
    builder = ConfigurationLoaderBuilder()
    builder.add_loading_handler(from_source)
    return builder.build()


def file_loader(directory: Union[PathLike, str] = DEFAULT_PATH,
                key_file: Union[PathLike, str] = None
                ) -> ConfigurationLoader:
    key = None
    if key_file is not None:
        key = Path(key_file).read_bytes()

    builder = ConfigurationLoaderBuilder()
    builder.add_loading_handler(get_file_handler(directory, key))
    builder.add_lazy_handler(get_find_suitable_file_handler(directory))
    return builder.build()
