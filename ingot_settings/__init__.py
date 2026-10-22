"""
ingot-settings: sources and formats for the settings of ``ingots.defaults``
beyond the standard library. An application inherits from :class:`Project`,
or joins :class:`Settings` with the settings of its other addons.
"""

__all__ = ("FileLoader", "Project", "Settings")

from .loaders import FileLoader
from .project import Project
from .settings import Settings
