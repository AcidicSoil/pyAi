# PowerShell script for building llama-cpp-vulkan Docker image on Windows

Write-Host "===== Building llama-cpp-vulkan Docker image =====" -ForegroundColor Cyan
Write-Host "This may take several minutes..." -ForegroundColor Yellow

# Remove any old image with the same name
Write-Host "Cleaning up any existing images..." -ForegroundColor Gray
docker rmi llama-cpp-vulkan:latest 2>$null

# Build with extended timeout and resource allocations
Write-Host "Starting build process..." -ForegroundColor Green
$env:DOCKER_BUILDKIT=1
docker build `
  --progress=plain `
  --no-cache `
  --tag llama-cpp-vulkan:latest `
  --file vulkan.Dockerfile `
  --build-arg BUILDKIT_INLINE_CACHE=1 `
  .

# Check if build was successful
if ($LASTEXITCODE -eq 0) {
  Write-Host "===== Build completed successfully! =====" -ForegroundColor Green
  Write-Host "You can now run the container with:" -ForegroundColor Cyan
  Write-Host "docker run --gpus all -v C:/path/to/models:/models llama-cpp-vulkan:latest -m /models/your-model.gguf [other options]" -ForegroundColor White
} else {
  Write-Host "===== Build failed! =====" -ForegroundColor Red
  Write-Host "Please check the error messages above." -ForegroundColor Yellow
  exit 1
}
