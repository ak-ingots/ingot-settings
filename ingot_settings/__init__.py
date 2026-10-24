"""
ingot-settings: sources and formats for the settings of ``ingots.defaults``
beyond the standard library, each a unit behind an extra of its own. An
application installs the extra and joins the unit's settings with its own:
``pip install "ingot-settings[yaml]"``, then
``class AppSettings(HttpSettings, YamlSettings)`` with
``from ingot_settings.yaml import YamlSettings``. The package itself imports
none of them.
"""

__all__ = ()
