"""The settings of the defaults with the sources of the addon."""

__all__ = ("Settings",)

from ingots.defaults.settings import Settings as BaseSettings
from ingots.puer import Slot

from .loaders import FileLoader


class Settings(BaseSettings):
    """The settings unit, loading files through the addon's :class:`FileLoader`."""

    file_loader = Slot(FileLoader)
