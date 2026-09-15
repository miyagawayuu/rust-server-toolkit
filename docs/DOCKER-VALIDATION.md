# Docker validation — 2026-09-15

## Scope

Docker Desktop 4.82.0, Docker Engine 29.6.1, Linux/amd64 on a Windows x86-64 host. These checks cover the packaged JSON helper and a small C# runtime fixture. They do not establish the correctness of every Codex-generated repair or a production deployment.

## Package checks

Both Python images passed eight unit tests, ZIP generation, checksum verification, equality of extracted file contents against a rebuilt package, and success/failure checks of the extracted CLI.

| Environment | Result |
| --- | --- |
| Python 3.10.21, Linux/amd64 | Passed |
| Python 3.13.15, Linux/amd64 | Passed |

Image digests:

- `python:3.10-slim`: `sha256:fd76ade0c607f27677bc04be3c60749f400eedc941d9e72967e19a4cedff80c2`
- `python:3.13-slim`: `sha256:9d2e5553305c7c7b0097999bb17187c69b921ccd6bc9d40e4bb5ebe652c00285`

The published alpha.1 package and the English alpha.2 candidate were tested. Alpha.2 candidate SHA-256: `53d65f7f9d844d4fdc552c55b14e2b81401ad783ab6a9bfa416d565802a07228`.

## Rust runtime checks

The fixture in `tests/docker/ToolkitSmoke.cs` is original test code. Both tests use separate containers, no host ports, no external network, dropped Linux capabilities, `no-new-privileges`, four CPUs, 10 GiB memory, and a 512-process limit. Only fixture inputs and private output directories are mounted.

The cached server build is **25230300**. These are cached-build tests, not a verification of the latest available Rust or framework versions. The existing offline harness disables server authentication/encryption for the isolated test; authenticated client connections and gameplay are not tested.

### Oxide

- Image: `rustfix-oxide:25230300-556956307-033a51e54954`
- Image ID: `sha256:d4e098b9cf84daeaef23918ffae290e2a0fe0f8642bd7e72c1ce79c09b3bef32`
- Framework log: Rust extension `2.0.7716`; Unity extension `2.0.3777`.
- Compilation: passed (`ToolkitSmoke was compiled successfully`).
- Initial load: passed (`Loaded plugin ToolkitSmoke v0.1.0`).
- Configuration read: passed (`TOOLKIT_CONFIG_OK multiplier=2`).
- Server initialization hook: observed (`TOOLKIT_SERVER_INITIALIZED` and `Server startup complete`).
- Harness result: `startup_seen=true`, `timed_out=true`, `server_exit=0`, duration 365 seconds. Startup occurred late enough that the 360-second deadline ended the post-start observation window. This is not an unqualified full-runtime pass.
- Offline map-upload/DNS errors and headless rendering warnings occurred. They did not prevent fixture compilation or initialization.

### Carbon

- Image: `rustfix-carbon:25230300-547241271-033a51e54954`
- Image ID: `sha256:a8337f244f6e494d95e6e9d9a2bd706bcf3225905aa122f5a2efeaceecf71025`
- Framework asset ID: `547241271`, cached artifact timestamp `2026-09-06T13:42:20Z`.
- Compilation/load: passed (`Loaded plugin ToolkitSmoke v0.1.0 by miyagawayuu [1088ms]`). Successful loading establishes compilation for this source fixture; no separate compiler-success line was required.
- Configuration read: passed (`TOOLKIT_CONFIG_OK multiplier=2`).
- Server initialization hook: observed (`TOOLKIT_SERVER_INITIALIZED` and `Server startup complete`).
- Harness result: `startup_seen=true`, `timed_out=true`, `server_exit=0`, duration 364 seconds. As with Oxide, the deadline ended the post-start observation window. Longer-term runtime stability was not established.
- Offline map-upload/DNS errors and headless rendering warnings occurred.

### Interpretation

The fixture compiled/loaded and read the expected setting on both cached frameworks, and both initialization hooks ran. Both harness runs reached their time limits, so the report does not label either run an unrestricted runtime pass. No live player or production server was involved.

## Remaining evaluation

- Real clients, authentication, game actions, persistence across restarts, and live reload behavior.
- Fresh server installation and updates through hosting panels.
- Third-party plugin repairs and framework API migration scenarios.
- Skill selection and complete natural-language workflows in fresh Codex tasks.

Raw server logs remain local under `.docker-validation/` and are excluded from Git and release packages. Reproduction instructions are in [Docker tests](../tests/docker/README.md).
