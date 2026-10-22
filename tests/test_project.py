import contextlib
import io
import os
import pathlib
import tempfile
import typing as t
import unittest
from unittest import mock

import ingot_settings
from ingot_settings.__main__ import main
from ingots.defaults import Project as DefaultsProject
from ingots.defaults.settings.loaders import BaseFormat, IniFormat, JsonFormat
from ingots.puer.cli import CommandRunner


class ProjectTestCase(unittest.TestCase):
    @t.override
    def setUp(self) -> None:
        self.tmp = pathlib.Path(self.enterContext(tempfile.TemporaryDirectory()))
        self.enterContext(mock.patch.dict(os.environ, clear=True))
        # the logging is not under test: keep the handlers of the test run
        self.enterContext(mock.patch("logging.config.dictConfig"))

    def run_project(self, *argv: str) -> tuple[int, str]:
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            code = CommandRunner(ingot_settings.Project, argv).run()
        return code, out.getvalue()

    def test_the_project_extends_the_defaults(self) -> None:
        self.assertTrue(issubclass(ingot_settings.Project, DefaultsProject))
        self.assertIs(ingot_settings.Project.settings.cls, ingot_settings.Settings)
        self.assertIs(
            ingot_settings.Settings.file_loader.cls, ingot_settings.FileLoader
        )

    def test_the_file_loader_keeps_the_formats_of_the_defaults(self) -> None:
        kind: type[BaseFormat] = BaseFormat  # type: ignore[type-abstract]
        self.assertEqual(
            [slot.cls for _, slot in ingot_settings.FileLoader.slots_iter(kind)],
            [IniFormat, JsonFormat],
        )

    def test_a_file_is_loaded_through_the_addon(self) -> None:
        path = self.tmp / "configs.json"
        path.write_text('{"IS_STRICT_CONFIGS": true}')
        code, out = self.run_project(
            "--configs-file",
            str(path),
            "--config",
            "IS_PRINT_CONFIGS=off",
            "settings",
            "list",
        )
        self.assertEqual(code, 0)
        self.assertIn("IS_STRICT_CONFIGS = True\n", out)

    def test_the_addon_runs_on_its_own(self) -> None:
        os.environ["INGOT_IS_PRINT_CONFIGS"] = "off"
        argv = ["ingot_settings", "settings", "list"]
        with (
            mock.patch("sys.argv", argv),
            contextlib.redirect_stdout(io.StringIO()) as out,
            self.assertRaises(SystemExit) as exit,
        ):
            main()
        self.assertEqual(exit.exception.code, 0)
        self.assertIn("IS_STRICT_CONFIGS", out.getvalue())
