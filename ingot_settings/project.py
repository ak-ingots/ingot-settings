"""The project of the addon: what an application inherits from."""

__all__ = ("SettingsProject",)

from ingots.defaults import Project
from ingots.puer import Slot

from .settings import SourcesSettings


class SettingsProject(Project):
    """
    The project of the defaults with the addon's :class:`SourcesSettings`.
    An application inherits from it and sets its own ``env_configs_prefix``;
    the addon run on its own (``python -m ingot_settings``) keeps the prefix
    of the defaults, ``INGOT``.
    """

    settings = Slot(SourcesSettings)
