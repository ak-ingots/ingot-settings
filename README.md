# ingot-settings

[![ci](https://github.com/ak-ingots/ingot-settings/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/ak-ingots/ingot-settings/actions/workflows/ci.yml)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/ak-ingots/ingot-settings/blob/main/LICENSE)

<!-- Links must be absolute: this README also renders on PyPI. -->

Sources and formats for the settings of
[Ingots](https://github.com/ak-ingots/ingots) beyond the standard library: an
addon extending the settings unit of `ingots.defaults`. First YAML files, then
loaders for cloud secret managers. Every integration sits behind an extra of
its own, so an application installs only what it uses:
`pip install "ingot-settings[yaml]"`.

```python
import ingot_settings


class AppProject(ingot_settings.Project):
    env_configs_prefix = "APP"
```

An application with other addons joins the settings instead:
`class AppSettings(HttpSettings, ingot_settings.Settings)`, and declares
`settings = Slot(AppSettings)` in its project.

**Status:** pre-alpha. 0.1.0 is the skeleton of the addon: its project, its
settings and their file loader, with the formats of the defaults (INI, JSON);
YAML comes in 0.2.0.

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
