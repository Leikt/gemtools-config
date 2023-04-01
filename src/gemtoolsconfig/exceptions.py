import logging


def critical(msg: str, exception_class: type[Exception]):
    """
    Logs a critical error message and raises an exception of the specified class.

    :param msg: The error message to log and include in the exception.
    :type msg: str
    :param exception_class: The class of exception to raise.
    :type exception_class: type[Exception]
    :raises: The specified exception class with the given error message.
    """
    logging.critical(msg)
    raise exception_class(msg)


class ConfigurationNotFoundError(Exception):
    """Raised when a requested configuration cannot be found.

    This error is raised when a configuration is requested by name, but no
    configuration with that name exists in the `configurations` dictionary of the
    `Configs` class.

    """


class ConfigurationLoadingError(Exception):
    """Raised when an error occurs while loading a configuration.

    This error is raised when a configuration fails to load due to an error in
    the configuration file, or when a required configuration file is missing.

    """


class ConfigurationLoaderNotFoundError(Exception):
    """Raised when a configuration loader cannot be found.

    This error is raised when a configuration loader is requested by name, but
    no loader with that name exists in the `loaders` dictionary of the
    `Configs` class.

    """


class ConfigurationLoaderFoundError(Exception):
    """Raised when a configuration loader already exists.

    This error is raised when an attempt is made to add a configuration loader
    to the `loaders` dictionary of the `Configs` class, but a loader with the
    same name already exists and `allow_overwrite` is set to `False`.

    """


class ConfigurationHandlerError(Exception):
    """Base class for configuration handler errors.

    This exception is raised when an error occurs while handling a configuration,
    such as during validation or processing.

    """


class ArgumentError(Exception): ...
