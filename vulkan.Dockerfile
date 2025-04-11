FROM ubuntu:22.04

# Install dependencies
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    lsb-release \
    software-properties-common \
    cmake \
    build-essential \
    git \
    libcurl4-openssl-dev

# Install Vulkan
RUN apt-get update && apt-get install -y \
    libvulkan1 \
    libvulkan-dev \
    vulkan-tools \
    mesa-vulkan-drivers

# Set environment variables for build
ENV MAKEFLAGS="-j$(nproc)"

# Clone and build llama.cpp (using a specific stable version tag)
WORKDIR /app
RUN git clone https://github.com/ggml-org/llama.cpp .
# Checkout a stable release tag instead of using main branch
RUN git checkout b4985
# Use CUDA if available (will be ignored if not)
RUN cmake -B build -DGGML_VULKAN=1 -DCMAKE_BUILD_TYPE=Release
# Build using multiple cores with more verbose output
RUN cmake --build build --config Release -- -j$(nproc) VERBOSE=1

# Set proper permissions for the built binaries
RUN chmod +x /app/build/bin/llama-cli

ENTRYPOINT ["/app/build/bin/llama-cli"]
