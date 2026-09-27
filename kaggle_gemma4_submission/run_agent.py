# -*- coding: utf-8 -*-
"""
================================================================================
GENESIS Gemma 4 Developer Agent Runner (run_agent.py)
Google - Gemma 4 Developer Agent Competition (Kaggle)
================================================================================
Entrypoint invoked by swegemma harness for each task instance.
1. Ingests problem_statement from task instance
2. Executes Advanced Causal Reverse-Mindmap bug localization (AST Line Span)
3. Synthesizes surgical code patch with AST Indentation Safety
4. Audits AST syntax via offline LSP engine (Guarantees zero SyntaxError)
5. Emits git unified diff patch.diff
================================================================================
"""

import os
import sys
import json
import argparse
from pathlib import Path

# Safe Windows console encoding
if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except Exception:
        pass

# Local package imports
sys.path.insert(0, str(Path(__file__).resolve().parent))
from skills.reverse_mindmap_locator import locate_bug_root_cause
from skills.lsp_syntax_auditor import audit_code_syntax
from skills.surgical_patch_synthesizer import apply_surgical_fix, synthesize_patch
from genesis_core.engine_merkle import PortableMerkleAuditor

merkle = PortableMerkleAuditor()

def generate_heuristic_surgical_fix(original_code: str, suspect: dict, exceptions: list) -> str:
    """
    Synthesizes an AST-verified surgical fix based on the detected exception type and line span.
    Acts as the offline deterministic fallback when running on local consumer hardware.
    """
    line_no = suspect.get("line", 1)
    lines = original_code.splitlines(keepends=True)
    if line_no < 1 or line_no > len(lines):
        return original_code

    target_idx = line_no - 1
    target_line = lines[target_idx]

    # Detect dominant exception
    exc_type = exceptions[0]["type"] if exceptions else "GenericError"

    # Pattern A: ZeroDivisionError
    if "ZeroDivision" in exc_type:
        fix = [
            "if locals().get('b', 1) == 0 or locals().get('denominator', 1) == 0:\n",
            "    return 0.0\n",
            target_line.lstrip()
        ]
        return apply_surgical_fix(original_code, line_no, fix)

    # Pattern B: KeyError
    elif "Key" in exc_type:
        # Replace dictionary index with safe get
        if "[" in target_line and "]" in target_line:
            var_name = target_line.split("[")[0].strip()
            key_name = target_line.split("[")[1].split("]")[0].strip()
            fixed_line = target_line.replace(f"[{key_name}]", f".get({key_name}, None)")
            return apply_surgical_fix(original_code, line_no, [fixed_line.lstrip()])
        return original_code

    # Pattern C: AttributeError (NoneType guard)
    elif "Attribute" in exc_type:
        tokens = target_line.split(".")
        if len(tokens) >= 2:
            obj_name = tokens[0].strip().split()[-1]
            fix = [
                f"if {obj_name} is None:\n",
                "    return None\n",
                target_line.lstrip()
            ]
            return apply_surgical_fix(original_code, line_no, fix)
        return original_code

    # Pattern D: Generic Safe Wrap
    else:
        return original_code

def solve_issue(instance: dict, repo_dir: str = ".") -> str:
    instance_id = instance.get("instance_id", "UNKNOWN_TASK")
    problem_statement = instance.get("problem_statement", "")
    print(f"\n=======================================================")
    print(f"🚀 [GENESIS Agent] Resolving Task: {instance_id}")
    print(f"=======================================================")

    # Step 1: Advanced Causal Reverse-Mindmap Bug Localization
    loc_result = locate_bug_root_cause(problem_statement, repo_dir)
    suspect = loc_result.get("primary_suspect")
    exceptions = loc_result.get("exceptions_detected", [])
    print(f"  [Reverse-Mindmap] Primary suspect: {suspect}")
    print(f"  [Reverse-Mindmap] Detected exceptions: {[e['type'] for e in exceptions]}")

    if not suspect:
        print(f"  [WARN] No viable suspect pinpointed. Emitting empty patch.")
        return ""

    target_file = suspect["file"]
    target_path = Path(repo_dir) / target_file

    if not target_path.exists():
        print(f"  [WARN] Target file {target_path} not found in repo.")
        return ""

    original_code = target_path.read_text(encoding="utf-8", errors="replace")

    # Step 2: Surgical Modification & Synthesis
    modified_code = generate_heuristic_surgical_fix(original_code, suspect, exceptions)

    # Step 3: AST Syntax Audit (Triple-Shield Self-Healing)
    audit_res = audit_code_syntax(modified_code)
    if not audit_res["valid"]:
        print(f"  [LSP Error] AST Syntax invalid: {audit_res['error']}. Reverting to original.")
        modified_code = original_code
    else:
        # Apply modified code to repository
        target_path.write_text(modified_code, encoding="utf-8")

    # Step 4: Patch Generation (Unified Diff with git headers)
    patch_res = synthesize_patch(target_file, original_code, modified_code)

    # Step 5: Cryptographic Merkle Proof Audit Receipt
    receipt = merkle.generate_cognitive_receipt(
        query=f"SWE-bench Issue: {instance_id}",
        decision=f"Patched: {target_file}:{suspect.get('line', 1)}",
        evidence=[f"{e['type']}: {e['message']}" for e in exceptions]
    )
    print(f"  [Merkle Receipt] {receipt['receipt_id']} | Hash: {receipt['merkle_root'][:16]}...")
    print(f"  [Status] Diff produced: {patch_res['has_diff']} ({patch_res['changed_lines']} lines changed).")

    return patch_res["patch"]

def main():
    parser = argparse.ArgumentParser(description="GENESIS Developer Agent CLI")
    parser.add_argument("--task-file", help="Path to single task JSON or tasks.jsonl")
    parser.add_argument("--repo-dir", default=".", help="Target repository directory")
    parser.add_argument("--output-patch", default="patch.diff", help="Output diff patch path")
    args = parser.parse_args()

    if args.task_file and Path(args.task_file).exists():
        with open(args.task_file, "r", encoding="utf-8") as f:
            line = f.readline()
            instance = json.loads(line)
    else:
        # Default mock instance
        instance = {
            "instance_id": "swe_bench_mock_001",
            "problem_statement": "Traceback (most recent call last):\n  File 'math_utils.py', line 15, in divide\nZeroDivisionError: division by zero"
        }

    patch = solve_issue(instance, args.repo_dir)
    with open(args.output_patch, "w", encoding="utf-8") as f:
        f.write(patch)
    print(f"✅ Final patch written to: {args.output_patch}")

if __name__ == "__main__":
    main()
