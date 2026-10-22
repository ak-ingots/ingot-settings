"""The loaders of the settings that the addon extends."""

__all__ = ("FileLoader",)

from ingots.defaults.settings.loaders import FileLoader as BaseFileLoader


class FileLoader(BaseFileLoader):
    """
    The file loader of the defaults with the formats of the addon, each a
    slot of its own: ``yaml_format = Slot(YamlFormat)`` for ``.yaml`` files.
    None yet: the formats of the defaults, INI and JSON.
    """
