$ErrorActionPreference = "Stop"
$qaRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$scripts = Join-Path $qaRoot ".venv-local\Scripts"
if (-not (Test-Path (Join-Path $scripts "ride.exe"))) {
    throw "RIDE is not installed in .venv-local. From Cartograph-QA run: .\.venv-local\Scripts\python.exe -m pip install robotframework-ride"
}
$env:Path = "$scripts;" + $env:Path
Set-Location $qaRoot
& (Join-Path $scripts "ride.exe")
