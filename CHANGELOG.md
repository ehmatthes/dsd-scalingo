Changelog: dsd-<platformname>
===

0.2 - Preliminary support configuration-only deployments.

### Unreleased

#### External changes

- Added links to README, and clarified some steps.

#### Internal links

- N/A

### 0.2.2

#### External changes

- Sets `DEBUG` to `False` by default.

#### Internal changes

- N/A

### 0.2.1

#### External changes

- Checks that at least one SSH key has been uploaded to Scalingo.
- Success messages include instructions for running management commands on the remote server.
- Replace underscores with hyphens in deployed project names.

#### Internal changes

- Run unit tests with `pytest tests/plugin_unit_tests`.
- E2e tests pass on macOS and Windows for config-only and fully automated workflows.

### 0.2.0

#### External changes

- Supports configuration-only deployment, through `python manage.py deploy`.

#### Internal changes

- Adds unit tests, which are run with `pytest tests/unit_tests`.

0.1 - Preliminary support for --automate-all.
---

### 0.1.2

#### External changes

- Reports deployed URL in output and log.

#### Internal changes

- Includes dump of `scalingo help` in `developer_resources/`.
- E2e test for `--automate-all` passes on macOS.

### 0.1.1

#### External changes

- Wrote initial external messages for --automate-all deployments.
- Initial README.

#### Internal changes

- Include curated set of links to Scalingo docs in README.

### 0.1.0

#### External changes

- Initial working state. Works for one specific project using --automate-all. No platform-specific messaging, no validation.

#### Internal changes

- Initial state.
