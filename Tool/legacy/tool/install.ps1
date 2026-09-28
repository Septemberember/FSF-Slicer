$ErrorActionPreference = "Stop"
$RootDir = Split-Path -Parent $MyInvocation.MyCommand.Path
python -m venv "$RootDir/.venv"
& "$RootDir/.venv/Scripts/python.exe" -m pip install --upgrade pip
& "$RootDir/.venv/Scripts/python.exe" -m pip install -e "$RootDir"
Write-Host "Installed. Run: $RootDir/.venv/Scripts/fsf-tbfv.exe doctor"
