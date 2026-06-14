#!/usr/bin/env bash
# Create a new feature branch and spec directory

set -e

# Source common utilities
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/common.sh"

# Default values
FEATURE_NAME=""

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        -n|--name)
            FEATURE_NAME="$2"
            shift 2
            ;;
        -h|--help)
            echo "Usage: $0 [OPTIONS]"
            echo ""
            echo "Options:"
            echo "  -n, --name    Feature name (e.g., 'user authentication')"
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

# Normalize the path/branch suffix to the supported ASCII kebab-case contract.
FEATURE_SUFFIX=$(printf "%s" "$FEATURE_NAME" |
    tr '[:upper:]' '[:lower:]' |
    sed 's/[^a-z0-9]/-/g; s/-\{1,\}/-/g; s/^-//; s/-$//')
if [ -z "$FEATURE_SUFFIX" ]; then
    log_error "Feature short name must contain ASCII letters or numbers (for example, 'user-auth')."
    exit 1
fi

TIMESTAMP=$(date +"%Y-%m%d-%H%M")
RANDOM_SUFFIX=$(LC_ALL=C tr -dc 'a-z0-9' </dev/urandom | head -c 2)
FEATURE_ID="${TIMESTAMP}${RANDOM_SUFFIX}"

# Generate branch name
BRANCH_NAME="${FEATURE_ID}-${FEATURE_SUFFIX}"

log_info "Creating feature: $FEATURE_NAME"
log_info "Feature ID: $FEATURE_ID"
log_info "Branch name: $BRANCH_NAME"

# Create feature directory
SPECS_DIR=$(get_specs_dir)
FEATURE_DIR="$SPECS_DIR/$BRANCH_NAME"
mkdir -p "$FEATURE_DIR"
log_success "Created feature directory: $FEATURE_DIR"

# Create the authoritative requirements record. spec.md is generated later.
REQUIREMENTS_TEMPLATE=".codexspec/templates/docs/requirements-template.md"
REQUIREMENTS_FILE="$FEATURE_DIR/requirements.md"
if [ -f "$REQUIREMENTS_TEMPLATE" ]; then
    sed \
        -e "s/\[FEATURE NAME\]/$FEATURE_SUFFIX/g" \
        -e "s/\[feature-id\]/$FEATURE_ID/g" \
        "$REQUIREMENTS_TEMPLATE" > "$REQUIREMENTS_FILE"
else
    cat > "$REQUIREMENTS_FILE" << 'EOF'
# Confirmed Requirements: __FEATURE_NAME__

**Feature ID**: `__FEATURE_ID__`
**Status**: Discovery
**Last Confirmed**: [DATE]

Only entries with `Status: confirmed` are binding downstream inputs.

## Needs

### NEED-001
- **Status**: open
- **Statement**: [Confirm with the user]
- **User Evidence**: "[Add a short quote or paraphrase after confirmation]"

## Constraints

### CON-001
- **Status**: open

## Decisions

### DEC-001
- **Status**: open

## Out of Scope

### OUT-001
- **Status**: open

## Open Questions

### OPEN-001
- **Status**: open

## Superseded Entries

<!-- Keep replaced entries with Status: superseded. -->
EOF
    sed \
        -e "s/__FEATURE_NAME__/$FEATURE_SUFFIX/g" \
        -e "s/__FEATURE_ID__/$FEATURE_ID/g" \
        "$REQUIREMENTS_FILE" > "$REQUIREMENTS_FILE.tmp"
    mv "$REQUIREMENTS_FILE.tmp" "$REQUIREMENTS_FILE"
fi

log_success "Created requirements record: $REQUIREMENTS_FILE"

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
echo "  1. Use /codexspec:specify to discuss the requirement"
echo "  2. Confirm the requirements record: $REQUIREMENTS_FILE"
echo "  3. Use /codexspec:generate-spec after confirmation"
