# -*- coding: utf-8 -*-
"""
GENESIS Advanced Reverse-Mindmap Bug Locator Skill
Pinpoints root-cause files, AST function nodes, and exact line spans
from issue descriptions, error logs, and repository AST structure.
Runs completely offline using Python standard library.
"""

import os
import re
import ast
from pathlib import Path
from typing import Dict, List, Any, Optional

FILE_PATTERN = re.compile(r'([a-zA-Z0-9_\-\./]+\.py)')
TRACEBACK_LINE_PATTERN = re.compile(r'File\s+["\']([^"\']+\.py)["\'],\s+line\s+(\d+)(?:,\s+in\s+([a-zA-Z0-9_]+))?')
EXCEPTION_PATTERN = re.compile(r'([A-Z][a-zA-Z0-9]*(?:Error|Exception|Warning)):?\s*(.*)')

class CodebaseASTMapper:
    """Extracts function and class definitions across repository files."""
    @staticmethod
    def map_file_symbols(file_path: Path) -> List[Dict[str, Any]]:
        symbols = []
        if not file_path.exists() or not file_path.name.endswith(".py"):
            return symbols
        try:
            content = file_path.read_text(encoding="utf-8", errors="replace")
            tree = ast.parse(content)
            for node in ast.walk(tree):
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    symbols.append({
                        "type": "function",
                        "name": node.name,
                        "line_start": node.lineno,
                        "line_end": getattr(node, "end_lineno", node.lineno),
                        "args": [a.arg for a in node.args.args]
                    })
                elif isinstance(node, ast.ClassDef):
                    symbols.append({
                        "type": "class",
                        "name": node.name,
                        "line_start": node.lineno,
                        "line_end": getattr(node, "end_lineno", node.lineno)
                    })
        except Exception:
            pass
        return symbols

def locate_bug_root_cause(problem_statement: str, repo_root: str = ".") -> Dict[str, Any]:
    """
    Performs Causal Reverse-Mindmap bug localization:
    Symptoms (Tracebacks/Exceptions) -> SNN Pruning -> AST Root Cause Lock.
    """
    repo_path = Path(repo_root) if repo_root else Path(".")

    # 1. Parse Traceback Lines
    tb_matches = TRACEBACK_LINE_PATTERN.findall(problem_statement)
    tb_candidates = []
    for f, line, func in tb_matches:
        f_clean = Path(f).name
        tb_candidates.append({
            "file": f,
            "filename": f_clean,
            "line": int(line),
            "function": func if func else "unknown",
            "confidence": 0.98
        })

    # 2. Parse General Mentions
    file_mentions = FILE_PATTERN.findall(problem_statement)
    general_candidates = []
    for fm in file_mentions:
        p = Path(fm)
        if not fm.startswith("test_") and "tests/" not in fm:
            general_candidates.append({
                "file": fm,
                "filename": p.name,
                "line": 1,
                "function": "module",
                "confidence": 0.80
            })

    # 3. Detect Exceptions and Error Messages
    exceptions = []
    for exc, msg in EXCEPTION_PATTERN.findall(problem_statement):
        exceptions.append({"type": exc, "message": msg.strip()})

    # 4. Reverse-Mindmap Causal Convergence (Rank Candidates)
    ranked = []
    seen_files = set()

    # Priority A: Tracebacks matching real files in repo
    for tb in tb_candidates:
        matched_path = None
        # Check direct or recursive match
        if (repo_path / tb["file"]).exists():
            matched_path = repo_path / tb["file"]
        else:
            matches = list(repo_path.rglob(tb["filename"]))
            if matches:
                matched_path = matches[0]

        if matched_path and tb["filename"] not in seen_files:
            seen_files.add(tb["filename"])
            symbols = CodebaseASTMapper.map_file_symbols(matched_path)
            
            # Find enclosing function
            target_func = None
            for s in symbols:
                if s["line_start"] <= tb["line"] <= s["line_end"]:
                    target_func = s
                    break

            ranked.append({
                "file": str(matched_path.relative_to(repo_path)).replace("\\", "/"),
                "full_path": str(matched_path),
                "line": tb["line"],
                "function": target_func["name"] if target_func else tb["function"],
                "func_span": [target_func["line_start"], target_func["line_end"]] if target_func else [tb["line"], tb["line"]],
                "confidence": 0.98
            })

    # Priority B: Mentioned files found in repo
    for gc in general_candidates:
        if gc["filename"] not in seen_files:
            matches = list(repo_path.rglob(gc["filename"]))
            if matches:
                seen_files.add(gc["filename"])
                target_p = matches[0]
                symbols = CodebaseASTMapper.map_file_symbols(target_p)
                ranked.append({
                    "file": str(target_p.relative_to(repo_path)).replace("\\", "/"),
                    "full_path": str(target_p),
                    "line": 1,
                    "function": symbols[0]["name"] if symbols else "module",
                    "func_span": [symbols[0]["line_start"], symbols[0]["line_end"]] if symbols else [1, 1],
                    "confidence": 0.85
                })

    return {
        "primary_suspect": ranked[0] if ranked else None,
        "ranked_targets": ranked,
        "exceptions_detected": exceptions,
        "total_targets_evaluated": len(ranked)
    }
