param(
    [int]$Port = 8080
)

$ErrorActionPreference = "Stop"
$qaRoot = "C:\Users\User\Downloads\New project\Cartograph-QA"
$java = "C:\Program Files\Microsoft\jdk-21.0.12.101-hotspot\bin\java.exe"
$ci = Join-Path $qaRoot "ci\jenkins"
$jenkinsHome = Join-Path $qaRoot ".jenkins-home"
$war = Join-Path $ci "jenkins.war"
$manager = Join-Path $ci "jenkins-plugin-manager.jar"
$plugins = Join-Path $ci "plugins.txt"

New-Item -ItemType Directory -Force -Path $ci, $jenkinsHome, (Join-Path $jenkinsHome "init.groovy.d") | Out-Null
Copy-Item (Join-Path $ci "init.groovy.d\*.groovy") (Join-Path $jenkinsHome "init.groovy.d") -Force

if (-not (Test-Path $java)) {
    throw "OpenJDK 21 not found at $java"
}

function Download-File($url, $dest) {
    Write-Host "Downloading $url"
    & curl.exe -L --fail --retry 5 --retry-all-errors -o $dest $url
    if ($LASTEXITCODE -ne 0 -or -not (Test-Path $dest) -or ((Get-Item $dest).Length -lt 1000)) {
        throw "Download failed: $url"
    }
}

if (-not (Test-Path $war) -or ((Get-Item $war).Length -lt 1000000)) {
    Download-File "https://get.jenkins.io/war-stable/latest/jenkins.war" $war
}
if (-not (Test-Path $manager) -or ((Get-Item $manager).Length -lt 1000)) {
    Download-File "https://github.com/jenkinsci/plugin-installation-manager-tool/releases/download/2.13.2/jenkins-plugin-manager-2.13.2.jar" $manager
}

Write-Host "Installing Jenkins plugins into $jenkinsHome ..."
& $java -jar $manager --war $war --plugin-file $plugins --plugin-download-directory (Join-Path $jenkinsHome "plugins") --latest true

$env:JENKINS_HOME = $jenkinsHome
$env:JAVA_HOME = "C:\Program Files\Microsoft\jdk-21.0.12.101-hotspot"
Write-Host "Starting Jenkins at http://localhost:$Port  (user admin / CartographQA!2026)"
Set-Location $qaRoot
& $java "-Djenkins.install.runSetupWizard=false" "-Djenkins.model.Jenkins.slaveAgentPort=-1" -jar $war --httpPort=$Port --httpListenAddress=127.0.0.1
