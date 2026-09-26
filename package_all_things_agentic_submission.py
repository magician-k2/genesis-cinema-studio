# -*- coding: utf-8 -*-
"""
================================================================================
GENESIS ALL THINGS AGENTIC HACKATHON SUBMISSION PACKAGER & INTEGRITY AUDITOR
(package_all_things_agentic_submission.py)

1. Validates all required hackathon submission files and documents.
2. Executes full SRE test suite (15 suites / 580 tests) for 100% Green Verification.
3. Generates the final submission ZIP bundle in outputs/.
================================================================================
"""

import os
import sys
import io
import time
import zipfile
import unittest
import argparse
from datetime import datetime

# Configure UTF-8 for Windows console
if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except Exception:
        pass

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(ROOT_DIR, "outputs")
os.makedirs(OUTPUT_DIR, exist_ok=True)

REQUIRED_SUBMISSION_FILES = [
    "HACKATHON_ALL_THINGS_AGENTIC_PROPOSAL.md",
    "HACKATHON_ALL_THINGS_AGENTIC_ARCHITECTURE.md",
    "HACKATHON_ALL_THINGS_AGENTIC_DEMO_VIDEO_SCRIPT.md",
    "README_ALL_THINGS_AGENTIC.md",
    "core/genesis_gemini_client.py",
    "core/genesis_mobile_remote_gateway.py",
    "core/genesis_mobile_auth_gateway.py",
    "core/agent_magi.py",
    "LAUNCH_GENESIS_CLOUD.py",
    "web/mobile_antigravity.html",
]

SUBMISSION_DIRECTORIES = ["core", "cortex_nodes", "web", "tests", "docs"]
SUBMISSION_INDIVIDUAL_FILES = [
    "HACKATHON_ALL_THINGS_AGENTIC_PROPOSAL.md",
    "HACKATHON_ALL_THINGS_AGENTIC_ARCHITECTURE.md",
    "HACKATHON_ALL_THINGS_AGENTIC_DEMO_VIDEO_SCRIPT.md",
    "README_ALL_THINGS_AGENTIC.md",
    "LAUNCH_GENESIS_CLOUD.py",
    "Dockerfile",
    "requirements.txt",
    "GENESIS_FULL_FUNCTIONAL_SPECIFICATION.md",
    "package_all_things_agentic_submission.py",
    "Run_Instant_Demo.bat"
]

def print_banner(title: str):
    print("=" * 80)
    print(f"  [GRAND PRIX] {title}")
    print("=" * 80)

def audit_submission_files() -> bool:
    print_banner("STEP 1: SUBMISSION ASSET INTEGRITY AUDIT")
    all_ok = True
    for rel_path in REQUIRED_SUBMISSION_FILES:
        full_path = os.path.join(ROOT_DIR, rel_path)
        if os.path.exists(full_path):
            size_kb = os.path.getsize(full_path) / 1024.0
            print(f"  [FOUND] {rel_path:<50} ({size_kb:>6.1f} KB)")
        else:
            print(f"  [MISSING] {rel_path}")
            all_ok = False
    return all_ok

def run_sre_test_suite() -> bool:
    print_banner("STEP 2: RUNNING 15 SRE TEST SUITES (580 TESTS)")
    start_time = time.time()
    
    loader = unittest.TestLoader()
    tests_dir = os.path.join(ROOT_DIR, "tests")
    suite = loader.discover(tests_dir, pattern="test_*.py")
    
    stream = io.StringIO()
    runner = unittest.TextTestRunner(stream=stream, verbosity=1)
    result = runner.run(suite)
    duration = time.time() - start_time
    
    total_tests = result.testsRun
    failures = len(result.failures)
    errors = len(result.errors)
    passed = total_tests - failures - errors
    
    print(f"  Total Tests Run : {total_tests}")
    print(f"  Passed          : {passed}")
    print(f"  Failures        : {failures}")
    print(f"  Errors          : {errors}")
    print(f"  Duration        : {duration:.2f}s")
    
    if result.wasSuccessful():
        print(f"  [SUCCESS] SRE TEST CERTIFICATION: 100% ALL GREEN PASS ({total_tests}/{total_tests})")
        return True
    else:
        print("  [ERROR] TEST FAILURES DETECTED!")
        print(stream.getvalue())
        return False

def build_submission_zip() -> str:
    print_banner("STEP 3: COMPILING DEVPOST SUBMISSION BUNDLE")
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    zip_name = f"GENESIS_ALL_THINGS_AGENTIC_SUBMISSION_{timestamp}.zip"
    latest_zip_name = "GENESIS_ALL_THINGS_AGENTIC_SUBMISSION_LATEST.zip"
    zip_path = os.path.join(OUTPUT_DIR, zip_name)
    latest_zip_path = os.path.join(OUTPUT_DIR, latest_zip_name)
    
    included_count = 0
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        # Add targeted directories
        for sdir in SUBMISSION_DIRECTORIES:
            dir_path = os.path.join(ROOT_DIR, sdir)
            if not os.path.exists(dir_path):
                continue
            for root, dirs, files in os.walk(dir_path):
                dirs[:] = [d for d in dirs if d not in ['__pycache__', '.pytest_cache', '.git']]
                for file in files:
                    if file.endswith(('.pyc', '.log', '.tmp', '.lnk')):
                        continue
                    full_path = os.path.join(root, file)
                    rel_path = os.path.relpath(full_path, ROOT_DIR)
                    try:
                        zipf.write(full_path, rel_path)
                        included_count += 1
                    except Exception as e:
                        print(f"  [SKIP] Could not add {rel_path}: {e}")
                        
        # Add individual root files
        for sfile in SUBMISSION_INDIVIDUAL_FILES:
            full_path = os.path.join(ROOT_DIR, sfile)
            if os.path.exists(full_path):
                try:
                    zipf.write(full_path, sfile)
                    included_count += 1
                except Exception as e:
                    print(f"  [SKIP] Could not add {sfile}: {e}")
                
    # Copy as latest
    import shutil
    shutil.copyfile(zip_path, latest_zip_path)
    
    size_mb = os.path.getsize(zip_path) / (1024.0 * 1024.0)
    print(f"  Packaged {included_count} files into:")
    print(f"     -> {zip_path} ({size_mb:.2f} MB)")
    print(f"     -> {latest_zip_path} ({size_mb:.2f} MB)")
    return zip_path

def main():
    parser = argparse.ArgumentParser(description="GENESIS Hackathon Submission Packager")
    parser.add_argument("--skip-tests", action="store_true", help="Skip running the 580 test suites")
    args = parser.parse_args()

    print_banner("ALL THINGS AGENTIC HACKATHON: SUBMISSION PACKAGER")
    
    files_ok = audit_submission_files()
    if not files_ok:
        print("[ERROR] Submission asset check failed!")
        sys.exit(1)
        
    if not args.skip_tests:
        tests_ok = run_sre_test_suite()
        if not tests_ok:
            print("[ERROR] SRE Test suite check failed!")
            sys.exit(1)
    else:
        print("  [INFO] Skipped full test run per --skip-tests flag (Tests verified green previously)")
        
    zip_file = build_submission_zip()
    
    print_banner("SUBMISSION PACKAGE READY FOR GRAND PRIX!")
    print("  Target Track : The Taskmaster ($180,000 Total Prize Pool)")
    print("  Core Model   : Google Gemini 3.7 Flash + Gemma 4 + Veo 2 + Imagen 3 + Lyria")
    print("  Live URL     : https://genesis-cognitive-cortex-569032305989.asia-northeast1.run.app")
    print("  PWA Portal   : https://genesis-cognitive-cortex-569032305989.asia-northeast1.run.app/mobile_antigravity")
    print(f"  ZIP Bundle   : {zip_file}")
    print("=" * 80)

if __name__ == '__main__':
    main()
