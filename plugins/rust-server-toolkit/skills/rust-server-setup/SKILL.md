---
name: rust-server-setup
description: Set up, update, or diagnose Facepunch Rust Dedicated Servers on Linux, Windows, Docker, or hosting panels, including choosing Oxide or Carbon. Use for Rust game server administration, not the Rust programming language.
---

# Rust server setup

Respond in the user's language. Work from the actual host, installation directory, service or panel, server identity, and intended vanilla/Oxide/Carbon framework. Infer these from the workspace when possible; ask only for missing details that affect implementation. If remote access is absent, prepare local configuration and exact deployment instructions without claiming deployment.

## Build and update

- Inspect existing startup scripts and configuration before generating replacements. Distinguish the Rust install root from `server/<identity>` and framework directories. Directory names alone do not prove a framework is active; check startup logs/version evidence.
- Read [operations.md](references/operations.md) for setup, update, and connectivity checks. Verify current releases and platform instructions at the linked primary sources at execution time. Record versions, download URLs, and checksums of downloaded artifacts; do not claim an artifact hash proves publisher authenticity.
- For an existing server, preserve identity, saves, blueprints, permissions, plugin data, and secrets. Establish a restorable backup before updates. Do not change seed/world size as an incidental fix.
- Prepare service/startup files locally and check syntax for the actual shell. Keep credentials out of source control and command output. Respect the host's existing secret storage.
- Treat Oxide and Carbon as alternative framework installations. Do not overlay both in the same live server. Test framework migrations in a separate copy with matching data.
- A setup request authorizes the necessary setup work; use existing authorization. Before an unrequested live restart, wipe, framework migration, or firewall exposure, present the exact effect and obtain authorization. Do all read-only diagnosis and candidate preparation first.

## Completion

Separate generated files, deployed changes, startup success, framework load, and real client connection. Check each only when evidence exists. For updates, show rollback commands and note whether rollback was exercised. If startup fails, inspect the first causal error and stop repeating the same failed operation without new evidence.
