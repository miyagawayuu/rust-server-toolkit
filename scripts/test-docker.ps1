param(
    [string[]]$Images = @('python:3.10-slim', 'python:3.13-slim')
)
$ErrorActionPreference = 'Stop'
$repoPath = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
foreach ($pythonImage in $Images) {
    & docker run --rm --network none --read-only --cap-drop ALL `
        --security-opt no-new-privileges --cpus 2 --memory 512m --pids-limit 128 `
        --tmpfs /tmp:rw,nosuid,nodev,size=128m `
        --mount "type=bind,source=$repoPath,target=/source,readonly" `
        $pythonImage python /source/tests/docker/package_smoke.py
    if ($LASTEXITCODE -ne 0) { throw "Docker verification failed: $pythonImage" }
}
