#!/bin/bash

# Screenshot utility script for stocks-dashboard
# Usage: ./take-screenshots.sh [output-dir] [url]
# If no arguments provided, takes screenshots of all pages
# If url provided, takes screenshot of that specific URL

set -e

OUTPUT_DIR="${1:-./screenshots}"
TARGET_URL="${2:-}"

echo "🔍 Stocks Dashboard Screenshot Utility"
echo "Output directory: $OUTPUT_DIR"

# Function to check if a service is running
check_service() {
    local url="$1"
    local service_name="$2"
    
    if curl -s --fail "$url" > /dev/null 2>&1; then
        echo "✅ $service_name is running"
        return 0
    else
        echo "❌ $service_name is not running"
        return 1
    fi
}

# Function to wait for service to be ready
wait_for_service() {
    local url="$1"
    local service_name="$2"
    local max_attempts=30
    local attempt=1
    
    echo "⏳ Waiting for $service_name to be ready..."
    
    while [ $attempt -le $max_attempts ]; do
        if curl -s --fail "$url" > /dev/null 2>&1; then
            echo "✅ $service_name is ready!"
            return 0
        fi
        
        echo "⏳ Attempt $attempt/$max_attempts - $service_name not ready yet..."
        sleep 2
        ((attempt++))
    done
    
    echo "❌ $service_name failed to start after $max_attempts attempts"
    return 1
}

# Check if development environment is running
echo "🔍 Checking if services are running..."

FRONTEND_RUNNING=false
BACKEND_RUNNING=false

if check_service "http://localhost:8085" "Frontend"; then
    FRONTEND_RUNNING=true
fi

if check_service "http://localhost:5000/health" "Backend" || check_service "http://localhost:5000" "Backend"; then
    BACKEND_RUNNING=true
fi

# Start services if not running
if [ "$FRONTEND_RUNNING" = false ] || [ "$BACKEND_RUNNING" = false ]; then
    echo "🚀 Starting development environment..."
    echo "⚠️  Note: In a normal setup, this would run 'just dev-docker'"
    echo "⚠️  For this demo, please ensure the development environment is running manually"
    echo "⚠️  Run: docker compose -f dev/docker-compose.yml -f dev/docker-compose.dev.yml up -d --build"
    
    # In a real environment with 'just' available, this would be:
    # just dev-docker > /dev/null 2>&1 &
    # wait_for_service "http://localhost:8085" "Frontend"
    # wait_for_service "http://localhost:5000" "Backend"
    
    echo "⚠️  Proceeding with screenshot attempt (services may not be ready)"
else
    echo "✅ All services are running!"
fi

# Ensure we have the necessary dependencies
if [ ! -d "node_modules" ]; then
    echo "📦 Installing Playwright dependencies..."
    cd tests && npm install && cd ..
fi

# Create output directory
mkdir -p "$OUTPUT_DIR"

echo "📸 Taking screenshots..."

# Run the TypeScript screenshot utility
if [ -n "$TARGET_URL" ]; then
    echo "📸 Taking screenshot of: $TARGET_URL"
    cd tests && npx tsx ../screenshot-utility.ts "$OUTPUT_DIR" "$TARGET_URL"
else
    echo "📸 Taking screenshots of all pages..."
    cd tests && npx tsx ../screenshot-utility.ts "$OUTPUT_DIR"
fi

echo "🎉 Screenshots completed!"
echo "📁 Screenshots saved in: $OUTPUT_DIR"

# List the screenshots taken
if [ -d "$OUTPUT_DIR" ]; then
    echo "📸 Screenshots taken:"
    ls -la "$OUTPUT_DIR"/*.png 2>/dev/null || echo "No PNG files found in $OUTPUT_DIR"
fi