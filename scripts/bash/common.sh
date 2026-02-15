#!/usr/bin/env bash
# Common utilities for CodexSpec scripts

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Logging functions
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Get the current feature ID from git branch or SPECIFY_FEATURE env var
get_feature_id() {
    if [ -n "$SPECIFY_FEATURE" ]; then
        echo "$SPECIFY_FEATURE"
        return
    fi

    # Try to get from git branch
    if command_exists git && git rev-parse --git-dir >/dev/null 2>&1; then
        local branch
        branch=$(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo "")
        if [[ "$branch" =~ ^[0-9]+- ]]; then
            echo "$branch"
            return
        fi
    fi

    echo ""
}

# Get the specs directory
get_specs_dir() {
    local base_dir="${1:-.}"
    echo "$base_dir/.codexspec/specs"
}

# Check if we're in a CodexSpec project
is_codexspec_project() {
    local dir="${1:-.}"
    [ -d "$dir/.codexspec" ]
}

# Ensure we're in a CodexSpec project
require_codexspec_project() {
    if ! is_codexspec_project; then
        log_error "Not a CodexSpec project. Run 'codexspec init' first."
        exit 1
    fi
}
