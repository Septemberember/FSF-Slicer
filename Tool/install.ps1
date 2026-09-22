$ErrorActionPreference = "Stop"
$RootDir = Split-Path -Parent $MyInvocation.MyCommand.Path
python -m venv "$RootDir/.venv"
if ($LASTEXITCODE -ne 0) { throw "Virtual environment creation failed." }
$ToolPython = Join-Path $RootDir ".venv/Scripts/python.exe"
& $ToolPython -m pip install -r "$RootDir/requirements-lock.txt"
if ($LASTEXITCODE -ne 0) { throw "Dependency installation failed." }
& $ToolPython -m pip install --no-deps "$RootDir"
if ($LASTEXITCODE -ne 0) { throw "FSF-Slicer installation failed." }
Write-Host "Installed. Run: $RootDir/.venv/Scripts/fsf-tbfv.exe doctor"
