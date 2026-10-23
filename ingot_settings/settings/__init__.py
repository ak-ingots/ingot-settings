"""The settings unit of the defaults with the sources of the addon."""

__all__ = ("SourcesSettings",)

from ingots.defaults.settings import Settings
from ingots.puer import Slot

from .loaders import SettingsFileLoader


class SourcesSettings(Settings):
    """
    The settings unit, loading files through the addon's
    :class:`SettingsFileLoader`.
    """

    file_loader = Slot(SettingsFileLoader)
