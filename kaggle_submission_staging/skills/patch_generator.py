# -*- coding: utf-8 -*-
"""
GENESIS Patch Generator Skill
Formats unified diffs with proper git headers for automated evaluation.
"""

import difflib
from typing import Dict, Any

def generate_git_patch(file_path: str, original_content: str, modified_content: str) -> Dict[str, Any]:
    """
    Produces a clean git-compatible unified diff.
    """
    orig_lines = original_content.splitlines(keepends=True)
    mod_lines = modified_content.splitlines(keepends=True)

    rel_path = file_path.replace("\\", "/").lstrip("/")

    diff_lines = list(difflib.unified_diff(
        orig_lines,
        mod_lines,
        fromfile=f"a/{rel_path}",
        tofile=f"b/{rel_path}",
        n=3
    ))

    if not diff_lines:
        return {
            "has_diff": False,
            "patch": "",
            "changed_lines": 0
        }

    # Add standard git diff header
    git_header = [
        f"diff --git a/{rel_path} b/{rel_path}\n",
        f"--- a/{rel_path}\n",
        f"+++ b/{rel_path}\n"
    ]
    # Skip the difflib headers if we prepend git headers
    body_lines = [l for l in diff_lines if not l.startswith("---") and not l.startswith("+++")]
    full_patch = "".join(git_header + body_lines)

    return {
        "has_diff": True,
        "patch": full_patch,
        "changed_lines": len([l for l in body_lines if l.startswith('+') or l.startswith('-')])
    }
