"""
YAML files as a source of overrides, on PyYAML: the ``yaml`` extra,
``pip install "ingot-settings[yaml]"``. Importing the unit needs the extra.
"""

__all__ = ("YamlFileLoader", "YamlFormat", "YamlSettingsUnit")

from ingots.defaults.settings import SettingsUnit
from ingots.puer import Slot

from .loaders import YamlFileLoader, YamlFormat


class YamlSettingsUnit(SettingsUnit):
    """
    The settings of the defaults reading ``--configs-file`` in YAML too,
    through :class:`YamlFileLoader`. An application joins them with the
    settings of its other addons:
    ``class AppSettingsUnit(HttpSettingsUnit, YamlSettingsUnit)``.
    """

    file_loader = Slot(YamlFileLoader)
