#!/usr/bin/env bash
# Check development prerequisites or resolve SDD workflow artifact paths.

set -e

# Source common utilities
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/common.sh"

JSON=false
PATHS_ONLY=false
REQUIRE_TASKS=false
INCLUDE_TASKS=false
FEATURE_ARG=""
WORKFLOW_MODE=false

while [[ $# -gt 0 ]]; do
    case "$1" in
        --json)
            JSON=true
            WORKFLOW_MODE=true
            shift
            ;;
        --paths-only)
            PATHS_ONLY=true
            WORKFLOW_MODE=true
            shift
            ;;
        --require-tasks)
            REQUIRE_TASKS=true
            WORKFLOW_MODE=true
            shift
            ;;
        --include-tasks)
            INCLUDE_TASKS=true
            WORKFLOW_MODE=true
            shift
            ;;
        --feature)
            FEATURE_ARG="$2"
            WORKFLOW_MODE=true
            shift 2
            ;;
        -h|--help)
            cat <<'EOF'
Usage: check-prerequisites.sh [OPTIONS]

With no options, checks the local development environment.

Workflow options:
  --json             Output JSON
  --paths-only       Resolve artifact paths without requiring plan/tasks
  --require-tasks    Require tasks.md
  --include-tasks    Include tasks.md in AVAILABLE_DOCS
  --feature PATH|ID  Resolve an explicit feature directory or ID
EOF
            exit 0
            ;;
        *)
            log_error "Unknown option: $1"
            exit 1
            ;;
    esac
done

resolve_feature_dir() {
    local specs_dir
    specs_dir=$(get_specs_dir)

    if [ -n "$FEATURE_ARG" ]; then
        if [ -d "$FEATURE_ARG" ]; then
            local explicit_dir
            explicit_dir=$(cd "$FEATURE_ARG" && pwd -P)
            if ! is_feature_name "$(basename "$explicit_dir")"; then
                log_error "Invalid feature directory name: $FEATURE_ARG"
                return 1
            fi
            printf "%s\n" "$explicit_dir"
            return
        fi
        if [ -f "$FEATURE_ARG" ]; then
            local artifact_dir
            artifact_dir=$(cd "$(dirname "$FEATURE_ARG")" && pwd -P)
            if ! is_feature_name "$(basename "$artifact_dir")"; then
                log_error "Invalid feature directory name: $artifact_dir"
                return 1
            fi
            printf "%s\n" "$artifact_dir"
            return
        fi
        if [ -d "$specs_dir/$FEATURE_ARG" ]; then
            if ! is_feature_name "$FEATURE_ARG"; then
                log_error "Invalid feature directory name: $FEATURE_ARG"
                return 1
            fi
            (cd "$specs_dir/$FEATURE_ARG" && pwd -P)
            return
        fi

        if ! is_feature_id "$FEATURE_ARG"; then
            log_error "Invalid feature ID: $FEATURE_ARG"
            return 1
        fi

        # A short ID is only a local lookup convenience. The full directory
        # name identifies the workspace, and ambiguity must be explicit.
        local id_matches=()
        local candidate
        if [ -d "$specs_dir" ]; then
            for candidate in "$specs_dir"/*; do
                [ -d "$candidate" ] || continue
                if is_feature_name "$(basename "$candidate")" &&
                    [[ "$(basename "$candidate")" == "$FEATURE_ARG"-* ]]; then
                    id_matches+=("$candidate")
                fi
            done
        fi
        if [ "${#id_matches[@]}" -eq 1 ]; then
            (cd "${id_matches[0]}" && pwd -P)
            return
        fi
        if [ "${#id_matches[@]}" -gt 1 ]; then
            log_error "Multiple feature directories match ID '$FEATURE_ARG'. Pass a full directory or artifact path."
            return 1
        fi

        log_error "Feature directory not found: $FEATURE_ARG"
        return 1
    fi

    local feature_id
    feature_id=$(get_feature_id)
    if [ -n "$feature_id" ] && [ -d "$specs_dir/$feature_id" ]; then
        (cd "$specs_dir/$feature_id" && pwd -P)
        return
    fi

    local candidates=()
    if [ -d "$specs_dir" ]; then
        while IFS= read -r candidate; do
            if is_feature_name "$(basename "$candidate")"; then
                candidates+=("$candidate")
            fi
        done < <(find "$specs_dir" -mindepth 1 -maxdepth 1 -type d | sort)
    fi

    if [ "${#candidates[@]}" -eq 1 ]; then
        (cd "${candidates[0]}" && pwd -P)
        return
    fi

    if [ "${#candidates[@]}" -gt 1 ]; then
        log_error "Multiple feature directories found. Pass --feature explicitly."
    else
        log_error "No feature directory found. Run /codexspec:specify first."
    fi
    return 1
}

if [ "$WORKFLOW_MODE" = true ]; then
    require_codexspec_project

    REPO_ROOT=$(git rev-parse --show-toplevel 2>/dev/null || pwd -P)
    if ! FEATURE_DIR=$(resolve_feature_dir); then
        printf "%s\n" "$FEATURE_DIR"
        exit 1
    fi
    BRANCH=$(git branch --show-current 2>/dev/null || true)
    REQUIREMENTS="$FEATURE_DIR/requirements.md"
    FEATURE_SPEC="$FEATURE_DIR/spec.md"
    IMPL_PLAN="$FEATURE_DIR/plan.md"
    TASKS="$FEATURE_DIR/tasks.md"

    if [ "$PATHS_ONLY" = false ]; then
        if [ ! -f "$IMPL_PLAN" ]; then
            log_error "plan.md not found in $FEATURE_DIR"
            exit 1
        fi
        if [ "$REQUIRE_TASKS" = true ] && [ ! -f "$TASKS" ]; then
            log_error "tasks.md not found in $FEATURE_DIR"
            exit 1
        fi
    fi

    AVAILABLE_DOCS=()
    [ -f "$REQUIREMENTS" ] && AVAILABLE_DOCS+=("requirements.md")
    [ -f "$FEATURE_SPEC" ] && AVAILABLE_DOCS+=("spec.md")
    [ -f "$IMPL_PLAN" ] && AVAILABLE_DOCS+=("plan.md")
    if [ "$INCLUDE_TASKS" = true ] && [ -f "$TASKS" ]; then
        AVAILABLE_DOCS+=("tasks.md")
    fi

    if [ "$JSON" = true ]; then
        python3 -c '
import json
import sys

keys = (
    "REPO_ROOT",
    "BRANCH",
    "FEATURE_DIR",
    "REQUIREMENTS",
    "FEATURE_SPEC",
    "IMPL_PLAN",
    "TASKS",
)
values = sys.argv[1:8]
payload = dict(zip(keys, values))
payload["AVAILABLE_DOCS"] = sys.argv[8:]
print(json.dumps(payload, separators=(",", ":")))
' "$REPO_ROOT" "$BRANCH" "$FEATURE_DIR" "$REQUIREMENTS" "$FEATURE_SPEC" "$IMPL_PLAN" "$TASKS" "${AVAILABLE_DOCS[@]}"
    else
        echo "REPO_ROOT: $REPO_ROOT"
        echo "BRANCH: $BRANCH"
        echo "FEATURE_DIR: $FEATURE_DIR"
        echo "REQUIREMENTS: $REQUIREMENTS"
        echo "FEATURE_SPEC: $FEATURE_SPEC"
        echo "IMPL_PLAN: $IMPL_PLAN"
        echo "TASKS: $TASKS"
        echo "AVAILABLE_DOCS: ${AVAILABLE_DOCS[*]}"
    fi
    exit 0
fi

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
