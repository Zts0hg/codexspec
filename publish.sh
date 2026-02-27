#!/bin/bash
# Publish codexspec to PyPI and create GitHub tag
# Usage: ./publish.sh [--test] [--skip-tag]

set -e

# Colors for output
RED='\033[0;31m'
YELLOW='\033[1;33m'
GREEN='\033[0;32m'
NC='\033[0m' # No Color

# Parse arguments
TEST_PYPI=false
SKIP_TAG=false

while [[ $# -gt 0 ]]; do
    case $1 in
        --test)
            TEST_PYPI=true
            shift
            ;;
        --skip-tag)
            SKIP_TAG=true
            shift
            ;;
        *)
            echo -e "${RED}Unknown option: $1${NC}"
            echo "Usage: ./publish.sh [--test] [--skip-tag]"
            exit 1
            ;;
    esac
done

# Extract version from pyproject.toml (portable across macOS and Linux)
VERSION=$(sed -n 's/^version = "\([^"]*\)"$/\1/p' pyproject.toml)
if [[ -z "$VERSION" ]]; then
    echo -e "${RED}Error: Could not extract version from pyproject.toml${NC}"
    exit 1
fi
echo -e "${GREEN}Version: $VERSION${NC}"

# Safety check: uncommitted changes
if ! git diff-index --quiet HEAD --; then
    echo -e "${YELLOW}Warning: You have uncommitted changes in the working directory.${NC}"
    echo -e "${YELLOW}Continuing anyway...${NC}"
fi

# Safety check: remote tag exists (only if not skipping tag)
if ! $SKIP_TAG; then
    TAG_NAME="v$VERSION"
    if git ls-remote --tags origin | grep -q "refs/tags/${TAG_NAME}$"; then
        echo -e "${RED}Error: Tag $TAG_NAME already exists on remote.${NC}"
        echo -e "${RED}Please update the version in pyproject.toml before publishing.${NC}"
        exit 1
    fi
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
    TARGET="TestPyPI"
else
    echo "Uploading to PyPI..."
    uvx twine upload dist/*
    TARGET="PyPI"
fi

# Create and push tag (only after successful upload, and not for test or skip-tag)
if ! $SKIP_TAG && ! $TEST_PYPI; then
    echo "Creating git tag $TAG_NAME..."
    git tag "$TAG_NAME"

    echo "Pushing tag to origin..."
    git push origin "$TAG_NAME"
fi

# Output completion message
echo ""
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}Publish Complete!${NC}"
echo -e "${GREEN}========================================${NC}"
echo -e "  Version:  ${GREEN}$VERSION${NC}"
echo -e "  Target:   ${GREEN}$TARGET${NC}"
if ! $SKIP_TAG && ! $TEST_PYPI; then
    echo -e "  Tag:      ${GREEN}$TAG_NAME${NC}"
    echo -e "  PyPI:     https://pypi.org/project/codexspec/$VERSION/"
elif $TEST_PYPI; then
    echo -e "  TestPyPI: https://test.pypi.org/project/codexspec/$VERSION/"
fi
echo -e "${GREEN}========================================${NC}"
