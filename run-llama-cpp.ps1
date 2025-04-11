# PowerShell script to run llama-cpp-vulkan container on Windows

param(
  [Parameter(Mandatory=$true, Position=0)]
  [string]$ModelsDir,

  [Parameter(ValueFromRemainingArguments=$true)]
  [string[]]$LlamaArgs
)

# Check if models directory exists
if (-not (Test-Path $ModelsDir -PathType Container)) {
  Write-Host "Error: Models directory $ModelsDir does not exist." -ForegroundColor Red
  exit 1
}

# Convert to absolute path and handle Windows paths for Docker
$ModelsDir = (Resolve-Path $ModelsDir).Path
$ModelsDir = $ModelsDir -replace '\\', '/'
$ModelsDir = $ModelsDir -replace '^([A-Za-z]):', '//$1'

Write-Host "Using models from: $ModelsDir" -ForegroundColor Cyan

# Detect GPU availability
Write-Host "Testing GPU availability..." -ForegroundColor Yellow
$gpuFlag = ""

# Check for NVIDIA GPU
try {
  $nvidiaCheck = nvidia-smi 2>$null
  if ($LASTEXITCODE -eq 0) {
    Write-Host "NVIDIA GPU detected, using --gpus all flag" -ForegroundColor Green
    $gpuFlag = "--gpus all"
  }
} catch {
  # Do nothing, just continue checking other GPU types
}

# If no NVIDIA GPU, try checking for Vulkan
if (-not $gpuFlag) {
  try {
    $vulkanCheck = vulkaninfo 2>$null
    if ($LASTEXITCODE -eq 0) {
      Write-Host "Vulkan compatible GPU detected" -ForegroundColor Green
      $gpuFlag = "--device=/dev/dri:/dev/dri"
    }
  } catch {
    # Do nothing, just continue
  }
}

# If still no GPU detected
if (-not $gpuFlag) {
  Write-Host "Warning: No GPU detected, performance will be limited to CPU only" -ForegroundColor Yellow
}

# Prepare arguments for Docker
$dockerArgs = @(
  "run",
  "--rm",
  "-it"
)

if ($gpuFlag) {
  $dockerArgs += $gpuFlag
}

$dockerArgs += @(
  "-v",
  "${ModelsDir}:/models",
  "llama-cpp-vulkan:latest",
  "-m",
  "/models"
)

if ($LlamaArgs) {
  $dockerArgs += $LlamaArgs
}

# Run the container
Write-Host "Starting llama-cpp-vulkan container..." -ForegroundColor Green
& docker $dockerArgs

# Check exit code
if ($LASTEXITCODE -ne 0) {
  Write-Host "Container execution failed. Please check the error messages above." -ForegroundColor Red
  exit 1
}
