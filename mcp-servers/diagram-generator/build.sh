#!/bin/bash
# Build the diagram-generator Docker image

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "Building diagram-generator MCP server Docker image without cache..."
docker build --no-cache -t architecture-squad/diagram-generator .

echo "Docker image 'architecture-squad/diagram-generator' built successfully!"
