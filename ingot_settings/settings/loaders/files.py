"""The file loader of the defaults with the formats of the addon."""

__all__ = ("SettingsFileLoader",)

from ingots.defaults.settings.loaders import FileLoader


class SettingsFileLoader(FileLoader):
    """
    The file loader of the defaults with the formats of the addon, each a
    slot of its own: ``yaml_format = Slot(YamlFormat)`` for ``.yaml`` files.
    None yet: the formats of the defaults, INI and JSON.
    """
