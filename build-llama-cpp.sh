#!/bin/bash
# Build script for llama-cpp-vulkan Docker image

# Set error handling
set -e

echo "===== Building llama-cpp-vulkan Docker image ====="
echo "This may take several minutes..."

# Remove any old image with the same name
echo "Cleaning up any existing images..."
docker rmi llama-cpp-vulkan:latest 2>/dev/null || true

# Build with extended timeout and resource allocations
echo "Starting build process..."
DOCKER_BUILDKIT=1 docker build \
  --progress=plain \
  --no-cache \
  --tag llama-cpp-vulkan:latest \
  --file vulkan.Dockerfile \
  --build-arg BUILDKIT_INLINE_CACHE=1 \
  .

# Check if build was successful
if [ $? -eq 0 ]; then
  echo "===== Build completed successfully! ====="
  echo "You can now run the container with:"
  echo "docker run --gpus all -v /path/to/models:/models llama-cpp-vulkan:latest -m /models/your-model.gguf [other options]"
else
  echo "===== Build failed! ====="
  echo "Please check the error messages above."
  exit 1
fi
