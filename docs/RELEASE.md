# Releases

## 0.1.0-alpha.2

- English documentation, listing metadata, starter prompts, and release notes for international distribution.
- Reproducible Docker test commands for the JSON helper and distribution package.
- An isolated C# fixture for Oxide/Carbon compilation, loading, and configuration checks.
- See [Docker validation](DOCKER-VALIDATION.md) for measured results and limitations.

## 0.1.0-alpha.1

- Initial server setup, C# repair, and configuration skills.
- Read-only JSON validation and structural comparison helper.
- MIT license, Codex compatibility manifest, and portable manifest.
- At the time of release, live Rust runtime evaluation had not been performed.

### Initial validation on 2026-09-15

- Eight JSON helper tests passed on Windows/Python 3.13.
- Official `validate_plugin.py` and all three `quick_validate.py` checks passed.
- Local Codex marketplace registration and plugin installation succeeded.
- ZIP integrity, inventory, and SHA-256 generation passed.
- GitHub Actions passed on Windows/Linux with Python 3.10 and 3.13.

## Distribution artifacts

Run `python scripts/package.py` to create an allowlisted ZIP and SHA-256 file in `dist/`. Plugin manifests and skills are at the ZIP root. GitHub distributes the source; the ZIP supports package inspection and submission preparation. Raw logs, credentials, and third-party binaries are excluded.

## Before a stable release

1. Execute and record the scenarios in `EVALUATION.md`.
2. Evaluate actual repair tasks and gameplay behavior on both frameworks.
3. Test skill selection in fresh Codex tasks after installation.
4. Prepare verified publisher details, contact information, and listing material for public directory submission.

## Public plugin directory

A GitHub Release and an OpenAI public plugin directory listing are separate distribution steps. Skills-only plugins can be submitted, but submission permissions, verified publisher identity, and review are required. This project has not been submitted or approved for that directory.

Sources checked on 2026-09-15: [Package your plugin](https://developers.openai.com/plugins/build/plugins), [Submit plugins](https://developers.openai.com/plugins/deploy/submission). Recheck the requirements before submitting.
