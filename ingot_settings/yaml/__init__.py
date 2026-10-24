"""
YAML files as a source of overrides, on PyYAML: the ``yaml`` extra,
``pip install "ingot-settings[yaml]"``. Importing the unit needs the extra.
"""

__all__ = ("YamlFileLoader", "YamlFormat", "YamlSettings")

from ingots.defaults.settings import Settings
from ingots.puer import Slot

from .loaders import YamlFileLoader, YamlFormat


class YamlSettings(Settings):
    """
    The settings of the defaults reading ``--configs-file`` in YAML too,
    through :class:`YamlFileLoader`. An application joins them with the
    settings of its other addons: ``class AppSettings(HttpSettings, YamlSettings)``.
    """

    file_loader = Slot(YamlFileLoader)
