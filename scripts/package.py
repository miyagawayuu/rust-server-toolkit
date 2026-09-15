#!/usr/bin/env python3
"""Build an allowlisted plugin ZIP with an adjacent SHA-256 checksum."""

import hashlib
import json
from pathlib import Path
import zipfile

ROOT = Path(__file__).resolve().parents[1]
PLUGIN = ROOT / "plugins/rust-server-toolkit"
FILES = [
    ".codex-plugin/plugin.json",
    "plugin.json",
    "skills/rust-server-setup/SKILL.md",
    "skills/rust-server-setup/references/operations.md",
    "skills/rust-plugin-repair/SKILL.md",
    "skills/rust-plugin-config/SKILL.md",
    "skills/rust-plugin-config/scripts/config_check.py",
]


def main():
    manifest = json.loads((PLUGIN / "plugin.json").read_text(encoding="utf-8"))
    legacy = json.loads((PLUGIN / ".codex-plugin/plugin.json").read_text(encoding="utf-8"))
    for field in ("name", "version", "description", "author", "repository", "license", "keywords"):
        if manifest[field] != legacy[field]:
            raise ValueError(f"Manifest mismatch: {field}")
    sources = [(PLUGIN / name, name) for name in FILES]
    sources += [(ROOT / name, name) for name in ("LICENSE", "PRIVACY.md")]
    # Read all expected inputs before creating the archive. No broad directory
    # scan: credentials, logs, fixtures, and caches cannot enter accidentally.
    contents = [(name, path.read_text(encoding="utf-8").encode("utf-8")) for path, name in sources]
    out = ROOT / "dist"
    out.mkdir(exist_ok=True)
    archive = out / f"{manifest['name']}-{manifest['version']}.zip"
    with zipfile.ZipFile(archive, "w", compression=zipfile.ZIP_DEFLATED) as package:
        for name, content in contents:
            info = zipfile.ZipInfo(name, date_time=(2026, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            package.writestr(info, content)
    with zipfile.ZipFile(archive) as package:
        if package.testzip() is not None:
            raise ValueError("Archive integrity check failed")
        if set(package.namelist()) != {name for name, _ in contents}:
            raise ValueError("Archive inventory mismatch")
    checksum = hashlib.sha256(archive.read_bytes()).hexdigest()
    archive.with_suffix(".zip.sha256").write_text(f"{checksum}  {archive.name}\n", encoding="utf-8")
    print(f"Built {archive.name}: {len(contents)} files; SHA-256 {checksum}")


if __name__ == "__main__":
    main()
