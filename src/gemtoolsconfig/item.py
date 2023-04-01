from types import MappingProxyType
from typing import Any

ConfigurationItem = MappingProxyType


def freeze_configuration(obj: Any) -> ConfigurationItem:
    """
    Freeze a configuration object by recursively converting its dictionary and list attributes
    into immutable `MappingProxyType` objects.

    :param obj: The configuration object to freeze.
    :type obj: Any
    :return: The frozen configuration object.
    :rtype: Any
    """
    if isinstance(obj, dict):
        item = {}
        for key, value in obj.items():
            item[key] = freeze_configuration(value)
        return MappingProxyType(item)

    elif isinstance(obj, list):
        item = {}
        for i, value in enumerate(obj):
            item[str(i)] = freeze_configuration(value)
        return MappingProxyType(item)

    return obj
