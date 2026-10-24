import contextlib
import io
import os
import pathlib
import tempfile
import typing as t
import unittest
from unittest import mock

from ingot_settings.yaml import YamlFormat, YamlSettings
from ingots.defaults import Project as DefaultsProject
from ingots.puer import Project, Slot
from ingots.puer.cli import CommandRunner


class YamlProject(DefaultsProject):
    settings = Slot(YamlSettings)


class YamlFormatTestCase(unittest.TestCase):
    @t.override
    def setUp(self) -> None:
        self.format = YamlFormat(Project())

    def test_a_mapping_gives_the_overrides(self) -> None:
        text = "HTTP_PORT: 9090\nHTTP_HOST: example.com\nHOSTS: [a, b]\n"
        self.assertEqual(
            self.format.parse(text),
            {"HTTP_PORT": "9090", "HTTP_HOST": "example.com", "HOSTS": ["a", "b"]},
        )

    def test_a_scalar_is_a_string(self) -> None:
        text = "A: yes\nB: NO\nC: 010\nD: 22:22\nE: 2026-10-23\nF: ~\nG: 1e3\n"
        self.assertEqual(
            self.format.parse(text),
            {
                "A": "yes",
                "B": "NO",
                "C": "010",
                "D": "22:22",
                "E": "2026-10-23",
                "F": "~",
                "G": "1e3",
            },
        )

    def test_an_alias_repeats_its_anchor(self) -> None:
        text = "A: &host db.internal\nB: *host\n"
        self.assertEqual(
            self.format.parse(text), {"A": "db.internal", "B": "db.internal"}
        )

    def test_an_alias_of_a_collection_fails(self) -> None:
        for text in [
            "A: &a [x, y]\nB: *a\n",
            "A: &a {x: y}\nB: *a\n",
            "A: &a [*a]\n",  # recursive
        ]:
            with (
                self.subTest(text),
                self.assertRaisesRegex(ValueError, "of a sequence or a mapping"),
            ):
                self.format.parse(text)

    def test_billion_laughs_fail(self) -> None:
        lines = ["A0: &a0 [x, x, x, x, x, x, x, x, x, x]"]
        lines += [
            f"A{i}: &a{i} [" + ", ".join([f"*a{i - 1}"] * 10) + "]" for i in range(1, 9)
        ]
        with self.assertRaisesRegex(ValueError, "of a sequence or a mapping"):
            self.format.parse("\n".join(lines))

    def test_the_aliases_repeat_at_most_the_text(self) -> None:
        value = "x" * 100
        self.assertEqual(
            self.format.parse(f"A: &a {value}\nB: *a\n"), {"A": value, "B": value}
        )
        with self.assertRaisesRegex(ValueError, "the aliases repeat too much"):
            self.format.parse(f"A: &a {value}\nB: [*a, *a]\n")

    def test_an_undefined_alias_fails(self) -> None:
        with self.assertRaisesRegex(ValueError, "found undefined alias"):
            self.format.parse("A: *a\n")

    def test_a_key_given_twice_fails(self) -> None:
        with self.assertRaisesRegex(ValueError, "found the key 'A' twice"):
            self.format.parse("A: 1\nB: 2\nA: 3\n")
        with self.assertRaisesRegex(ValueError, "found the key 'C' twice"):
            self.format.parse("A: {C: 1, C: 2}\n")

    def test_a_key_that_is_no_scalar_fails(self) -> None:
        with self.assertRaisesRegex(ValueError, "found unhashable key"):
            self.format.parse("? [a, b]\n: 1\n")

    def test_an_empty_file_has_no_overrides(self) -> None:
        self.assertEqual(self.format.parse(""), {})
        self.assertEqual(self.format.parse("# nothing\n"), {})

    def test_a_file_that_is_no_mapping_fails(self) -> None:
        with self.assertRaisesRegex(ValueError, "^not a YAML mapping but list$"):
            self.format.parse("- a\n- b\n")

    def test_a_file_that_is_no_yaml_fails(self) -> None:
        with self.assertRaisesRegex(ValueError, "while parsing"):
            self.format.parse("HTTP_PORT: [9090\n")

    def test_a_tag_builds_no_object(self) -> None:
        for text in [
            "X: !!python/object/apply:os.system [echo]\n",
            "X: !!int 1\n",
            "X: !local value\n",
            "X: !!str [a]\n",
        ]:
            with (
                self.subTest(text),
                self.assertRaisesRegex(ValueError, "found the tag"),
            ):
                self.format.parse(text)

    def test_a_plain_tag_is_no_tag(self) -> None:
        self.assertEqual(
            self.format.parse("X: !!str 1\nY: ! 2\n"), {"X": "1", "Y": "2"}
        )


class YamlFileTestCase(unittest.TestCase):
    @t.override
    def setUp(self) -> None:
        self.tmp = pathlib.Path(self.enterContext(tempfile.TemporaryDirectory()))
        self.enterContext(mock.patch.dict(os.environ, clear=True))
        # the logging is not under test: keep the handlers of the test run
        self.enterContext(mock.patch("logging.config.dictConfig"))

    def test_a_yaml_file_is_loaded(self) -> None:
        for name in ["configs.yaml", "configs.YML"]:
            with self.subTest(name):
                path = self.tmp / name
                path.write_text("IS_STRICT_CONFIGS: yes\nIS_PRINT_CONFIGS: off\n")
                out = io.StringIO()
                with contextlib.redirect_stdout(out):
                    code = CommandRunner(
                        YamlProject,
                        ["--configs-file", str(path), "settings", "list"],
                    ).run()
                self.assertEqual(code, 0)
                self.assertIn("IS_STRICT_CONFIGS = True\n", out.getvalue())
                self.assertIn("IS_PRINT_CONFIGS = False\n", out.getvalue())

    def test_a_value_its_config_does_not_convert_is_wrong(self) -> None:
        path = self.tmp / "configs.yaml"
        path.write_text("IS_PRINT_CONFIGS: {a: 1}\n")
        with (
            contextlib.redirect_stdout(io.StringIO()),
            self.assertLogs("ingots.defaults.settings", "WARNING") as logs,
        ):
            code = CommandRunner(
                YamlProject,
                ["--configs-file", str(path), "settings", "list"],
            ).run()
        self.assertEqual(code, 0)
        self.assertIn(
            "IS_PRINT_CONFIGS: cannot convert dict {'a': '1'}; ignored",
            logs.output[0],
        )
