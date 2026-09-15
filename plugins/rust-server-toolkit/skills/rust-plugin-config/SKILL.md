---
name: rust-plugin-config
description: Inspect and adjust Oxide or Carbon Rust game plugin JSON configuration using plugin source or version-matched documentation. Use for rates, cooldowns, permissions-related settings, malformed JSON, or configuration migrations.
---

# Rust plugin configuration

Respond in the user's language. Establish the plugin name/version, active framework, actual configuration path, and the requested gameplay result. Read plugin source or version-matched documentation to determine exact keys, units, ranges, defaults, and reload behavior. Do not invent universal keys for rates, loot, stacks, or cooldowns.

Typical paths are `oxide/config/<Plugin>.json` and `carbon/configs/<Plugin>.json`; hosts can relocate them. Verify the active path instead of creating a second copy. Distinguish plugin config from persistent `data`, localization, framework config, and permission storage.

## Prepare changes

1. Inspect JSON syntax using bundled `scripts/config_check.py` (relative to this skill). It accepts UTF-8 with or without BOM, rejects duplicate keys and non-finite numbers, and never writes input files. The check proves JSON validity only, not compatibility with the plugin.
2. Explain relevant values and units from source/docs. Change only requested keys, preserving other values and types. A config cannot replace a permission grant when plugin code requires a permission.
3. Keep the original as a private backup before replacement. Prepare a candidate file in the user's workspace. Avoid wholesale serialization when a small edit preserves formatting. Do not delete a malformed live config to force defaults unless that recovery was authorized.
4. Validate the candidate and compare with the original. `config_check.py diff` outputs change kind and JSON Pointer path only, never values; paths may still contain private names, so treat the report as private. Arrays are reported as one changed value. Review actual changed values privately before deployment.
5. Check whether unload/reload writes in-memory configuration back to disk. Where it does, unload before replacing the live file, within authorized downtime. Deploy using a same-filesystem temporary file and atomic replacement when supported; otherwise use the host's documented file workflow. Reload only the affected plugin when supported. A request for a candidate file does not authorize live reload.
6. Verify startup/reload logs and the requested gameplay behavior. If rejected, restore the backup with the same lifecycle precautions. Report candidate creation, live application, and gameplay verification separately.

## Helper

Use Python 3.10+ available on the host; do not assume `python3` exists on Windows. Resolve these paths relative to this skill, not the user's current directory.

```sh
python scripts/config_check.py check /path/to/Plugin.json
python scripts/config_check.py diff /path/to/original.json /path/to/candidate.json
```

Exit 0 means valid input (including a valid diff); exit 2 means unreadable/invalid input. Errors exclude source lines and values. The helper does not identify arbitrary secrets, validate plugin schema, edit files, connect to a server, or apply a reload.

Sources: [Oxide configuration](https://docs.oxidemod.com/guides/owners/configure-plugins), [Carbon configuration management](https://carbonmod.gg/tutorials/beginners-guide/config-management). Check current behavior when applying a change.
