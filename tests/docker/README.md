# Docker validation

## Distribution package

Place the release ZIP and its SHA-256 file in `dist/`, then run:

```powershell
docker pull python:3.10-slim
docker pull python:3.13-slim
./scripts/test-docker.ps1
```

The test uses the version declared in the portable manifest. A locally generated ZIP can also be tested, but testing the published artifact requires downloading the files attached to that release.

Checks include eight unit tests, package generation, SHA-256 verification, extraction, equality of every file in the supplied and rebuilt ZIPs, and success/failure cases for the extracted CLI. ZIP metadata or compression differences can produce different archive hashes on Windows and Linux even when their file contents match.

The source mount is read-only, scratch storage is temporary, and runtime networking is disabled. Pulling images requires network access.

## Rust runtime fixture

`ToolkitSmoke.cs` is test code authored in this repository. It is not included in the distributed plugin ZIP. It logs `TOOLKIT_CONFIG_OK multiplier=2` when the supplied JSON setting is loaded, and `TOOLKIT_SERVER_INITIALIZED` when the server initialization hook runs. An unexpected configuration value causes initialization to fail.

Use separate Linux/amd64 Rust test servers for each framework. Place the C# file in the framework's plugins directory and the JSON file in `oxide/config` or `carbon/configs`, respectively. Do not deploy the fixture to a production server.

The local `rustfix-*` images used for this evaluation are not distributed with this repository. Reproduction requires an isolated server environment with equivalent builds. Exact environment details and results are recorded in `docs/DOCKER-VALIDATION.md`.

This checks framework compilation, loading, and configuration reads. It does not evaluate Codex's natural-language repair decisions, all third-party plugins, or player interactions.
