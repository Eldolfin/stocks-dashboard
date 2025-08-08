#!/bin/bash

# Demo Video Generation Script
# This script runs the comprehensive E2E test and prepares assets for demo video creation

set -e

echo "🎬 Starting Demo Video Generation Process"
echo "========================================"

# Check if we're in the tests directory
if [ ! -f "playwright.config.ts" ]; then
    echo "❌ Error: This script must be run from the tests directory"
    echo "Usage: cd tests && ./generate-demo.sh"
    exit 1
fi

# Check if the server is running
echo "🔍 Checking if development server is running..."
if ! curl -s -f http://localhost:8085 > /dev/null; then
    echo "⚠️  Development server not detected at localhost:8085"
    echo "Please start the development environment first:"
    echo "  cd ../dev && docker compose -f docker-compose.yml -f docker-compose.dev.yml up -d"
    echo ""
    echo "Or use the just command:"
    echo "  just dev-docker"
    exit 1
fi

echo "✅ Development server is running"

# Clean up previous screenshots
echo "🧹 Cleaning up previous test screenshots..."
rm -rf tests/comprehensive-walkthrough.spec.ts-snapshots/
mkdir -p tests/comprehensive-walkthrough.spec.ts-snapshots/

# Run the comprehensive test
echo "🧪 Running comprehensive feature walkthrough test..."
echo "This will take a few minutes to complete..."

# Run test with video recording enabled
npx playwright test comprehensive-walkthrough.spec.ts \
    --reporter=html \
    --timeout=120000 \
    --project=chromium

# Check if test completed successfully
if [ $? -eq 0 ]; then
    echo "✅ Comprehensive test completed successfully!"
    
    echo ""
    echo "📸 Generated Screenshots:"
    echo "========================"
    find tests/comprehensive-walkthrough.spec.ts-snapshots/ -name "*.png" | sort | while read -r file; do
        echo "  📷 $(basename "$file")"
    done
    
    echo ""
    echo "📊 Test Report:"
    echo "==============="
    echo "Open the test report: playwright-report/index.html"
    
    echo ""
    echo "🎥 Demo Video Creation:"
    echo "======================"
    echo "1. Screenshots are available in: tests/comprehensive-walkthrough.spec.ts-snapshots/"
    echo "2. Use these screenshots as a storyboard for video creation"
    echo "3. To record actual interactions, run:"
    echo "   npx playwright test comprehensive-walkthrough.spec.ts --ui"
    echo "4. For video recording, add --video=on to capture browser interactions"
    
    echo ""
    echo "🚀 Demo generation completed successfully!"
    
else
    echo "❌ Test failed. Check the output above for details."
    echo "Common issues:"
    echo "  - Development server not running properly"
    echo "  - Network connectivity issues"
    echo "  - Test data files missing"
    echo ""
    echo "Try running with --ui for debugging:"
    echo "  npx playwright test comprehensive-walkthrough.spec.ts --ui"
    exit 1
fi