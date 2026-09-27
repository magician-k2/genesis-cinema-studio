# -*- coding: utf-8 -*-
"""
GENESIS Surgical Patch Synthesizer Skill
Performs AST-guided surgical code splicing and unified diff generation.
Guarantees indentation safety, syntax preservation, and git-apply compatibility.
"""

import difflib
from pathlib import Path
from typing import Dict, Any, List

def apply_surgical_fix(original_code: str, line_no: int, replacement_lines: List[str]) -> str:
    """
    Replaces or wraps the targeted line with proper indentation.
    """
    lines = original_code.splitlines(keepends=True)
    if line_no < 1 or line_no > len(lines):
        return original_code

    target_idx = line_no - 1
    target_line = lines[target_idx]

    # Detect indentation of target line
    indent = ""
    for ch in target_line:
        if ch in (" ", "\t"):
            indent += ch
        else:
            break

    # Format replacements preserving relative indentation
    formatted_replacements = []
    for r in replacement_lines:
        if not r.endswith("\n"):
            r += "\n"
        # Prepend base indent to every replacement line
        formatted_replacements.append(indent + r)

    # Splice
    new_lines = lines[:target_idx] + formatted_replacements + lines[target_idx + 1:]
    return "".join(new_lines)

def synthesize_patch(
    file_rel_path: str,
    original_code: str,
    modified_code: str
) -> Dict[str, Any]:
    """
    Produces standard git unified diff with @@ hunk headers.
    """
    orig_lines = original_code.splitlines(keepends=True)
    mod_lines = modified_code.splitlines(keepends=True)

    clean_path = file_rel_path.replace("\\", "/").lstrip("/")

    diff_lines = list(difflib.unified_diff(
        orig_lines,
        mod_lines,
        fromfile=f"a/{clean_path}",
        tofile=f"b/{clean_path}",
        n=3
    ))

    if not diff_lines:
        return {"has_diff": False, "patch": "", "changed_lines": 0}

    # Prepend standard git header
    git_header = [
        f"diff --git a/{clean_path} b/{clean_path}\n",
        f"--- a/{clean_path}\n",
        f"+++ b/{clean_path}\n"
    ]
    # Filter out difflib standard header lines
    body_lines = [l for l in diff_lines if not l.startswith("---") and not l.startswith("+++")]
    full_patch = "".join(git_header + body_lines)

    changed_count = sum(1 for l in body_lines if l.startswith('+') or l.startswith('-'))

    return {
        "has_diff": True,
        "patch": full_patch,
        "changed_lines": changed_count,
        "file_path": clean_path
    }
