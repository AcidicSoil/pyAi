#!/bin/bash
# Script to run llama-cpp-vulkan container

# Check if model path was provided
if [ $# -lt 1 ]; then
  echo "Usage: $0 path/to/models [additional llama.cpp options]"
  echo "Example: $0 ./models --temp 0.7 --ctx-size 2048"
  exit 1
fi

# Get the models directory
MODELS_DIR="$1"
shift

# Make sure the models directory exists
if [ ! -d "$MODELS_DIR" ]; then
  echo "Error: Models directory $MODELS_DIR does not exist."
  exit 1
fi

MODELS_DIR=$(realpath "$MODELS_DIR")
echo "Using models from: $MODELS_DIR"

# Detect GPU availability and set appropriate flags
echo "Testing GPU availability..."
if command -v nvidia-smi &> /dev/null; then
  echo "NVIDIA GPU detected, using --gpus all flag"
  GPU_FLAG="--gpus all"
elif command -v vulkaninfo &> /dev/null; then
  echo "Vulkan compatible GPU detected, mounting device"
  GPU_FLAG="--device=/dev/dri:/dev/dri"
else
  echo "Warning: No GPU detected, performance will be limited to CPU only"
  GPU_FLAG=""
fi

# Run the container
echo "Starting llama-cpp-vulkan container..."
docker run --rm -it \
  $GPU_FLAG \
  -v "$MODELS_DIR":/models \
  llama-cpp-vulkan:latest \
  -m /models \
  "$@"

# Check exit code
if [ $? -ne 0 ]; then
  echo "Container execution failed. Please check the error messages above."
  exit 1
fi
