#!/bin/bash
# Publish codexspec to PyPI and create GitHub tag
# Usage: ./publish.sh [--test] [--skip-tag] [--auto-bump] [--skip-marketplace]

set -e

# Colors for output
RED='\033[0;31m'
YELLOW='\033[1;33m'
GREEN='\033[0;32m'
NC='\033[0m' # No Color

# Parse arguments
TEST_PYPI=false
SKIP_TAG=false
AUTO_BUMP=false
SKIP_MARKETPLACE=false

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
        --auto-bump)
            AUTO_BUMP=true
            shift
            ;;
        --skip-marketplace)
            SKIP_MARKETPLACE=true
            shift
            ;;
        *)
            echo -e "${RED}Unknown option: $1${NC}"
            echo "Usage: ./publish.sh [--test] [--skip-tag] [--auto-bump] [--skip-marketplace]"
            exit 1
            ;;
    esac
done

# Function to bump patch version
bump_patch_version() {
    local version=$1
    local major minor patch
    IFS='.' read -r major minor patch <<< "$version"
    patch=$((patch + 1))
    echo "${major}.${minor}.${patch}"
}

# Function to update marketplace.json with new version
update_marketplace() {
    local version=$1
    local tag_name="v$version"
    local marketplace_file=".claude-plugin/marketplace.json"

    echo -e "${YELLOW}Updating marketplace.json to $tag_name...${NC}"

    # Check if marketplace.json exists
    if [[ ! -f "$marketplace_file" ]]; then
        echo -e "${YELLOW}Warning: $marketplace_file not found. Skipping marketplace update.${NC}"
        return 0
    fi

    # Validate JSON format
    if ! python -m json.tool "$marketplace_file" > /dev/null 2>&1; then
        echo -e "${RED}Error: $marketplace_file contains invalid JSON.${NC}"
        return 1
    fi

    # Update ref and version in marketplace.json (portable across macOS and Linux)
    # Update the "ref" field
    sed -i.bak "s/\"ref\": \"v[^\"]*\"/\"ref\": \"$tag_name\"/" "$marketplace_file"
    rm -f "${marketplace_file}.bak"

    # Update the "version" field in plugins array
    sed -i.bak "s/\"version\": \"[^\"]*\"/\"version\": \"$version\"/" "$marketplace_file"
    rm -f "${marketplace_file}.bak"

    # Verify the update was successful
    if grep -q "\"ref\": \"$tag_name\"" "$marketplace_file"; then
        echo -e "${GREEN}✓ marketplace.json updated to $tag_name${NC}"
    else
        echo -e "${RED}Error: Failed to update marketplace.json${NC}"
        return 1
    fi

    return 0
}

# Function to commit and push marketplace changes
commit_marketplace_changes() {
    local version=$1
    local marketplace_file=".claude-plugin/marketplace.json"

    if [[ ! -f "$marketplace_file" ]]; then
        return 0
    fi

    # Check if there are changes to commit
    if git diff --quiet "$marketplace_file" 2>/dev/null; then
        echo -e "${YELLOW}No changes to marketplace.json${NC}"
        return 0
    fi

    echo -e "${YELLOW}Committing marketplace.json changes...${NC}"

    git add "$marketplace_file"
    git commit -m "chore: update marketplace.json to v$version"

    echo -e "${YELLOW}Pushing marketplace.json to origin...${NC}"
    git push origin HEAD

    echo -e "${GREEN}✓ marketplace.json committed and pushed${NC}"
}

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
        if $AUTO_BUMP; then
            # Auto-bump the patch version
            NEW_VERSION=$(bump_patch_version "$VERSION")
            echo -e "${YELLOW}Tag $TAG_NAME already exists on remote.${NC}"
            echo -e "${YELLOW}Auto-bumping version: $VERSION -> $NEW_VERSION${NC}"

            # Update pyproject.toml with new version (portable across macOS and Linux)
            sed -i.bak "s/^version = \"${VERSION}\"/version = \"${NEW_VERSION}\"/" pyproject.toml
            rm -f pyproject.toml.bak

            # Update variables
            VERSION="$NEW_VERSION"
            TAG_NAME="v$VERSION"
            echo -e "${GREEN}Version updated to: $VERSION${NC}"
        else
            echo -e "${RED}Error: Tag $TAG_NAME already exists on remote.${NC}"
            echo -e "${RED}Please update the version in pyproject.toml before publishing.${NC}"
            echo -e "${RED}Or use --auto-bump to automatically bump the patch version.${NC}"
            exit 1
        fi
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

    # Update marketplace.json after tag is created and pushed
    if ! $SKIP_MARKETPLACE; then
        if update_marketplace "$VERSION"; then
            commit_marketplace_changes "$VERSION"
        fi
    else
        echo -e "${YELLOW}Skipping marketplace update (--skip-marketplace)${NC}"
    fi
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
    if ! $SKIP_MARKETPLACE; then
        echo -e "  Plugin:   ${GREEN}marketplace.json updated${NC}"
    fi
elif $TEST_PYPI; then
    echo -e "  TestPyPI: https://test.pypi.org/project/codexspec/$VERSION/"
fi
echo -e "${GREEN}========================================${NC}"
