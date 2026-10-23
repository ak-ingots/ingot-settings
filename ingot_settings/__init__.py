"""
ingot-settings: sources and formats for the settings of ``ingots.defaults``
beyond the standard library. An application inherits from
:class:`SettingsProject`, or joins the settings unit of the addon,
:class:`~ingot_settings.settings.SourcesSettings`, with those of its other
addons.
"""

__all__ = ("SettingsProject",)

from .project import SettingsProject
