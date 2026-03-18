#!/usr/bin/env python3
"""
Real Message Extractor Utility

This script extracts real messages from Claude Code JSONL files and saves them
as categorized test fixtures. Run this once to generate the test data, then tests use
the static fixtures without needing access to the real environment.

Usage:
    # Extract from default location (~/.claude/projects/*/*.jsonl)
    uv run python tests/scripts/python/extract_real_messages.py

    # Extract from specific directory
    uv run python tests/scripts/python/extract_real_messages.py --input /path/to/jsonl/files

    # Specify output file
    uv run python tests/scripts/python/extract_real_messages.py --output tests/scripts/python/fixtures/real_messages.py
"""

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Any


def categorize_message(message: dict) -> str | None:
    """Categorize a message by its type based on stop_reason and content.

    Args:
        message: The message dictionary to categorize

    Returns:
        Category name or None if not relevant
    """
    stop_reason = message.get("stop_reason")
    content = message.get("content", [])

    # STREAMING: stop_reason=null
    if stop_reason is None:
        return "STREAMING"

    # Check for AskUserQuestion tool
    for item in content:
        if item.get("type") == "tool_use" and item.get("name") == "AskUserQuestion":
            return "USER_QUESTION"

    # TOOL_USE: stop_reason=tool_use (but not AskUserQuestion)
    if stop_reason == "tool_use":
        return "TOOL_USE"

    # ERROR_STOP: check for error conditions
    if stop_reason in ("refusal", "error"):
        return "ERROR_STOP"

    # Check for tool_result with is_error
    for item in content:
        if item.get("type") == "tool_result" and item.get("is_error"):
            return "ERROR_STOP"

    # TASK_COMPLETE: normal completion reasons
    if stop_reason in ("end_turn", "stop_sequence", "max_tokens"):
        return "TASK_COMPLETE"

    return None


def extract_messages_from_jsonl(jsonl_path: Path) -> dict[str, list[dict]]:
    """Extract and categorize messages from a JSONL file.

    Args:
        jsonl_path: Path to the JSONL file

    Returns:
        Dictionary mapping categories to lists of messages
    """
    categorized: dict[str, list[dict]] = {
        "STREAMING": [],
        "TOOL_USE": [],
        "USER_QUESTION": [],
        "ERROR_STOP": [],
        "TASK_COMPLETE": [],
    }

    with open(jsonl_path, "r", encoding="utf-8") as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue

            try:
                data = json.loads(line)
            except json.JSONDecodeError:
                continue

            # Handle wrapped messages (type: "assistant", message: {...})
            message = data.get("message", data)
            if data.get("type") != "assistant":
                continue

            category = categorize_message(message)
            if category and category in categorized:
                # Keep only first 3 samples per category to avoid huge files
                if len(categorized[category]) < 3:
                    categorized[category].append(message)

    return categorized


def extract_all_messages(input_dir: Path) -> dict[str, list[dict]]:
    """Extract messages from all JSONL files in a directory (including nested).

    Args:
        input_dir: Directory containing JSONL files (searches recursively)

    Returns:
        Dictionary mapping categories to lists of messages
    """
    all_categorized: dict[str, list[dict]] = {
        "STREAMING": [],
        "TOOL_USE": [],
        "USER_QUESTION": [],
        "ERROR_STOP": [],
        "TASK_COMPLETE": [],
    }

    # Search recursively for JSONL files
    jsonl_files = list(input_dir.rglob("*.jsonl"))

    for jsonl_file in jsonl_files:
        categorized = extract_messages_from_jsonl(jsonl_file)
        for category, messages in categorized.items():
            for msg in messages:
                if len(all_categorized[category]) < 5:  # Max 5 per category
                    all_categorized[category].append(msg)

    return all_categorized


def _convert_to_python_literal(obj: Any, indent: int = 0) -> str:
    """Convert a Python object to a valid Python literal string.

    This handles the conversion of JSON null to Python None.
    """
    indent_str = "    " * indent
    if obj is None:
        return "None"
    elif isinstance(obj, bool):
        return "True" if obj else "False"
    elif isinstance(obj, (int, float)):
        return repr(obj)
    elif isinstance(obj, str):
        # Use repr for proper escaping
        return repr(obj)
    elif isinstance(obj, list):
        if not obj:
            return "[]"
        items = []
        for item in obj:
            items.append(_convert_to_python_literal(item, indent + 1))
        if len(items) <= 2 and all(len(i) < 50 for i in items):
            return "[" + ", ".join(items) + "]"
        inner = ",\n".join("    " * (indent + 1) + item for item in items)
        return f"[\n{inner},\n{indent_str}]"
    elif isinstance(obj, dict):
        if not obj:
            return "{}"
        items = []
        for k, v in obj.items():
            key_str = repr(k)
            val_str = _convert_to_python_literal(v, indent + 1)
            items.append(f"{key_str}: {val_str}")
        inner = ",\n".join("    " * (indent + 1) + item for item in items)
        return f"{{\n{inner},\n{indent_str}}}"
    else:
        return repr(obj)


def generate_python_fixture(categorized: dict[str, list[dict]], output_path: Path) -> None:
    """Generate a Python file with message fixtures.

    Args:
        categorized: Dictionary of categorized messages
        output_path: Path to write the Python file
    """
    lines = [
        "#!/usr/bin/env python3",
        '"""',
        "Real Message Fixtures for Testing",
        "",
        "This file contains extracted real messages from Claude Code JSONL files.",
        "These are used as static test data to avoid depending on the real environment.",
        "",
        f"Generated: {datetime.now().isoformat()}",
        '"""',
        "",
        "# Message samples categorized by type",
        "REAL_MESSAGES = {",
    ]

    for category, messages in categorized.items():
        lines.append(f'    "{category}": [')
        for i, msg in enumerate(messages):
            # Convert to valid Python literal
            msg_str = _convert_to_python_literal(msg, indent=3)
            # Add proper indentation
            indented = "\n".join("        " + line if line.strip() else "" for line in msg_str.split("\n"))
            lines.append(f"        # Sample {i + 1}")
            lines.append(f"        {indented},")
        lines.append("    ],")

    lines.append("}")
    lines.append("")
    lines.append("")
    lines.append("def get_messages(category: str) -> list[dict]:")
    lines.append('    """Get messages for a specific category."""')
    lines.append("    return REAL_MESSAGES.get(category, [])")
    lines.append("")
    lines.append("")
    lines.append("def get_sample(category: str, index: int = 0) -> dict | None:")
    lines.append('    """Get a single sample message."""')
    lines.append("    messages = get_messages(category)")
    lines.append("    return messages[index] if index < len(messages) else None")
    lines.append("")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"Written fixtures to {output_path}")


def main():
    parser = argparse.ArgumentParser(description="Extract real messages from JSONL files for testing")
    parser.add_argument(
        "--input",
        type=Path,
        default=Path.home() / ".claude" / "projects",
        help="Input directory containing JSONL files (default: ~/.claude/projects)",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(__file__).parent / "fixtures" / "real_messages.py",
        help="Output Python file path (default: fixtures/real_messages.py)",
    )
    args = parser.parse_args()

    if not args.input.exists():
        print(f"Error: Input directory does not exist: {args.input}", file=sys.stderr)
        sys.exit(1)

    print(f"Extracting messages from: {args.input}")
    categorized = extract_all_messages(args.input)

    # Print summary
    print("\nExtracted messages:")
    total = 0
    for category, messages in categorized.items():
        count = len(messages)
        total += count
        print(f"  {category}: {count}")
    print(f"  Total: {total}")

    if total == 0:
        print("\nNo messages found. Make sure the input directory contains JSONL files.", file=sys.stderr)
        sys.exit(1)

    generate_python_fixture(categorized, args.output)
    print("\nDone! You can now use these fixtures in your tests.")


if __name__ == "__main__":
    main()
