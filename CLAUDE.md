# CLAUDE.md

Guidance for Claude Code in this repository. Keep it under 200 lines and do not
repeat what README or the ADRs say: link to them.

## What this is

`ingot-settings`: an addon of [Ingots](https://github.com/ak-ingots/ingots)
with sources and formats for the settings of `ingots.defaults` beyond the
standard library. So far the skeleton, laid out as `ingots.defaults`, a unit
in the `__init__.py` of its package: `SettingsProject` (`project.py`) takes
the addon's `SourcesSettings` (`settings/`), whose `SettingsFileLoader`
(`settings/loaders/files.py`) will hold the formats as slots; YAML files come
in 0.2.0, on PyYAML. `python -m ingot_settings` runs the addon on its own
(prefix `INGOT`). Every integration sits behind an extra of its own and lives
in its own module, the only one importing its dependency; the package imports
none of them. A library (ADR 0003), Python >= 3.14, part of
the [ak-ingots](https://github.com/ak-ingots) ecosystem; the meta repository
`ingots-libs` holds the ecosystem-wide decisions in `docs/adr/`.

## Commands

Everything goes through `make` (run `make` alone for the target list); uv
provides the environments and interpreters.

```bash
make check        # what CI runs: lint, test, coverage, wheel-test, cl-check
make lint         # black --check, flake8, mypy --strict
make test         # unittest on the working tree
make coverage     # the same under coverage; fails below 99%
make wheel-test   # unittest on the built wheel, PYTHONS="3.14 3.15"
make format       # black
```

One test: `uv run python -m unittest tests.test_canary.CanaryTestCase`.

## Commits and GitHub

- Never commit, amend, push, open a pull request, tag or rewrite history on
  your own initiative: show a summary and the proposed message, wait for an
  explicit approval of that commit. One approval does not extend to the
  next. Never merge a pull request: the user does (`gh pr merge` is denied).
- The remote is `ak-ingots/ingot-settings`. Inside the `ingots-libs`
  checkout, run gh and git network commands as
  `direnv exec /home/bee/work/ingots-libs <cmd>` (the token comes from its
  `.envrc`; never read it).
- `main` and `release/X.Y` are protected by a ruleset: no direct push, force
  push or deletion; pull requests only, squash-merged, with every CI job
  green on a branch up to date with `main`. One change per branch and PR,
  kept to one commit; the squash commit takes the PR title and description,
  so write them as the commit message. The `Co-Authored-By` trailer goes in
  the branch commit only: GitHub carries it to the end of the squash commit.
- Before pushing a branch, rebase it onto the current `main` and run
  `make check`. After the user merges, switch to `main`, pull and delete the
  local branch.
- A release: a pull request sets the version (`uv version X.Y.Z`) and
  collates the changelog (`make cl-build VERSION=X.Y.Z`); after the merge,
  the tag `vX.Y.Z` on its commit starts the `release` workflow, which
  publishes to TestPyPI, then to PyPI once the user approves the `pypi`
  environment. Run by hand, the workflow rehearses on TestPyPI only.

## Rules

- Every change users should know about adds a fragment to `changelog.d/`
  (`<issue>.<type>.md` or `+<slug>.<type>.md`, see `changelog.d/README.md`);
  `cl-check` fails CI without one.
- The version is static in `pyproject.toml` (`uv_build`, no setuptools-scm);
  it changes only at release time.
- `ingots` is pinned to a minor version (`>=0.30.1,<0.31`): before 1.0 a minor
  version of the framework may break its addons. Moving on to the next one
  is a change of its own, with a news fragment.
- Flat layout: the package is `ingot_settings/` at the root. The wheel must be
  complete: `make wheel-test` imports the package only from the wheel.
- Tests are stdlib `unittest`, no pytest. Code passes `mypy --strict` with
  `explicit-override`: every override takes `@t.override`; black at 88
  columns.
- The supported interpreters are listed in three places with nothing linking
  them: `PYTHONS` in the Makefile, the classifiers and the `wheel` matrix in
  `.github/workflows/ci.yml`. Change them together.
- CI runs exactly the `make` targets; a new check goes into `make check` and
  `ci.yml` together.
- A class takes the prefix of the addon, `Settings`, so that an application
  imports it under its own name, and inherits the class of the defaults
  without an alias. The settings unit, which the prefix would double,
  takes what the addon brings to it: `SourcesSettings`.
- Code layout and naming follow ADR 0007; the PUER rules of `ingots` apply to
  an addon too: hooks start with an underscore and are overridden, not
  called; a protected member is touched only by its class, its subclasses
  and its own package.

## Design

An addon extends the framework through slots and subclassing (ADR 0004) and
ships contract tests that its consumers run (ADR 0005); design principles in
ADR 0006. The settings it extends are documented in `ingots`:
`docs/defaults/settings.md` and `docs/defaults/addon.md`.
