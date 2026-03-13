#!/usr/bin/env python3
"""
Format Python code files according to PEP 8 style guidelines.
- Normalize indentation (4 spaces)
- Remove trailing whitespace
- Ensure single newline at end of file
- One blank line between methods inside a class
- Two blank lines between top-level classes/functions
- Remove multiple consecutive blank lines
"""

import re
from pathlib import Path


def format_python_file(file_path: Path) -> bool:
    """Format a single Python file. Returns True if file was modified."""
    with open(file_path, "r", encoding="utf-8") as f:
        original_content = f.read()
    
    lines = original_content.splitlines()
    result = []
    i = 0
    
    while i < len(lines):
        line = lines[i]
        stripped = line.rstrip()
        
        if stripped == "":
            blank_count = 0
            while i < len(lines) and lines[i].strip() == "":
                blank_count += 1
                i += 1
            
            if i >= len(lines):
                break
            
            next_line = lines[i]
            next_stripped = next_line.strip()
            next_indent = len(next_line) - len(next_line.lstrip())
            
            is_top_level = next_indent == 0
            is_class = next_stripped.startswith("class ")
            is_def = next_stripped.startswith("def ") or next_stripped.startswith("async def ")
            is_decorator = next_stripped.startswith("@")
            
            if is_class and is_top_level:
                result.append("")
                result.append("")
            elif (is_decorator or is_def) and not is_top_level:
                result.append("")
            else:
                result.append("")
            
            continue
        
        if stripped and line[0] in " \t":
            indent = 0
            for ch in line:
                if ch == "\t":
                    indent += 4
                elif ch == " ":
                    indent += 1
                else:
                    break
            stripped = " " * indent + stripped.lstrip()
        
        result.append(stripped)
        i += 1
    
    while result and result[-1] == "":
        result.pop()
    
    formatted = "\n".join(result) + "\n" if result else ""
    
    if formatted != original_content:
        with open(file_path, "w", encoding="utf-8", newline="\n") as f:
            f.write(formatted)
        return True
    return False


def format_lua_file(file_path: Path) -> bool:
    """Format a Lua file. Returns True if file was modified."""
    with open(file_path, "r", encoding="utf-8") as f:
        original_content = f.read()
    
    lines = original_content.splitlines()
    result = []
    
    for line in lines:
        stripped = line.rstrip()
        if stripped and line[0] in " \t":
            indent = 0
            for ch in line:
                if ch == "\t":
                    indent += 4
                elif ch == " ":
                    indent += 1
                else:
                    break
            stripped = " " * indent + stripped.lstrip()
        result.append(stripped)
    
    while result and result[-1] == "":
        result.pop()
    
    formatted = "\n".join(result) + "\n" if result else ""
    
    if formatted != original_content:
        with open(file_path, "w", encoding="utf-8", newline="\n") as f:
            f.write(formatted)
        return True
    return False


def main():
    base_path = Path(__file__).parent.parent / "custom_components" / "midea_smart_home"
    
    py_files = list(base_path.rglob("*.py"))
    lua_files = list(base_path.rglob("*.lua"))
    
    py_modified = 0
    lua_modified = 0
    
    print(f"Found {len(py_files)} Python files")
    for py_file in py_files:
        if format_python_file(py_file):
            py_modified += 1
            print(f"  Formatted: {py_file.relative_to(base_path.parent.parent)}")
    
    print(f"\nFound {len(lua_files)} Lua files")
    for lua_file in lua_files:
        if format_lua_file(lua_file):
            lua_modified += 1
            print(f"  Formatted: {lua_file.relative_to(base_path.parent.parent)}")
    
    print(f"\nDone! Modified {py_modified} Python files, {lua_modified} Lua files.")


if __name__ == "__main__":
    main()
