#!/usr/bin/env bash
# Resolve a deterministic, read-only review target for review-code.

set -u

SCHEMA_VERSION="1"

json_escape() {
    local value="$1"
    value=${value//\\/\\\\}
    value=${value//\"/\\\"}
    value=${value//$'\b'/\\b}
    value=${value//$'\f'/\\f}
    value=${value//$'\n'/\\n}
    value=${value//$'\r'/\\r}
    value=${value//$'\t'/\\t}
    printf '%s' "$value"
}

json_string() {
    printf '"%s"' "$(json_escape "$1")"
}

json_nullable_string() {
    if [ -n "$1" ]; then
        json_string "$1"
    else
        printf 'null'
    fi
}

emit_error() {
    local code="$1"
    local message="$2"
    local hint="$3"
    printf '{"schema_version":"%s","status":"error","error":{"code":' "$SCHEMA_VERSION"
    json_string "$code"
    printf ',"message":'
    json_string "$message"
    printf ',"hint":'
    json_string "$hint"
    printf '}}\n'
    exit 2
}

selector="default"
base_override=""
commit_input=""
parent_override=""
feature_override=""
focus_values=()

set_selector() {
    local requested="$1"
    if [ "$selector" != "default" ]; then
        emit_error "conflicting_selectors" "Review target selectors are mutually exclusive." \
            "Choose exactly one of --committed, --uncommitted, or --commit <sha>."
    fi
    selector="$requested"
}

require_option_value() {
    local option="$1"
    local remaining="$2"
    if [ "$remaining" -lt 2 ]; then
        emit_error "missing_option_value" "Missing value for $option." "Pass a value immediately after $option."
    fi
}

while [ "$#" -gt 0 ]; do
    case "$1" in
        --committed)
            set_selector "committed"
            shift
            ;;
        --uncommitted)
            set_selector "uncommitted"
            shift
            ;;
        --commit)
            require_option_value "$1" "$#"
            set_selector "commit"
            commit_input="$2"
            shift 2
            ;;
        --base)
            require_option_value "$1" "$#"
            if [ -n "$base_override" ]; then
                emit_error "duplicate_base" "--base may be supplied only once." "Remove the duplicate --base argument."
            fi
            base_override="$2"
            shift 2
            ;;
        --parent)
            require_option_value "$1" "$#"
            if [ -n "$parent_override" ]; then
                emit_error "duplicate_parent" "--parent may be supplied only once." "Remove the duplicate --parent argument."
            fi
            parent_override="$2"
            shift 2
            ;;
        --feature)
            require_option_value "$1" "$#"
            if [ -n "$feature_override" ]; then
                emit_error "duplicate_feature" "--feature may be supplied only once." "Remove the duplicate --feature argument."
            fi
            feature_override="$2"
            shift 2
            ;;
        --focus)
            require_option_value "$1" "$#"
            focus_values+=("$2")
            shift 2
            ;;
        --*)
            emit_error "unknown_argument" "Unknown review-code argument: $1" \
                "Use a documented defect target, --feature, --focus, or explicit --audit mode."
            ;;
        *)
            emit_error "bare_path_argument" "Bare path arguments are not valid defect-review targets: $1" \
                "Use review-code --audit $1 for a whole-path quality audit."
            ;;
    esac
done

if [ -n "$base_override" ] && [ "$selector" != "default" ] && [ "$selector" != "committed" ]; then
    emit_error "invalid_base_modifier" "--base is valid only for the default or --committed target." \
        "Remove --base or select the default/--committed target."
fi
if [ -n "$parent_override" ] && [ "$selector" != "commit" ]; then
    emit_error "parent_requires_commit" "--parent is valid only with --commit <sha>." \
        "Add --commit <sha> or remove --parent."
fi
if [ -n "$parent_override" ] && ! [[ "$parent_override" =~ ^[1-9][0-9]*$ ]]; then
    emit_error "invalid_parent" "--parent must be a positive integer." "Pass a valid merge-parent index such as --parent 2."
fi

if ! repo_root=$(git rev-parse --show-toplevel 2>/dev/null); then
    emit_error "not_a_git_repository" "review-code defect mode requires a Git repository." \
        "Run the command inside a Git repository or use --audit for a path audit."
fi
cd "$repo_root" || emit_error "repository_unreadable" "Cannot enter the Git repository root." "Check repository permissions."

current_branch=$(git branch --show-current 2>/dev/null || true)
head_sha=$(git rev-parse --verify HEAD 2>/dev/null || true)
if [ -z "$head_sha" ]; then
    emit_error "head_not_found" "The repository has no resolvable HEAD commit." "Create an initial commit before defect review."
fi

base_ref=""
base_sha=""
merge_base_sha=""
commit_sha=""
parent_sha=""
parent_number=""
complete_feature="false"

selected_remote() {
    local upstream remote_count
    upstream=$(git rev-parse --abbrev-ref --symbolic-full-name '@{upstream}' 2>/dev/null || true)
    if [[ "$upstream" == */* ]]; then
        printf '%s' "${upstream%%/*}"
        return
    fi
    if git remote get-url origin >/dev/null 2>&1; then
        printf 'origin'
        return
    fi
    remote_count=$(git remote 2>/dev/null | wc -l | tr -d ' ')
    if [ "$remote_count" = "1" ]; then
        git remote 2>/dev/null | head -n 1
    fi
}

resolve_base() {
    local remote candidate remote_head remote_branch fallback
    if [ -n "$base_override" ]; then
        base_ref="$base_override"
    else
        remote=$(selected_remote)
        if [ -n "$remote" ]; then
            candidate=$(git symbolic-ref --quiet --short "refs/remotes/$remote/HEAD" 2>/dev/null || true)
            if [ -n "$candidate" ] && git rev-parse --verify "${candidate}^{commit}" >/dev/null 2>&1; then
                base_ref="$candidate"
            fi
            if [ -z "$base_ref" ]; then
                remote_head=$(git ls-remote --symref "$remote" HEAD 2>/dev/null || true)
                remote_branch=$(printf '%s\n' "$remote_head" | awk '$1 == "ref:" {print $2; exit}')
                if [[ "$remote_branch" == refs/heads/* ]]; then
                    candidate="$remote/${remote_branch#refs/heads/}"
                    if git rev-parse --verify "${candidate}^{commit}" >/dev/null 2>&1; then
                        base_ref="$candidate"
                    fi
                fi
            fi
        fi
        if [ -z "$base_ref" ]; then
            for fallback in origin/main origin/master main master; do
                if git rev-parse --verify "${fallback}^{commit}" >/dev/null 2>&1; then
                    base_ref="$fallback"
                    break
                fi
            done
        fi
    fi

    if [ -z "$base_ref" ]; then
        emit_error "base_not_found" "Could not determine the repository base branch." \
            "Pass --base <branch> explicitly or configure the remote default HEAD."
    fi
    base_sha=$(git rev-parse --verify "${base_ref}^{commit}" 2>/dev/null || true)
    if [ -z "$base_sha" ]; then
        emit_error "base_not_found" "Base ref cannot be resolved: $base_ref" "Pass an existing local or remote-tracking ref."
    fi
    merge_base_sha=$(git merge-base "$head_sha" "$base_sha" 2>/dev/null || true)
    if [ -z "$merge_base_sha" ]; then
        emit_error "merge_base_not_found" "No merge base exists between HEAD and $base_ref." \
            "Pass the correct --base ref or reconcile unrelated histories."
    fi
}

inventory_paths=()
inventory_old_paths=()
inventory_statuses=()
inventory_segments=()
inventory_modes=()
inventory_kinds=()
target_segment_names=()
target_segment_from=()
target_segment_to=()

find_inventory_index() {
    local target="$1" i
    i=0
    while [ "$i" -lt "${#inventory_paths[@]}" ]; do
        if [ "${inventory_paths[$i]}" = "$target" ]; then
            printf '%s' "$i"
            return
        fi
        i=$((i + 1))
    done
    printf '%s' "-1"
}

append_segment() {
    local existing="$1" segment="$2"
    case ",$existing," in
        *",$segment,"*) printf '%s' "$existing" ;;
        ",,") printf '%s' "$segment" ;;
        *) printf '%s,%s' "$existing" "$segment" ;;
    esac
}

add_inventory_record() {
    local status="$1" path="$2" old_path="$3" segment="$4" index
    status=${status:0:1}
    index=$(find_inventory_index "$path")
    if [ "$index" -lt 0 ]; then
        inventory_paths+=("$path")
        inventory_old_paths+=("$old_path")
        inventory_statuses+=("$status")
        inventory_segments+=("$segment")
        inventory_modes+=("")
        inventory_kinds+=("")
    else
        inventory_statuses[$index]="$status"
        inventory_segments[$index]=$(append_segment "${inventory_segments[$index]}" "$segment")
        if [ -n "$old_path" ]; then
            inventory_old_paths[$index]="$old_path"
        fi
    fi
}

add_target_segment() {
    target_segment_names+=("$1")
    target_segment_from+=("$2")
    target_segment_to+=("$3")
}

collect_diff() {
    local segment="$1" status path old_path
    shift
    while IFS= read -r -d '' status; do
        old_path=""
        if [[ "$status" == R* || "$status" == C* ]]; then
            IFS= read -r -d '' old_path || true
            IFS= read -r -d '' path || true
        else
            IFS= read -r -d '' path || true
        fi
        add_inventory_record "$status" "$path" "$old_path" "$segment"
    done < <("$@" 2>/dev/null)
}

collect_untracked() {
    local path
    while IFS= read -r -d '' path; do
        add_inventory_record "A" "$path" "" "untracked"
    done < <(git ls-files --others --exclude-standard -z 2>/dev/null)
}

has_uncommitted_work() {
    if ! git diff --quiet --ignore-submodules=none -- 2>/dev/null; then
        return 0
    fi
    if ! git diff --cached --quiet --ignore-submodules=none -- 2>/dev/null; then
        return 0
    fi
    if [ -n "$(git ls-files --others --exclude-standard 2>/dev/null | head -n 1)" ]; then
        return 0
    fi
    return 1
}

collect_uncommitted_segments() {
    add_target_segment "staged" "$head_sha" "index"
    collect_diff "staged" git diff --cached --name-status -z --find-renames --
    add_target_segment "unstaged" "index" "worktree"
    collect_diff "unstaged" git diff --name-status -z --find-renames --
    add_target_segment "untracked" "none" "worktree"
    collect_untracked
}

case "$selector" in
    default)
        resolve_base
        base_branch_name=${base_ref#refs/heads/}
        base_branch_name=${base_branch_name#refs/remotes/}
        base_branch_name=${base_branch_name#*/}
        if [ -n "$current_branch" ] && [ "$current_branch" = "$base_branch_name" ]; then
            collect_uncommitted_segments
            complete_feature="false"
        else
            add_target_segment "committed" "$merge_base_sha" "$head_sha"
            collect_diff "committed" git diff --name-status -z --find-renames "$merge_base_sha" "$head_sha" --
            collect_uncommitted_segments
            complete_feature="true"
        fi
        ;;
    committed)
        resolve_base
        add_target_segment "committed" "$merge_base_sha" "$head_sha"
        collect_diff "committed" git diff --name-status -z --find-renames "$merge_base_sha" "$head_sha" --
        if has_uncommitted_work; then
            complete_feature="false"
        else
            complete_feature="true"
        fi
        ;;
    uncommitted)
        collect_uncommitted_segments
        complete_feature="false"
        ;;
    commit)
        commit_sha=$(git rev-parse --verify "${commit_input}^{commit}" 2>/dev/null || true)
        if [ -z "$commit_sha" ]; then
            emit_error "commit_not_found" "Commit cannot be resolved: $commit_input" "Pass an existing commit SHA or ref."
        fi
        commit_line=$(git rev-list --parents -n 1 "$commit_sha" 2>/dev/null || true)
        read -r -a commit_parts <<< "$commit_line"
        parent_count=$((${#commit_parts[@]} - 1))
        if [ "$parent_count" -eq 0 ]; then
            if [ -n "$parent_override" ]; then
                emit_error "invalid_parent" "Root commits have no selectable parent." "Remove --parent for a root commit."
            fi
            parent_sha=$(git hash-object -t tree --stdin </dev/null 2>/dev/null || true)
            parent_number="0"
            add_target_segment "commit" "$parent_sha" "$commit_sha"
            collect_diff "commit" git diff-tree --root --no-commit-id -r --name-status -z --find-renames "$commit_sha" --
        else
            if [ -n "$parent_override" ]; then
                parent_number="$parent_override"
            else
                parent_number="1"
            fi
            if [ "$parent_number" -gt "$parent_count" ]; then
                emit_error "invalid_parent" "Commit has no parent $parent_number." \
                    "Choose a parent index from 1 through $parent_count."
            fi
            parent_sha=${commit_parts[$parent_number]}
            add_target_segment "commit" "$parent_sha" "$commit_sha"
            collect_diff "commit" git diff --name-status -z --find-renames "$parent_sha" "$commit_sha" --
        fi
        complete_feature="false"
        ;;
esac

classify_inventory() {
    local i path status mode kind
    i=0
    while [ "$i" -lt "${#inventory_paths[@]}" ]; do
        path=${inventory_paths[$i]}
        status=${inventory_statuses[$i]}
        mode=$(git ls-files -s -- "$path" 2>/dev/null | awk 'NR == 1 {print $1}')
        kind="file"
        if [ "$mode" = "160000" ]; then
            kind="submodule"
        elif [ "$mode" = "120000" ] || [ -L "$path" ]; then
            kind="symlink"
        elif [ "$status" = "D" ] && [ ! -e "$path" ] && [ ! -L "$path" ]; then
            kind="missing"
        elif [ -f "$path" ]; then
            if [ -s "$path" ] && ! LC_ALL=C grep -Iq . "$path" 2>/dev/null; then
                kind="binary"
            fi
        fi
        inventory_modes[$i]="$mode"
        inventory_kinds[$i]="$kind"
        i=$((i + 1))
    done
}

classify_inventory

feature_status="not_resolved"
feature_source="none"
feature_path=""
if [ -n "$feature_override" ]; then
    if [ ! -d "$feature_override" ]; then
        emit_error "feature_not_found" "Feature directory does not exist: $feature_override" \
            "Pass an existing CodexSpec feature directory."
    fi
    feature_path=$(cd "$feature_override" 2>/dev/null && pwd -P)
    feature_status="resolved"
    feature_source="explicit"
elif [ -n "$current_branch" ] && [ -d "$repo_root/.codexspec/specs/$current_branch" ]; then
    feature_path=$(cd "$repo_root/.codexspec/specs/$current_branch" 2>/dev/null && pwd -P)
    feature_status="resolved"
    feature_source="branch"
fi

printf '{"schema_version":"%s","status":"ok","mode":"defect","selector":' "$SCHEMA_VERSION"
json_string "$selector"
printf ',"arguments":{"base_override":'
json_nullable_string "$base_override"
printf ',"commit":'
json_nullable_string "$commit_input"
printf ',"parent":'
if [ -n "$parent_override" ]; then printf '%s' "$parent_override"; else printf 'null'; fi
printf ',"feature_override":'
json_nullable_string "$feature_override"
printf ',"focus":['
i=0
while [ "$i" -lt "${#focus_values[@]}" ]; do
    [ "$i" -gt 0 ] && printf ','
    json_string "${focus_values[$i]}"
    i=$((i + 1))
done
printf ']},"repository":{"root":'
json_string "$repo_root"
printf ',"current_branch":'
json_nullable_string "$current_branch"
printf ',"head_sha":'
json_string "$head_sha"
printf '},"target":{"complete_feature":%s,"empty":' "$complete_feature"
if [ "${#inventory_paths[@]}" -eq 0 ]; then printf 'true'; else printf 'false'; fi
printf ',"base_ref":'
json_nullable_string "$base_ref"
printf ',"base_sha":'
json_nullable_string "$base_sha"
printf ',"merge_base_sha":'
json_nullable_string "$merge_base_sha"
printf ',"commit_sha":'
json_nullable_string "$commit_sha"
printf ',"parent_sha":'
json_nullable_string "$parent_sha"
printf ',"parent_number":'
if [ -n "$parent_number" ]; then printf '%s' "$parent_number"; else printf 'null'; fi
printf ',"segments":['
i=0
while [ "$i" -lt "${#target_segment_names[@]}" ]; do
    [ "$i" -gt 0 ] && printf ','
    printf '{"name":'
    json_string "${target_segment_names[$i]}"
    printf ',"from":'
    json_nullable_string "${target_segment_from[$i]}"
    printf ',"to":'
    json_nullable_string "${target_segment_to[$i]}"
    printf '}'
    i=$((i + 1))
done
printf ']},"feature":{"status":'
json_string "$feature_status"
printf ',"source":'
json_string "$feature_source"
printf ',"path":'
json_nullable_string "$feature_path"
printf ',"artifacts":['
if [ -n "$feature_path" ]; then
    artifact_index=0
    for artifact in requirements.md spec.md plan.md tasks.md; do
        [ "$artifact_index" -gt 0 ] && printf ','
        printf '{"name":'
        json_string "$artifact"
        printf ',"readable":'
        if [ -r "$feature_path/$artifact" ]; then printf 'true'; else printf 'false'; fi
        printf '}'
        artifact_index=$((artifact_index + 1))
    done
fi
printf ']},"inventory":['
i=0
committed_count=0
staged_count=0
unstaged_count=0
untracked_count=0
while [ "$i" -lt "${#inventory_paths[@]}" ]; do
    [ "$i" -gt 0 ] && printf ','
    printf '{"path":'
    json_string "${inventory_paths[$i]}"
    printf ',"old_path":'
    json_nullable_string "${inventory_old_paths[$i]}"
    printf ',"status":'
    json_string "${inventory_statuses[$i]}"
    printf ',"segments":['
    IFS=',' read -r -a record_segments <<< "${inventory_segments[$i]}"
    segment_index=0
    while [ "$segment_index" -lt "${#record_segments[@]}" ]; do
        [ "$segment_index" -gt 0 ] && printf ','
        segment_name=${record_segments[$segment_index]}
        json_string "$segment_name"
        case "$segment_name" in
            committed|commit) committed_count=$((committed_count + 1)) ;;
            staged) staged_count=$((staged_count + 1)) ;;
            unstaged) unstaged_count=$((unstaged_count + 1)) ;;
            untracked) untracked_count=$((untracked_count + 1)) ;;
        esac
        segment_index=$((segment_index + 1))
    done
    printf '],"object_mode":'
    json_nullable_string "${inventory_modes[$i]}"
    printf ',"kind":'
    json_string "${inventory_kinds[$i]}"
    printf '}'
    i=$((i + 1))
done
printf '],"counts":{"total":%s,"committed":%s,"staged":%s,"unstaged":%s,"untracked":%s}}\n' \
    "${#inventory_paths[@]}" "$committed_count" "$staged_count" "$unstaged_count" "$untracked_count"
