"""
================================================================================
TEST SUITE: GENESIS REVERSE MINDMAP INTERACTIVE STUDIO E2E TEST
Verifies UI, Causal Convergence, M3 Drawer, Scenario Switching & Evidence Receipt
================================================================================
"""

import os
import sys
import io

# Ensure UTF-8 output on Windows console
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

from playwright.sync_api import sync_playwright

def test_reverse_mindmap_studio():
    artifacts_dir = r"C:\Users\magic\.gemini\antigravity\brain\772fd035-315f-4cf1-9c9c-2dace4be65ad"
    os.makedirs(artifacts_dir, exist_ok=True)

    print("\n========================================================")
    print("🌟 [TEST] REVERSE MINDMAP INTERACTIVE STUDIO E2E TEST")
    print("========================================================")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 1600, "height": 900})

        # 1. ロード
        url = "http://localhost:8080/mindmap_interactive_studio.html"
        print(f"[STEP 1] Loading studio on {url} ...")
        page.goto(url)
        page.wait_for_timeout(1000)

        # 2. 初期ビュー（SWE-bench バグ真因収束）の検証
        print("\n[STEP 2] Verifying Initial Scenario (SWE-bench Bug Root Cause Convergence)...")
        title = page.inner_text("#hud-scenario-title")
        latency = page.inner_text("#hud-latency")
        confidence = page.inner_text("#hud-confidence")
        pruned = page.inner_text("#hud-pruned")

        print(f"  Title: {title}")
        print(f"  SNN Latency: {latency}")
        print(f"  Confidence: {confidence}")
        print(f"  Pruned Branches: {pruned}")

        assert "SWE-bench" in title, f"Expected SWE-bench in title, got: {title}"
        assert confidence == "99.8%", f"Expected 99.8% confidence, got: {confidence}"

        shot_initial = os.path.join(artifacts_dir, "screen_reverse_mindmap_initial_swe_bench.png")
        page.screenshot(path=shot_initial)
        print(f"  📸 Saved SWE-bench Initial View to: {shot_initial}")

        # 3. ノードクリック & M3 インスペクター展開の検証
        print("\n[STEP 3] Testing Node Selection & M3 Inspector Drawer...")
        # 中心核ノードをクリック選択
        page.evaluate("""() => {
            const studio = window.meshStudio;
            studio.selectNode(studio.centerNode);
        }""")
        page.wait_for_timeout(500)

        insp_active = page.evaluate("""() => {
            const el = document.getElementById('inspector-panel');
            return el.classList.contains('active');
        }""")
        insp_title = page.inner_text("#insp-title")
        print(f"  Inspector Active: {insp_active}")
        print(f"  Inspector Title: {insp_title}")

        assert insp_active == True, "Inspector panel must be active after node selection"

        shot_insp = os.path.join(artifacts_dir, "screen_reverse_mindmap_inspector_drawer.png")
        page.screenshot(path=shot_insp)
        print(f"  📸 Saved Inspector Drawer View to: {shot_insp}")

        # 4. 思考レシート表示 (XAI White-Box Modal)
        print("\n[STEP 4] Testing White-Box Decision Evidence Receipt Modal...")
        page.click("#btn-open-receipt")
        page.wait_for_timeout(500)

        modal_open = page.evaluate("""() => {
            const el = document.getElementById('receipt-modal');
            return el.classList.contains('open');
        }""")
        rcpt_id = page.inner_text("#rcpt-id")
        rcpt_hash = page.inner_text("#rcpt-hash")
        print(f"  Modal Open: {modal_open}")
        print(f"  Receipt ID: {rcpt_id}")
        print(f"  Proof Hash: {rcpt_hash}")

        assert modal_open == True, "Receipt modal must open on click"
        assert rcpt_id.startswith("RCPT-XAI-"), f"Invalid Receipt ID: {rcpt_id}"

        shot_rcpt = os.path.join(artifacts_dir, "screen_reverse_mindmap_evidence_receipt_modal.png")
        page.screenshot(path=shot_rcpt)
        print(f"  📸 Saved Evidence Receipt Modal to: {shot_rcpt}")

        # Escキーでモーダル閉じる
        page.keyboard.press("Escape")
        page.wait_for_timeout(300)

        # 5. シナリオ切り替え: 3D自律ドローン救助
        print("\n[STEP 5] Switching Scenario to 3D Drone Search & Rescue...")
        page.click("#tab-drone")
        page.wait_for_timeout(800)

        drone_title = page.inner_text("#hud-scenario-title")
        drone_conf = page.inner_text("#hud-confidence")
        print(f"  Title: {drone_title}, Confidence: {drone_conf}")
        assert "3D Bio-Cybernetics" in drone_title, f"Expected 3D Drone title, got: {drone_title}"

        shot_drone = os.path.join(artifacts_dir, "screen_reverse_mindmap_scenario_drone.png")
        page.screenshot(path=shot_drone)
        print(f"  📸 Saved 3D Drone Scenario View to: {shot_drone}")

        # 6. シナリオ切り替え: 医療安全 5Rプロトコル
        print("\n[STEP 6] Switching Scenario to Clinical AI 5R Protocol...")
        page.click("#tab-clinical")
        page.wait_for_timeout(800)

        med_title = page.inner_text("#hud-scenario-title")
        med_conf = page.inner_text("#hud-confidence")
        print(f"  Title: {med_title}, Confidence: {med_conf}")
        assert "Clinical AI" in med_title, f"Expected Clinical AI title, got: {med_title}"

        shot_med = os.path.join(artifacts_dir, "screen_reverse_mindmap_scenario_clinical.png")
        page.screenshot(path=shot_med)
        print(f"  📸 Saved Clinical AI Scenario View to: {shot_med}")

        browser.close()

    print("\n========================================================")
    print("🎉 ALL REVERSE MINDMAP STUDIO TESTS PASSED 100%!")
    print("========================================================")

if __name__ == "__main__":
    test_reverse_mindmap_studio()
