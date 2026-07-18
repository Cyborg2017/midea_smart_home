#!/usr/bin/env python3
"""
Sort translation and icon files alphabetically by key.
"""

import argparse
import json
import re
import sys
from pathlib import Path


PRESERVE_ORDER_KEYS = {"data", "data_description"}

def natural_sort_key(key: str) -> tuple:
    """Generate a sort key that sorts numbers numerically, not lexicographically.

    Splits the string into numeric and non-numeric parts, converting numeric parts
    to integers for proper numerical ordering.
    """
    def try_convert(part):
        try:
            return (0, int(part), "")
        except ValueError:
            return (1, 0, part.lower())

    return tuple(try_convert(part) for part in re.split(r'(\d+)', str(key)))


def sort_dict_recursive(d: dict, parent_key: str = "") -> dict:
    """Sort dictionary recursively, preserving order for value mappings."""
    if not isinstance(d, dict):
        return d

    if parent_key in PRESERVE_ORDER_KEYS:
        return d

    sorted_keys = sorted(d.keys(), key=natural_sort_key)
    result = {}

    for key in sorted_keys:
        value = d[key]
        if isinstance(value, dict):
            result[key] = sort_dict_recursive(value, key)
        else:
            result[key] = value

    return result


def format_icons_json(data: dict) -> str:
    """Format icons.json with compact entity entries."""
    lines = ["{"]
    lines.append('    "entity": {')
    
    entity_types = sorted(data.get("entity", {}).keys(), key=lambda x: str(x).lower())
    
    for i, entity_type in enumerate(entity_types):
        entities = data["entity"][entity_type]
        lines.append(f'        "{entity_type}": {{')
        
        entity_ids = sorted(entities.keys(), key=lambda x: str(x).lower())
        for j, entity_id in enumerate(entity_ids):
            entity_data = entities[entity_id]
            icon = entity_data.get("default", "")
            comma = "," if j < len(entity_ids) - 1 else ""
            lines.append(f'            "{entity_id}": {{ "default": "{icon}" }}{comma}')
        
        comma = "," if i < len(entity_types) - 1 else ""
        lines.append(f'        }}{comma}')
    
    lines.append("    }")
    lines.append("}")
    
    return "\n".join(lines)


def check_json_file(file_path: Path, is_icons: bool = False) -> bool:
    """Check if a JSON file needs sorting. Returns True if file needs sorting."""
    with open(file_path, "r", encoding="utf-8") as f:
        original_content = f.read()
    
    data = json.loads(original_content)
    sorted_data = sort_dict_recursive(data)
    
    if is_icons:
        formatted = format_icons_json(sorted_data)
    else:
        formatted = json.dumps(sorted_data, ensure_ascii=False, indent=2) + "\n"
    
    # Normalize both for comparison (strip trailing whitespace/newlines)
    original_normalized = original_content.rstrip()
    formatted_normalized = formatted.rstrip()
    
    return formatted_normalized != original_normalized


def check_translations() -> bool:
    """Check if translation files need sorting. Returns True if any file needs sorting."""
    base_path = Path(__file__).parent.parent / "custom_components" / "midea_smart_home"
    translations_path = base_path / "translations"
    icons_path = base_path / "icons.json"
    
    needs_sort = []
    
    en_file = translations_path / "en.json"
    zh_file = translations_path / "zh-Hans.json"
    
    if check_json_file(en_file):
        needs_sort.append(en_file)
    if check_json_file(zh_file):
        needs_sort.append(zh_file)
    if check_json_file(icons_path, is_icons=True):
        needs_sort.append(icons_path)
    
    return needs_sort


def main():
    parser = argparse.ArgumentParser(description="Sort translation and icon files")
    parser.add_argument(
        "--check",
        action="store_true",
        help="Check if files are sorted correctly without modifying them",
    )
    args = parser.parse_args()
    
    base_path = Path(__file__).parent.parent / "custom_components" / "midea_smart_home"
    translations_path = base_path / "translations"
    icons_path = base_path / "icons.json"
    
    en_file = translations_path / "en.json"
    zh_file = translations_path / "zh-Hans.json"
    
    if args.check:
        needs_sort = []
        
        print("Checking translation files...")
        if check_json_file(en_file):
            needs_sort.append(en_file)
            print(f"  Needs sorting: {en_file.relative_to(base_path.parent.parent)}")
        if check_json_file(zh_file):
            needs_sort.append(zh_file)
            print(f"  Needs sorting: {zh_file.relative_to(base_path.parent.parent)}")
        if check_json_file(icons_path, is_icons=True):
            needs_sort.append(icons_path)
            print(f"  Needs sorting: {icons_path.relative_to(base_path.parent.parent)}")
        
        if needs_sort:
            print(f"\n[ERROR] Found {len(needs_sort)} files that need sorting.")
            print("   Run: python scripts/sort_translations.py")
            sys.exit(1)
        else:
            print("\n[OK] All files are properly sorted.")
            sys.exit(0)
    else:
        print("Sorting English translation file...")
        with open(en_file, "r", encoding="utf-8") as f:
            en_data = json.load(f)
        sorted_en = sort_dict_recursive(en_data)
        with open(en_file, "w", encoding="utf-8", newline="\n") as f:
            json.dump(sorted_en, f, ensure_ascii=False, indent=2)
            f.write("\n")
        print(f"  Saved: {en_file}")
        
        print("Sorting Chinese translation file...")
        with open(zh_file, "r", encoding="utf-8") as f:
            zh_data = json.load(f)
        sorted_zh = sort_dict_recursive(zh_data)
        with open(zh_file, "w", encoding="utf-8", newline="\n") as f:
            json.dump(sorted_zh, f, ensure_ascii=False, indent=2)
            f.write("\n")
        print(f"  Saved: {zh_file}")
        
        print("Sorting icons file...")
        with open(icons_path, "r", encoding="utf-8") as f:
            icons_data = json.load(f)
        sorted_icons = sort_dict_recursive(icons_data)
        formatted = format_icons_json(sorted_icons)
        with open(icons_path, "w", encoding="utf-8", newline="\n") as f:
            f.write(formatted)
            f.write("\n")
        print(f"  Saved: {icons_path}")
        
        print("\nDone!")


if __name__ == "__main__":
    main()
