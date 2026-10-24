"""
A canary for the development pipeline: the tests are found and run, and the
package they import is the one under test - the built wheel in `make
wheel-test`, not the working tree.
"""

import importlib.metadata
import importlib.resources
import os
import unittest

import ingot_settings


class CanaryTestCase(unittest.TestCase):
    def test_the_distribution_is_installed(self) -> None:
        self.assertTrue(importlib.metadata.version("ingot-settings"))

    def test_the_package_is_typed(self) -> None:
        self.assertTrue(
            importlib.resources.files(ingot_settings).joinpath("py.typed").is_file()
        )

    @unittest.skipUnless(
        os.environ.get("INGOT_SETTINGS_WHEEL_TEST"), "not a wheel test"
    )
    def test_the_wheel_is_imported_not_the_working_tree(self) -> None:
        self.assertIn("site-packages", ingot_settings.__file__ or "")

    def test_the_framework_is_installed(self) -> None:
        self.assertTrue(importlib.metadata.version("ingots").startswith("0.31."))
