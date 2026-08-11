$ErrorActionPreference = "Stop"
$RootDir = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
python -m fsf_tool analyze `
  --java "$RootDir/examples/UserInputProgram.java" `
  --fsf "$RootDir/examples/cube_sum.fsf.yaml" `
  --output "$RootDir/demo-output"

