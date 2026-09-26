# -*- coding: utf-8 -*-
"""
================================================================================
Kaggle Gemma 4 Developer Agent Submission Builder
(build_kaggle_submission.py)
Compiles kaggle_gemma4_submission/ into official Kaggle submission.zip
================================================================================
"""

import os
import sys
import zipfile
from pathlib import Path

# Safe Windows console encoding
if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except Exception:
        pass

ROOT_DIR = Path(__file__).resolve().parent
SUBMISSION_DIR = ROOT_DIR / "kaggle_gemma4_submission"
OUTPUT_DIR = ROOT_DIR / "outputs"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

REQUIRED_SUBMISSION_FILES = [
    "agent.yaml",
    "configs/sampling.yaml",
    "prompts/system.md",
    "run_agent.py"
]

def build_kaggle_zip() -> Path:
    print("=" * 80)
    print("📦 COMPILING KAGGLE GEMMA 4 DEVELOPER AGENT SUBMISSION ZIP")
    print("=" * 80)

    # 1. Audit mandatory files
    for req in REQUIRED_SUBMISSION_FILES:
        target = SUBMISSION_DIR / req
        if not target.exists():
            print(f"❌ [MISSING] Required file missing: {req}")
            sys.exit(1)
        else:
            print(f"✅ [VERIFIED] {req}")

    # 2. Package into outputs/kaggle_gemma4_submission.zip
    out_zip = OUTPUT_DIR / "kaggle_gemma4_submission.zip"
    included_count = 0

    with zipfile.ZipFile(out_zip, 'w', zipfile.ZIP_DEFLATED) as zf:
        for root, dirs, files in os.walk(SUBMISSION_DIR):
            dirs[:] = [d for d in dirs if d not in ['__pycache__', '.git']]
            for file in files:
                if file.endswith(('.pyc', '.tmp', '.diff')):
                    continue
                full_path = Path(root) / file
                rel_path = full_path.relative_to(SUBMISSION_DIR)
                zf.write(full_path, rel_path)
                included_count += 1

    size_kb = out_zip.stat().st_size / 1024.0
    print(f"\n🎉 Package created successfully!")
    print(f"   Target ZIP : {out_zip} ({size_kb:.1f} KB, {included_count} files)")
    print("=" * 80)
    print("🚀 Ready to drag & drop directly onto Kaggle Submission page!")
    print("=" * 80)
    return out_zip

if __name__ == "__main__":
    build_kaggle_zip()
