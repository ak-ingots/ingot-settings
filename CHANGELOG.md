# ingot-settings Changelog

<!-- towncrier release notes start -->

## [0.1.0] - 2026-10-22
### Added
- Started ingot-settings, an addon of Ingots for the sources and formats of the settings beyond the standard library, for `ingots` 0.30.1 and later 0.30 releases. Its skeleton: `Project`, the project of the defaults with the addon's `Settings`, whose `FileLoader` will take the addon's formats as slots, with those of the defaults for now (INI, JSON); `python -m ingot_settings` runs it on its own. The development automation of the ecosystem comes with it: `make check` (lint, tests on the working tree and on the built wheel for every supported Python, coverage, changelog check), towncrier news fragments, and the `ci` and `release` workflows.
