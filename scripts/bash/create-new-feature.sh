#!/usr/bin/env bash
# Create a new feature branch and spec directory

set -e

# Source common utilities
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/common.sh"

# Default values
FEATURE_NAME=""
FEATURE_ID=""

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        -n|--name)
            FEATURE_NAME="$2"
            shift 2
            ;;
        -i|--id)
            FEATURE_ID="$2"
            shift 2
            ;;
        -h|--help)
            echo "Usage: $0 [OPTIONS]"
            echo ""
            echo "Options:"
            echo "  -n, --name    Feature name (e.g., 'user authentication')"
            echo "  -i, --id      Feature ID (e.g., '001')"
            echo "  -h, --help    Show this help message"
            exit 0
            ;;
        *)
            log_error "Unknown option: $1"
            exit 1
            ;;
    esac
done

# Validate inputs
if [ -z "$FEATURE_NAME" ]; then
    log_error "Feature name is required. Use -n or --name."
    exit 1
fi

# Check if we're in a CodexSpec project
require_codexspec_project

# Generate feature ID if not provided
if [ -z "$FEATURE_ID" ]; then
    # Find the next available ID
    SPECS_DIR=$(get_specs_dir)
    if [ -d "$SPECS_DIR" ]; then
        LAST_ID=$(ls -1 "$SPECS_DIR" 2>/dev/null | grep -E '^[0-9]+' | sort -n | tail -1 | cut -d'-' -f1)
        if [ -n "$LAST_ID" ]; then
            FEATURE_ID=$(printf "%03d" $((10#$LAST_ID + 1)))
        else
            FEATURE_ID="001"
        fi
    else
        FEATURE_ID="001"
    fi
fi

# Generate branch name
BRANCH_NAME="${FEATURE_ID}-$(echo "$FEATURE_NAME" | tr '[:upper:]' '[:lower:]' | tr ' ' '-' | tr -cd 'a-z0-9-')"

log_info "Creating feature: $FEATURE_NAME"
log_info "Feature ID: $FEATURE_ID"
log_info "Branch name: $BRANCH_NAME"

# Create feature directory
SPECS_DIR=$(get_specs_dir)
FEATURE_DIR="$SPECS_DIR/$BRANCH_NAME"
mkdir -p "$FEATURE_DIR"
log_success "Created feature directory: $FEATURE_DIR"

# Create initial spec file
cat > "$FEATURE_DIR/spec.md" << 'EOF'
# Feature: [Feature Name]

## Overview
[High-level description of the feature]

## Goals
- [Goal 1]
- [Goal 2]

## User Stories
[To be defined]

## Functional Requirements
[To be defined]

## Non-Functional Requirements
[To be defined]
EOF

log_success "Created initial spec file: $FEATURE_DIR/spec.md"

# Create git branch if git is available
if command_exists git && git rev-parse --git-dir >/dev/null 2>&1; then
    git checkout -b "$BRANCH_NAME" 2>/dev/null || {
        log_warning "Could not create git branch. It may already exist."
    }
    log_success "Created git branch: $BRANCH_NAME"
fi

log_success "Feature created successfully!"
echo ""
echo "Next steps:"
echo "  1. Edit the spec file: $FEATURE_DIR/spec.md"
echo "  2. Use /codexspec.specify to refine the specification"
