#!/bin/bash

# Create a local directory if it doesn't exist
mkdir -p ./local_docs

# We've already created the continue-llms.txt file in the local_docs directory
# If you need to modify it, edit ./local_docs/continue-llms.txt directly

uvx --from mcpdoc mcpdoc \
    --yaml config.yaml \
    --allowed-domains langchain-ai.github.io langchain.com cline.bot augmentcode.com continue-llms.txt sourcegraph.com \
    --transport sse \
    --port 8082 \
    --host localhost &

npx @modelcontextprotocol/inspector
