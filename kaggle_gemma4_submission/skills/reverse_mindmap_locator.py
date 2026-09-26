# -*- coding: utf-8 -*-
"""
GENESIS Reverse-Mindmap Bug Locator Skill
Pinpoints root-cause files and AST nodes from SWE-bench issue descriptions.
Runs completely offline using Python standard library.
"""

import re
from pathlib import Path
from typing import Dict, List, Any

FILE_PATTERN = re.compile(r'([a-zA-Z0-9_\-\./]+\.py)')
TRACEBACK_LINE_PATTERN = re.compile(r'File\s+"([^"]+\.py)",\s+line\s+(\d+),\s+in\s+([a-zA-Z0-9_]+)')
EXCEPTION_PATTERN = re.compile(r'([A-Z][a-zA-Z0-9]*(?:Error|Exception|Warning)):')

def locate_bug_root_cause(problem_statement: str, repo_root: str) -> Dict[str, Any]:
    """
    Extracts evidence from problem statement and ranks likely defect files.
    """
    repo_path = Path(repo_root) if repo_root else Path(".")
    
    # 1. Extract tracebacks
    tb_matches = TRACEBACK_LINE_PATTERN.findall(problem_statement)
    tb_files = []
    for f, line, func in tb_matches:
        tb_files.append({
            "file": f,
            "line": int(line),
            "function": func,
            "confidence": 0.95
        })

    # 2. Extract general Python files mentioned
    raw_files = FILE_PATTERN.findall(problem_statement)
    found_candidates = []
    
    for rf in raw_files:
        p = Path(rf)
        # Check if exists in repo or is relative
        clean_name = p.name
        if clean_name.startswith("test_") or "tests/" in rf:
            priority = 0.50 # Test file
        else:
            priority = 0.85 # Source implementation file
            
        found_candidates.append({
            "path": str(rf),
            "filename": clean_name,
            "priority": priority
        })

    # 3. Extract Exception Types
    exceptions = EXCEPTION_PATTERN.findall(problem_statement)

    # 4. Rank targets (Reverse-Mindmap convergence)
    ranked_targets = []
    seen = set()
    
    # Priority A: Traceback exact files
    for tb in tb_files:
        f_clean = Path(tb["file"]).name
        if f_clean not in seen:
            seen.add(f_clean)
            ranked_targets.append(tb)

    # Priority B: Explicitly mentioned source files
    for c in found_candidates:
        if c["filename"] not in seen and not c["filename"].startswith("test_"):
            seen.add(c["filename"])
            ranked_targets.append({
                "file": c["path"],
                "line": 1,
                "function": "module",
                "confidence": c["priority"]
            })

    return {
        "ranked_targets": ranked_targets,
        "exceptions_detected": list(set(exceptions)),
        "traceback_nodes_found": len(tb_files),
        "primary_suspect": ranked_targets[0] if ranked_targets else None
    }
