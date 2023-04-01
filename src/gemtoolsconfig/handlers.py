import os
from functools import partial
from os import PathLike
from pathlib import Path
from typing import Callable, Union
from typing import Any

from gemtoolsio import load_string, load_file, load_encrypted_file

from .exceptions import critical, ArgumentError

KEY_RESULT = '__result__'

DEFAULT_PATH = '.'

DEFAULT_CONFIG_PATH = 'config.toml'

_MISSING = object()


def get_argument(kwargs: dict,
                 name: str,
                 default: Any = _MISSING,
                 choices: list[Any] = None
                 ) -> Any:
    """
    Return the value of the specified argument from a dictionary of keyword arguments.

    :param kwargs: A dictionary of keyword arguments to search for the specified argument name.
    :type kwargs: dict
    :param name: The name of the argument to retrieve.
    :type name: str
    :param default: The default value to return if the argument is not present in kwargs.
                    Defaults to _MISSING, which indicates that no default value is specified.
    :type default: Any, optional
    :param choices: A list of valid choices for the argument value. If specified and the argument
                    value is not in the list, raise an ArgumentError.
    :type choices: list[Any], optional
    :return: The value of the specified argument in kwargs, or the default value if not present.
    :rtype: Any
    :raises: ArgumentError: If the specified argument is required and not present in kwargs,
             or if the argument value is not in the list of valid choices.
    """
    value = kwargs.get(name, default)
    if value is _MISSING:
        critical(f'Missing required argument "{name}" in {kwargs}.', ArgumentError)
    if choices is not None and value not in choices:
        critical(f'Argument "{name}" must be one of {choices}, got {value}.', ArgumentError)

    return value


LoadingHandler = Callable[[dict], dict]
"""
A loading handler is a callable that takes a dictionary containing configuration data as input
and returns a dictionary containing configuration data as output. It can be used to transform or
filter configuration data during loading.

The final handler returns a dict containing the KEY_RESULT key, the value associated is the dict are
list final configuration data.
"""

LazyHandler = Callable[[dict], dict]
"""
A lazy handler is a callable that takes a dictionary containing configuration data as input
and returns a dictionary containing configuration data as output. It can be used to transform or
filter configuration data lazily, i.e. on-demand when the data is accessed for the first time.
"""


def from_source(params: dict) -> dict:
    """
    Load configuration data from a string source.

    :param params: A dictionary containing parameters for loading configuration data.
                   The dictionary must contain the following keys:
                   - 'text': The string containing the configuration data to load.
                   - 'format': The format of the configuration data.
    :type params: dict
    :return: A dictionary containing the loaded configuration data under the KEY_RESULT key.
    :rtype: dict
    """
    source_text = get_argument(params, 'text')
    source_format = get_argument(params, 'format')
    params[KEY_RESULT] = load_string(source_text, source_format)
    return params


def get_file_handler(directory: Union[PathLike, str] = DEFAULT_PATH, key: bytes = None) -> LoadingHandler:
    """
    Get a handler for loading configuration data from a file.

    :param directory: The directory where the configuration file is located. Defaults to the current directory.
    :type directory: Union[PathLike, str]
    :param key: Optional encryption key for encrypted configuration files. Defaults to None.
    :type key: bytes, optional
    :return: A callable that takes a dictionary containing parameters for loading configuration data
             from a file, and returns a dictionary containing the loaded configuration data under
             the KEY_RESULT key.
    :rtype: LoadingHandler
    :raises: NotADirectoryError if the specified directory does not exist.
    """
    directory = Path(directory)
    if not directory.exists():
        critical(str(directory), NotADirectoryError)

    if key is not None:
        load = partial(load_encrypted_file, key=key)
    else:
        load = load_file

    def handler(params: dict) -> dict:
        file_path = directory / get_argument(params, 'path', DEFAULT_CONFIG_PATH)
        params['full_path'] = file_path
        params[KEY_RESULT] = load(file_path)
        return params

    return handler


def _find_suitable_file(directory: Path, config_name: str) -> str:
    """
    Find a suitable configuration file in the specified directory.

    :param directory: The directory where the configuration files are located. Defaults to the current directory.
    :type directory: Union[PathLike, str]
    :param config_name: The name of the configuration file.
    :type config_name: str
    :return: The name of the configuration file found in the directory.
    :rtype: str
    :raises: FileNotFoundError if no suitable configuration file is found in the directory.
    """
    for filename in os.listdir(directory):
        if isinstance(filename, bytes):
            filename = filename.decode()

        if filename == config_name:
            return config_name

        if filename.split('.')[0] == config_name:
            return filename
    raise FileNotFoundError(f'Cannot find a suitable configuration file for "{config_name}" in "{str(directory)}".')


def get_find_suitable_file_handler(directory: Union[PathLike, str] = DEFAULT_PATH) -> LazyHandler:
    """
    Get a handler for finding a suitable configuration file.

    :param directory: The directory where the configuration files are located. Defaults to the current directory.
    :type directory: Union[PathLike, str]
    :return: A callable that takes a dictionary containing parameters for finding a suitable configuration file,
             and returns a dictionary containing the path of the configuration file found in the directory.
    :rtype: LazyHandler
    :raises: NotADirectoryError if the specified directory does not exist.
    """
    directory = Path(directory)
    if not directory.exists():
        critical(str(directory), NotADirectoryError)

    def handler(params: dict) -> dict:
        config_name = get_argument(params, 'name')
        params['path'] = _find_suitable_file(directory, config_name)
        return params

    return handler
