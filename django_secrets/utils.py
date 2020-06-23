import inspect
import os

try:
    from typing import Iterable
except ImportError:
    from collections import Iterable


class SettingKeyNotExists(Exception):
    def __init__(self, names):
        self.names = names

    def __str__(self):
        return "SettingKeyNotExists ({names})".format(names=", ".join(self.names))


def setting(
    available_names,
    default=None,
    settings_module=None,
    lookup_env=True,
    raise_exception=False,
):
    """
    Helper function to get a Django setting by name. If setting doesn't exists
    it will return a default.
    """
    if settings_module is None:
        stack = inspect.stack()
        frame = stack[3][0]
        settings_module = inspect.getmodule(frame)

    if isinstance(available_names, str) or not isinstance(available_names, Iterable):
        available_names = [available_names]

    for name in available_names:
        value = getattr(settings_module, name, None)
        if value is not None:
            return value

    if lookup_env:
        for name in available_names:
            value = os.environ.get(name)
            if value is not None:
                return value

    if raise_exception:
        raise SettingKeyNotExists(available_names)

    return default
