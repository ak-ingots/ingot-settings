import contextlib
import importlib
import io
import os
import pathlib
import subprocess
import sys
import tempfile
import typing as t
import unittest
from unittest import mock

import ingot_settings
from ingot_settings.yaml import YamlFileLoader, YamlFormat, YamlSettings
from ingots.defaults import Project
from ingots.defaults.settings import Settings
from ingots.defaults.settings.configs import Configs, IntConfig
from ingots.defaults.settings.loaders import (
    BaseFormat,
    FileLoader,
    IniFormat,
    JsonFormat,
)
from ingots.puer import Slot
from ingots.puer.cli import CommandRunner


class HttpConfigs(Configs):
    HTTP_PORT = IntConfig(80)


class HttpSettings(Settings):
    """The settings of another addon, with configs of its own."""

    configs = Slot(HttpConfigs)


class AppSettings(HttpSettings, YamlSettings):
    pass


class AppProject(Project):
    settings = Slot(AppSettings)


class JsoncFormat(JsonFormat):
    EXTENSIONS = frozenset({".jsonc"})


class JsoncFileLoader(FileLoader):
    """The file loader of another addon, with a format of its own."""

    jsonc_format = Slot(JsoncFormat)


class JsoncSettings(Settings):
    file_loader = Slot(JsoncFileLoader)


class PackageTestCase(unittest.TestCase):
    def test_the_package_imports_no_unit(self) -> None:
        self.assertEqual(ingot_settings.__all__, ())
        code = "import sys, ingot_settings; print('yaml' in sys.modules)"
        result = subprocess.run(
            [sys.executable, "-c", code], capture_output=True, text=True, check=True
        )
        self.assertEqual(result.stdout, "False\n")

    def test_the_yaml_unit_needs_its_extra(self) -> None:
        with mock.patch.dict(sys.modules, {"yaml": None}):  # import yaml fails
            for name in [name for name in sys.modules if "ingot_settings." in name]:
                del sys.modules[name]  # restored on exit
            with self.assertRaisesRegex(
                ImportError,
                r"^ingot_settings.yaml needs PyYAML: "
                r'pip install "ingot-settings\[yaml\]"$',
            ):
                importlib.import_module("ingot_settings.yaml")


class YamlUnitTestCase(unittest.TestCase):
    @t.override
    def setUp(self) -> None:
        self.tmp = pathlib.Path(self.enterContext(tempfile.TemporaryDirectory()))
        self.enterContext(mock.patch.dict(os.environ, clear=True))
        # the logging is not under test: keep the handlers of the test run
        self.enterContext(mock.patch("logging.config.dictConfig"))

    def test_the_file_loader_adds_yaml_to_the_formats_of_the_defaults(self) -> None:
        kind: type[BaseFormat] = BaseFormat  # type: ignore[type-abstract]
        self.assertIs(YamlSettings.file_loader.cls, YamlFileLoader)
        self.assertEqual(
            [slot.cls for _, slot in YamlFileLoader.slots_iter(kind)],
            [IniFormat, JsonFormat, YamlFormat],
        )

    def test_joined_settings_read_yaml_into_the_configs_of_another_addon(
        self,
    ) -> None:
        path = self.tmp / "configs.yaml"
        path.write_text("HTTP_PORT: 9090\nIS_PRINT_CONFIGS: off\n")
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            code = CommandRunner(
                AppProject, ["--configs-file", str(path), "settings", "list"]
            ).run()
        self.assertEqual(code, 0)
        self.assertIn("HTTP_PORT = 9090\n", out.getvalue())

    def test_joined_file_loaders_take_a_class_extending_both(self) -> None:
        with self.assertRaisesRegex(TypeError, r"BadSettings.file_loader = "):

            class BadSettings(YamlSettings, JsoncSettings):  # type: ignore[misc]
                pass

        class AppFileLoader(YamlFileLoader, JsoncFileLoader):
            pass

        class JoinedSettings(YamlSettings, JsoncSettings):
            file_loader = Slot(AppFileLoader)

        kind: type[BaseFormat] = BaseFormat  # type: ignore[type-abstract]
        self.assertEqual(
            {slot.cls for _, slot in JoinedSettings.file_loader.cls.slots_iter(kind)},
            {IniFormat, JsonFormat, YamlFormat, JsoncFormat},
        )
