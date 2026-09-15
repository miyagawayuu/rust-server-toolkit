# Operational decisions

Primary sources (recheck when using):

- [Facepunch server setup](https://wiki.facepunch.com/rust/Creating-a-server)
- [Oxide server setup](https://docs.oxidemod.com/guides/owners/setup-server)
- [Oxide installation](https://docs.oxidemod.com/guides/owners/install-oxide)
- [Carbon documentation](https://carbonmod.gg/)

## Fresh installation

Determine OS/architecture, available disk/memory, hosting method, public versus private access, and desired framework. Reuse an existing hosting panel/container lifecycle when present. Use a dedicated unprivileged account for a self-managed installation.

Rust Dedicated Server uses SteamCMD app ID `258550`. Use an absolute install directory and set `force_install_dir` before login. Example for an already-installed SteamCMD on Linux, after choosing the actual path:

```sh
./steamcmd.sh +force_install_dir /srv/rust +login anonymous +app_update 258550 validate +quit
```

This command downloads/changes server files; do not run it as a diagnostic on an active installation. Do not change a selected release branch implicitly. Inspect downloaded framework archive layout before extraction to avoid duplicated `RustDedicated_Data` nesting. Get the package matching OS, architecture, and server branch from its official project.

Choose an identity and explicit non-conflicting game/query/RCON ports from the actual configuration. Establish which need UDP/TCP from current server docs. Restrict RCON to an administrator path. Check host and provider firewalls plus container port mappings; never open every port to troubleshoot.

## Existing server update

Record current Rust build and framework/plugin versions. Save and stop through the actual service or panel in the authorized maintenance window. Verify process exit. Back up the selected identity directory and framework configuration, permissions, plugin sources and persistent data, plus startup files. Retain compatible prior binaries if binary rollback is required. Verify the backup can be read and list the intended restore paths.

Update Rust first, then install/reinstall the selected compatible framework as required. Test startup, framework version, representative plugins, and client join. A save written by a newer build may require restoring the old save with old binaries; a binary-only rollback is not necessarily sufficient.

## Connectivity diagnosis

Compare listener bindings, process state, port configuration, container forwarding, local firewall, provider firewall, and client route in that order. UDP timeouts are inconclusive without server-side evidence. Separate game join from server-list query and RCON connectivity. Use a real client for the join gate; a listening socket alone does not establish playability. Never disable Steam authentication or anti-cheat to conceal a networking problem.
