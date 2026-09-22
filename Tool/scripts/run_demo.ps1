$ErrorActionPreference = "Stop"
$RootDir = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
$ToolPython = Join-Path $RootDir ".venv/Scripts/python.exe"
if (-not (Test-Path $ToolPython)) { $ToolPython = "python" }
& $ToolPython -m fsf_tool analyze `
  --java "$RootDir/examples/Calculator.java" `
  --fsf "$RootDir/examples/calculator_full.fsf.yaml" `
  --output "$RootDir/demo-output"
if ($LASTEXITCODE -ne 0) { throw "Analysis failed; inspect the diagnostics." }
