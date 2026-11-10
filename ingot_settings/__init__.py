"""
ingot-settings: sources and formats for the settings of ``ingots.defaults``
beyond the standard library, each a unit behind an extra of its own. An
application installs the extra and joins the unit's settings with its own:
``pip install "ingot-settings[yaml]"``, then
``class AppSettingsUnit(HttpSettingsUnit, YamlSettingsUnit)`` with
``from ingot_settings.yaml import YamlSettingsUnit``. The package itself imports
none of them.
"""

__all__ = ()
