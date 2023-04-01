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


def find_suitable_file(path: Path) -> Path:
    import os
    for filename in os.listdir(path.parent):
        if isinstance(filename, bytes):
            filename = filename.decode()
        if filename.split('.')[0] != path.name:
            continue
        filename = filename.removesuffix('.fer')
        return path / Path(filename)
    raise FileNotFoundError(str(path))


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
    source_text = get_argument(params, 'text')
    source_format = get_argument(params, 'format')
    params[KEY_RESULT] = load_string(source_text, source_format)
    return params


def get_file_handler(directory: Union[PathLike, str] = DEFAULT_PATH, key: bytes = None) -> LoadingHandler:
    directory = Path(directory)
    if not directory.exists():
        critical(str(directory), NotADirectoryError)

    if key is not None:
        load = partial(load_encrypted_file, key=key)
    else:
        load = load_file

    def handler(params: dict) -> dict:
        file_path = get_argument(params, 'path', DEFAULT_CONFIG_PATH)
        file_path = find_suitable_file(directory / Path(file_path))
        params['full_path'] = directory / Path(file_path)
        params[KEY_RESULT] = load(file_path)
        return params

    return handler
