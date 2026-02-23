#!/bin/bash
# Publish codexspec to PyPI
# Usage: ./publish.sh [--test]

set -e

# Parse arguments
TEST_PYPI=false
if [[ "$1" == "--test" ]]; then
    TEST_PYPI=true
fi

# Clean dist directory
echo "Cleaning dist directory..."
rm -rf dist

# Build package
echo "Building package..."
uv build

# Upload to PyPI
if $TEST_PYPI; then
    echo "Uploading to TestPyPI..."
    uvx twine upload --repository testpypi dist/*
else
    echo "Uploading to PyPI..."
    uvx twine upload dist/*
fi

echo "Done!"
