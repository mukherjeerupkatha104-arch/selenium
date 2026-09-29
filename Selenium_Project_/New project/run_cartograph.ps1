param(
    [string]$IncludeTag = "",
    [string]$Browser = "chrome",
    [string]$Environment = "qa",
    [string]$Headless = "true",
    [string]$OutputDir = "results"
)

$ErrorActionPreference = "Stop"
$projectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$qaRoot = Join-Path $projectRoot "Cartograph-QA"
$robot = Join-Path $qaRoot ".venv-local\Scripts\robot.exe"

if (-not (Test-Path $robot)) {
    throw "Local Robot environment not found at $robot. Create it with: py -3.11 -m venv `"$qaRoot\.venv-local`"; `"$qaRoot\.venv-local\Scripts\python.exe`" -m pip install -r `"$qaRoot\requirements.txt`""
}

Get-Process chromedriver -ErrorAction SilentlyContinue | Stop-Process -Force -ErrorAction SilentlyContinue

Set-Location $qaRoot
$argsList = @(
    "-d", $OutputDir,
    "-v", "BROWSER:$Browser",
    "-v", "ENVIRONMENT:$Environment",
    "-v", "HEADLESS:$Headless"
)
if ($IncludeTag) {
    $argsList += @("-i", $IncludeTag)
}
$argsList += "tests"

& $robot @argsList
exit $LASTEXITCODE
