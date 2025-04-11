# llama.cpp with Vulkan Acceleration

This directory contains scripts to build and run a Docker container with llama.cpp compiled with Vulkan support for GPU acceleration.

## Prerequisites

- Docker installed and running
- GPU with Vulkan support (NVIDIA, AMD, or Intel)
- Vulkan drivers installed on your host system
- For NVIDIA GPUs: NVIDIA Container Toolkit installed

## Building the Container

### On Linux/macOS:

```bash
# Make the script executable
chmod +x build-llama-cpp.sh

# Run the build script
./build-llama-cpp.sh
```

### On Windows:

```powershell
# Run the PowerShell build script
.\build-llama-cpp.ps1
```

The build process may take several minutes to complete. It will:

1. Remove any existing llama-cpp-vulkan image
2. Build a new image with Vulkan support enabled
3. Optimize compilation using all available CPU cores
4. Tag the image as llama-cpp-vulkan:latest

## Using the Container

### On Linux/macOS:

```bash
# Make the script executable
chmod +x run-llama-cpp.sh

# Run the container with your models directory
./run-llama-cpp.sh /path/to/your/models [additional args]

# Example:
./run-llama-cpp.sh ./models --temp 0.7 --ctx-size 2048
```

### On Windows:

```powershell
# Run the PowerShell script
.\run-llama-cpp.ps1 C:\path\to\your\models [additional args]

# Example:
.\run-llama-cpp.ps1 .\models --temp 0.7 --ctx-size 2048
```

## Troubleshooting

### Build Issues

If the build keeps getting canceled, try:

1. Increase Docker resources (CPU, memory) in Docker Desktop settings
2. Run with `--no-cache` to start a fresh build
3. Consider using the Docker BuildKit frontend, which has better handling of build failures

### Runtime Issues

If you get errors about GPU access:

1. Check that Vulkan is properly installed on your host:
   ```bash
   vulkaninfo
   ```

2. For NVIDIA GPUs, verify the NVIDIA Container Toolkit is working:
   ```bash
   docker run --rm --gpus all nvidia/cuda:11.0-base nvidia-smi
   ```

3. Try running without GPU acceleration using the CPU only

## Resources

- [llama.cpp GitHub repository](https://github.com/ggml-org/llama.cpp)
- [Vulkan SDK](https://www.lunarg.com/vulkan-sdk/)
- [NVIDIA Container Toolkit](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/install-guide.html) 
