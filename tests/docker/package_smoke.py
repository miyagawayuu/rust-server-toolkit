"""Run tests and exercise the actual release ZIP inside an isolated container."""
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import zipfile

source = Path('/source')
with tempfile.TemporaryDirectory() as temp:
    root = Path(temp)
    for name in ('plugins', 'scripts', 'tests'):
        shutil.copytree(source / name, root / name, ignore=shutil.ignore_patterns('__pycache__'))
    for name in ('LICENSE', 'PRIVACY.md'):
        shutil.copyfile(source / name, root / name)
    subprocess.run([sys.executable, '-m', 'unittest', 'discover', '-s', 'tests', '-v'], cwd=root, check=True)
    subprocess.run([sys.executable, 'scripts/package.py'], cwd=root, check=True)
    version = json.loads((source / 'plugins/rust-server-toolkit/plugin.json').read_text())['version']
    archive = source / 'dist' / ('rust-server-toolkit-' + version + '.zip')
    digest = hashlib.sha256(archive.read_bytes()).hexdigest()
    expected = archive.with_suffix('.zip.sha256').read_text().split()[0]
    assert digest == expected, 'Release checksum mismatch'
    extracted = root / 'extracted'
    with zipfile.ZipFile(archive) as package:
        assert package.testzip() is None
        with zipfile.ZipFile(root / 'dist' / archive.name) as rebuilt:
            assert set(package.namelist()) == set(rebuilt.namelist())
            for name in package.namelist():
                assert package.read(name) == rebuilt.read(name), 'Release content mismatch: ' + name
        for name in package.namelist():
            target = (extracted / name).resolve()
            assert target.is_relative_to(extracted.resolve()), 'Unsafe ZIP path'
        package.extractall(extracted)
    helper = extracted / 'skills/rust-plugin-config/scripts/config_check.py'
    old = root / 'old.json'
    new = root / 'new.json'
    old.write_text('{"Multiplier":1.0,"Unrelated":true}')
    new.write_text('{"Multiplier":2.0,"Unrelated":true}')
    for command in (['check', str(new)], ['diff', str(old), str(new)]):
        run = subprocess.run([sys.executable, str(helper), *command], capture_output=True, text=True, check=True)
        result = json.loads(run.stdout)
        assert result['valid']
        if command[0] == 'diff':
            assert result['changes'] == [{'kind':'changed', 'path':'/Multiplier'}]
    bad = root / 'bad.json'
    bad.write_text('{"Multiplier":1,"Multiplier":2}')
    run = subprocess.run([sys.executable, str(helper), 'check', str(bad)], capture_output=True, text=True)
    assert run.returncode == 2
    assert json.loads(run.stdout)['valid'] is False
    print(json.dumps({'package_smoke':'passed', 'release_sha256':digest, 'python':sys.version}))
