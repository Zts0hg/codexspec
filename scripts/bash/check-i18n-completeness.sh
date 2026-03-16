#!/usr/bin/env bash
#
# Check i18n translation completeness
# Detects untranslated English content in target language files
#
# Usage: ./check-i18n-completeness.sh <docs_dir> [target_langs...]
# Returns: 0 if all translations complete, 1 if untranslated content found

set -e

DOCS_DIR="${1:-docs}"
SOURCE_LANG="en"
shift
TARGET_LANGS="$*"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Check if docs directory exists
if [ ! -d "$DOCS_DIR" ]; then
    echo "Error: Docs directory '$DOCS_DIR' not found"
    exit 2
fi

# Get target languages if not specified
if [ -z "$TARGET_LANGS" ]; then
    cd "$DOCS_DIR"
    TARGET_LANGS=$(find . -maxdepth 1 -type d ! -name "." ! -name "./$SOURCE_LANG" | sed 's|^\./||' | sed 's|^.*/||' | sort | tr '\n' ' ')
fi

if [ -z "$TARGET_LANGS" ]; then
    echo "Warning: No target language directories found"
    exit 0
fi

echo "Checking translation completeness..."
echo "Source language: $SOURCE_LANG"
echo "Target languages: $TARGET_LANGS"
echo ""

ERRORS=0
WARNINGS=0

# Function to check if text is likely untranslated English
is_untranslated() {
    local text="$1"

    # Skip empty lines
    [ -z "$text" ] && return 1

    # Skip lines that are just punctuation or numbers
    echo "$text" | grep -qE '^[[:punct:][:space:][:digit:]]*$' && return 1

    # Skip YAML frontmatter lines
    echo "$text" | grep -qE '^(---|\.\.\.)([[:space:]]|$)' && return 1

    # Skip code blocks (bash -n will handle these)
    echo "$text" | grep -qE '^```' && return 1

    # Skip inline code
    echo "$text" | grep -qE '^\s*`[^`]+`\s*$' && return 1

    # Skip URLs
    echo "$text" | grep -qE '^\s*https?://' && return 1

    # Skip lines that are mostly URLs or paths
    echo "$text" | grep -qE '\[.*\]\(http' && return 1

    # Skip lines that are purely code comments with English commands
    echo "$text" | grep -qE '^\s*(//|#)\s*(npm|yarn|pip|uv|git|python|node)\s' && return 1

    # Check if line contains substantial English text
    # (words longer than 3 chars, excluding common tech terms)
    if echo "$text" | grep -qE '\b[A-Za-z]{4,}\b'; then
        # Exclude common technical terms that should stay in English
        local tech_terms="API|CLI|HTTP|HTTPS|JSON|YAML|TOML|URL|GitHub|GitLab|npm|yarn|pip|pytest"
        if ! echo "$text" | grep -qE "\b($tech_terms)\b"; then
            return 0
        fi
    fi

    return 1
}

# Check each target language
for lang in $TARGET_LANGS; do
    echo -e "${BLUE}Checking $lang...${NC}"

    if [ ! -d "$DOCS_DIR/$lang" ]; then
        echo "  ${YELLOW}⚠${NC} Directory not found: $DOCS_DIR/$lang"
        WARNINGS=$((WARNINGS + 1))
        continue
    fi

    # Find all markdown files in target language
    cd "$DOCS_DIR/$lang"
    TARGET_FILES=$(find . -name "*.md" -type f | sort)

    for file in $TARGET_FILES; do
        IN_CODE_BLOCK=0
        FILE_ISSUES=0

        while IFS= read -r line; do
            # Track code blocks
            if echo "$line" | grep -qE '^```'; then
                IN_CODE_BLOCK=$((1 - IN_CODE_BLOCK))
                continue
            fi

            # Skip lines inside code blocks
            [ $IN_CODE_BLOCK -eq 1 ] && continue

            # Check for untranslated English
            if is_untranslated "$line"; then
                # Extract English words for reporting
                english_words=$(echo "$line" | grep -oE '\b[A-Za-z]{4,}\b' | head -5 | tr '\n' ' ')

                if [ $FILE_ISSUES -eq 0 ]; then
                    echo "  ${RED}✗${NC} $file"
                fi

                echo "    Line contains untranslated English: $english_words..."
                FILE_ISSUES=$((FILE_ISSUES + 1))
                ERRORS=$((ERRORS + 1))
            fi
        done < "$file"
    done

    if [ $ERRORS -eq 0 ]; then
        echo "  ${GREEN}✓${NC} No untranslated content found"
    fi

    echo ""
done

# Summary
echo "==================================="
echo "Completeness Check Summary"
echo "==================================="
echo "Untranslated segments: $ERRORS"
echo "Warnings: $WARNINGS"
echo ""

if [ $ERRORS -gt 0 ]; then
    echo "${RED}FAILED${NC}: Found untranslated English content"
    echo ""
    echo "Tips for fixing:"
    echo "1. Translate the English text to the target language"
    echo "2. Keep technical terms (API, CLI, etc.) in English if appropriate"
    echo "3. Use the glossary for consistent term translations"
    exit 1
else
    echo "${GREEN}PASSED${NC}: All translations appear complete"
    exit 0
fi
