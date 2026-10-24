# ingot-settings

[![ci](https://github.com/ak-ingots/ingot-settings/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/ak-ingots/ingot-settings/actions/workflows/ci.yml)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/ak-ingots/ingot-settings/blob/main/LICENSE)

<!-- Links must be absolute: this README also renders on PyPI. -->

Sources and formats for the settings of
[Ingots](https://github.com/ak-ingots/ingots) beyond the standard library: an
addon extending the settings unit of `ingots.defaults`. First YAML files, then
loaders for cloud secret managers. Every integration is a unit behind an
extra of its own, and nothing is wired in by default: an application installs
the extras it uses and joins their settings with its own.

```python
from ingot_settings.yaml import YamlSettings  # pip install "ingot-settings[yaml]"
from ingots.defaults import Project
from ingots.puer import Slot


class AppSettings(HttpSettings, YamlSettings):
    pass


class AppProject(Project):
    env_configs_prefix = "APP"
    settings = Slot(AppSettings)
```

Importing a unit without its extra fails at once, naming the extra.

## YAML files

`ingot_settings.yaml`, the `yaml` extra: `YamlSettings` read `--configs-file`
in YAML too (`.yaml`, `.yml`), next to INI and JSON: a mapping of config
names to values.

```yaml
HTTP_HOST: example.com
HTTP_PORT: 9090
IS_STRICT_CONFIGS: true
```

The file is read with the base loader of [PyYAML](https://pyyaml.org/),
which resolves no types: every scalar is a string, converted by its config as
an environment variable is. `NO` stays `"NO"` for a string config and is a
false for a bool one; the booleans, octals and dates of YAML 1.1 do not
apply. A sequence or a mapping reaches its config as a list or a dict, which
the config rejects unless it converts them: such an override is wrong. A tag
(`!!int`, `!!python/object`) and a key given twice are errors. An alias may
repeat a scalar, `HOST: &host db.internal` then `OTHER_HOST: *host`, but not a
sequence or a mapping, which would nest into data exponentially larger than
the file (billion laughs); the aliases together may repeat at most as many
characters as the file holds.

## Joining units

Units that extend different slots join as they are. Two that extend the same
one, such as two file loaders with formats of their own, take a class
extending both: `ingots` (and mypy) reject the settings until they declare it.

```python
class AppFileLoader(YamlFileLoader, TomlFileLoader):
    pass


class AppSettings(YamlSettings, TomlSettings):
    file_loader = Slot(AppFileLoader)
```

**Status:** pre-alpha: YAML files.

## Development

Requires [uv](https://docs.astral.sh/uv/) and `make`; uv fetches the
interpreters it needs.

```sh
make                 # the target list
make check           # everything CI runs: lint, test, coverage, wheel-test, cl-check
make format          # black
make all             # build the sdist and the wheel into dist/
```

- Every change users should know about adds a news fragment to `changelog.d/`
  (see [its README](https://github.com/ak-ingots/ingot-settings/blob/main/changelog.d/README.md)).
- A release is a pull request setting the version (`uv version X.Y.Z`) and
  collating the changelog (`make cl-build VERSION=X.Y.Z`), then the tag
  `vX.Y.Z` on `main`: the `release` workflow publishes the tested build to
  TestPyPI, then to PyPI. Run by hand, it rehearses on TestPyPI only.

## License

[Apache 2.0](https://github.com/ak-ingots/ingot-settings/blob/main/LICENSE).
