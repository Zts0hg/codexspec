#!/usr/bin/env bash
#
# Check i18n structure consistency across all language versions
# Ensures all language directories have the same file structure as the source (en)
#
# Usage: ./check-i18n-structure.sh <docs_dir>
# Returns: 0 if structure is consistent, 1 if issues found

set -e

DOCS_DIR="${1:-docs}"
SOURCE_LANG="en"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if docs directory exists
if [ ! -d "$DOCS_DIR" ]; then
    echo "Error: Docs directory '$DOCS_DIR' not found"
    exit 2
fi

# Check if source language directory exists
if [ ! -d "$DOCS_DIR/$SOURCE_LANG" ]; then
    echo "Error: Source language directory '$DOCS_DIR/$SOURCE_LANG' not found"
    exit 2
fi

echo "Checking i18n structure consistency..."
echo "Source language: $SOURCE_LANG"
echo ""

# Get list of all markdown files in source language
cd "$DOCS_DIR/$SOURCE_LANG"
SOURCE_FILES=$(find . -name "*.md" -type f | sort)
SOURCE_COUNT=$(echo "$SOURCE_FILES" | grep -c "^" || echo 0)

echo "Source files found: $SOURCE_COUNT"
echo ""

# Get list of target language directories
cd "$DOCS_DIR"
LANG_DIRS=$(find . -maxdepth 1 -type d ! -name "." ! -name "./$SOURCE_LANG" | sed 's|^\./||' | sed 's|^.*/||' | sort)

if [ -z "$LANG_DIRS" ]; then
    echo "Warning: No target language directories found"
    exit 0
fi

echo "Target languages: $(echo "$LANG_DIRS" | tr '\n' ' ')"
echo ""

ERRORS=0
WARNINGS=0

# Check each target language
for lang in $LANG_DIRS; do
    echo "Checking $lang..."

    cd "$DOCS_DIR/$lang"
    TARGET_FILES=$(find . -name "*.md" -type f | sort)
    TARGET_COUNT=$(echo "$TARGET_FILES" | grep -c "^" || echo 0)

    # Compare file counts
    if [ "$TARGET_COUNT" -ne "$SOURCE_COUNT" ]; then
        echo "  ${YELLOW}⚠${NC} File count mismatch: $lang has $TARGET_COUNT files, expected $SOURCE_COUNT"
        WARNINGS=$((WARNINGS + 1))
    else
        echo "  ${GREEN}✓${NC} File count matches: $TARGET_COUNT"
    fi

    # Check for missing files
    for src_file in $SOURCE_FILES; do
        if [ ! -f "$src_file" ]; then
            echo "  ${RED}✗${NC} Missing file: $src_file"
            ERRORS=$((ERRORS + 1))
        fi
    done

    # Check for extra files (not in source)
    for tgt_file in $TARGET_FILES; do
        if ! echo "$SOURCE_FILES" | grep -q "^$tgt_file$"; then
            echo "  ${YELLOW}⚠${NC} Extra file (not in source): $tgt_file"
            WARNINGS=$((WARNINGS + 1))
        fi
    done

    echo ""
done

# Summary
echo "==================================="
echo "Structure Check Summary"
echo "==================================="
echo "Errors: $ERRORS"
echo "Warnings: $WARNINGS"
echo ""

if [ $ERRORS -gt 0 ]; then
    echo "${RED}FAILED${NC}: Structure inconsistencies found"
    exit 1
elif [ $WARNINGS -gt 0 ]; then
    echo "${YELLOW}WARNING${NC}: Minor structure differences found"
    exit 0
else
    echo "${GREEN}PASSED${NC}: All language structures are consistent"
    exit 0
fi
