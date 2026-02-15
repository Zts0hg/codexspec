#!/usr/bin/env bash
# Check prerequisites for CodexSpec development

set -e

# Source common utilities
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/common.sh"

log_info "Checking prerequisites for CodexSpec..."

# Check Python
if command_exists python3; then
    PYTHON_VERSION=$(python3 --version 2>&1 | cut -d' ' -f2)
    log_success "Python 3 installed: $PYTHON_VERSION"
else
    log_error "Python 3 is not installed"
    exit 1
fi

# Check uv
if command_exists uv; then
    UV_VERSION=$(uv --version 2>&1)
    log_success "uv installed: $UV_VERSION"
else
    log_warning "uv is not installed. Recommended for package management."
    echo "  Install with: curl -LsSf https://astral.sh/uv/install.sh | sh"
fi

# Check git
if command_exists git; then
    GIT_VERSION=$(git --version 2>&1 | cut -d' ' -f3)
    log_success "Git installed: $GIT_VERSION"
else
    log_warning "Git is not installed. Recommended for version control."
fi

# Check Claude Code
if command_exists claude; then
    log_success "Claude Code CLI is installed"
else
    log_warning "Claude Code CLI is not installed"
    echo "  Install from: https://claude.ai/code"
fi

# Check if in a CodexSpec project
if is_codexspec_project; then
    log_success "Currently in a CodexSpec project"
else
    log_info "Not currently in a CodexSpec project"
    echo "  Run 'codexspec init' to initialize a new project"
fi

echo ""
log_success "Prerequisite check complete!"
