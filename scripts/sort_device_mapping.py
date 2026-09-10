#!/usr/bin/env python3
"""
Sort Platform.* keys inside entities dicts of device_mapping files.

Reorders the Platform.* entries of every standalone device mapping
(T0x*.py) into a canonical order and normalizes the trailing comma of
each entry (all entries end with a comma except the last one).
"""

import argparse
import re
import sys
from pathlib import Path

# Canonical order of Platform.* keys inside "entities" dicts.
PLATFORM_ORDER = [
    "CLIMATE", "COVER", "FAN", "HUMIDIFIER", "LIGHT", "TEXT", "TIME",
    "VACUUM", "WATER_HEATER", "BUTTON", "LOCK", "NUMBER", "SWITCH",
    "SELECT", "BINARY_SENSOR", "SENSOR",
]
PLATFORM_RANK = {name: i for i, name in enumerate(PLATFORM_ORDER)}

ENTRY_RE = re.compile(r"^( +)Platform\.([A-Z_]+): \{")
ENTITIES_RE = re.compile(r'^(\s*)"entities": \{\s*$')


def _collect_entry_blocks(lines: list, start: int, entities_indent: int) -> tuple:
    """Collect consecutive Platform.* entry blocks below an entities dict.

    Returns (blocks, next_index) where blocks is a list of
    (platform_name, block_lines).
    """
    blocks = []
    i = start
    while i < len(lines):
        m = ENTRY_RE.match(lines[i])
        if not m or len(m.group(1)) != entities_indent + 4:
            break
        entry_indent = len(m.group(1))
        block = [lines[i]]
        i += 1
        while i < len(lines):
            line = lines[i]
            if not line.strip():
                block.append(line)
                i += 1
                continue
            indent = len(line) - len(line.lstrip(" "))
            if indent < entry_indent:
                break
            block.append(line)
            i += 1
            if indent == entry_indent:
                break
        blocks.append((m.group(2), block))
    return blocks, i


def _normalize_block_ending(block: list, is_last: bool) -> None:
    """Ensure the entry's closing line ends with a comma unless it is last."""
    for idx in range(len(block) - 1, -1, -1):
        if block[idx].strip():
            line = block[idx]
            stripped = line.rstrip("\r\n")
            eol = line[len(stripped):]
            core = stripped.rstrip()
            core = core.rstrip(",") if is_last else core.rstrip(",") + ","
            block[idx] = core + eol
            return


def sort_platform_entries(text: str) -> str:
    """Return file content with Platform.* entity keys in canonical order."""
    lines = text.splitlines(keepends=True)
    out = []
    i = 0
    while i < len(lines):
        m = ENTITIES_RE.match(lines[i])
        if not m:
            out.append(lines[i])
            i += 1
            continue
        entities_indent = len(m.group(1))
        out.append(lines[i])
        i += 1
        blocks, i = _collect_entry_blocks(lines, i, entities_indent)
        if blocks:
            blocks.sort(key=lambda b: PLATFORM_RANK.get(b[0], len(PLATFORM_ORDER)))
            for pos, (_, block) in enumerate(blocks):
                _normalize_block_ending(block, is_last=pos == len(blocks) - 1)
                out.extend(block)
    return "".join(out)


def check_device_mapping_file(path: Path) -> bool:
    """Check a single file. Returns True if it needs sorting."""
    original = path.read_text(encoding="utf-8")
    return sort_platform_entries(original) != original


def sort_device_mapping_file(path: Path) -> bool:
    """Sort a single file in place. Returns True if it was modified."""
    original = path.read_text(encoding="utf-8")
    sorted_text = sort_platform_entries(original)
    if sorted_text != original:
        path.write_text(sorted_text, encoding="utf-8")
        return True
    return False


def main():
    parser = argparse.ArgumentParser(description="Sort Platform keys in device_mapping files")
    parser.add_argument(
        "--check",
        action="store_true",
        help="Check if files are sorted correctly without modifying them",
    )
    args = parser.parse_args()

    base_path = Path(__file__).parent.parent / "custom_components" / "midea_smart_home"
    device_mapping_path = base_path / "device_mapping"
    py_files = sorted(device_mapping_path.glob("T0x*.py"))

    if args.check:
        print(f"Checking {len(py_files)} device mapping files...")
        needs_sort = []
        for py_file in py_files:
            if check_device_mapping_file(py_file):
                needs_sort.append(py_file.relative_to(base_path.parent.parent))

        if needs_sort:
            print("  The following files need sorting:")
            for f in needs_sort:
                print(f"    {f}")
            print(f"\n[ERROR] Found {len(needs_sort)} files that need sorting.")
            print("   Run: python scripts/sort_device_mapping.py")
            sys.exit(1)
        else:
            print("\n[OK] All files are properly sorted.")
            sys.exit(0)
    else:
        print(f"Found {len(py_files)} device mapping files")
        modified = 0
        for py_file in py_files:
            if sort_device_mapping_file(py_file):
                modified += 1
                print(f"  Formatted: {py_file.relative_to(base_path.parent.parent)}")

        print(f"\nDone! Modified {modified} files.")


if __name__ == "__main__":
    main()
