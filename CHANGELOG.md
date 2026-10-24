# ingot-settings Changelog

<!-- towncrier release notes start -->

## [0.2.0] - 2026-10-24
### Added
- Added YAML files, the unit `ingot_settings.yaml` behind the `yaml` extra (`pip install "ingot-settings[yaml]"`, on PyYAML): `YamlSettings`, joined with an application's settings, read `--configs-file` in `.yaml` and `.yml` too, a mapping of config names to values. The base loader resolves no types: a scalar is a string its config converts, as from an environment variable; a tag, a key given twice and an alias of anything but a scalar are errors. Importing the unit without the extra fails, naming it.

### Changed
- Moved on to ingots 0.31 (`>=0.31.0,<0.32`): joined settings must list the loaders of all their bases, and the formats of a file loader may not share an extension.

### Removed
- Removed `Project`, `Settings`, `FileLoader` and `python -m ingot_settings`: nothing is wired in by default any more, an application joins the units of the extras it installed with its own settings.

## [0.1.0] - 2026-10-22
### Added
- Started ingot-settings, an addon of Ingots for the sources and formats of the settings beyond the standard library, for `ingots` 0.30.1 and later 0.30 releases. Its skeleton: `Project`, the project of the defaults with the addon's `Settings`, whose `FileLoader` will take the addon's formats as slots, with those of the defaults for now (INI, JSON); `python -m ingot_settings` runs it on its own. The development automation of the ecosystem comes with it: `make check` (lint, tests on the working tree and on the built wheel for every supported Python, coverage, changelog check), towncrier news fragments, and the `ci` and `release` workflows.
