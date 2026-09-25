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

        # 7. プロンプト入力からの動的データ収集・判断・答えの導出テスト
        print("\n[STEP 7] Testing Dynamic Prompt Analysis, Data Harvesting & Convergence...")
        test_prompt = "ドローンがなぜ東に救助者がいるのに北に直進するのか調べて修正して"
        page.fill("#prompt-input", test_prompt)
        page.click("#btn-run-prompt")
        
        # 段階的アニメーションの完了を待機 (約1.5秒)
        page.wait_for_timeout(2000)

        prompt_title = page.inner_text("#hud-scenario-title")
        prompt_pruned = page.inner_text("#hud-pruned")
        prompt_conf = page.inner_text("#hud-confidence")
        print(f"  After Prompt Execution:")
        print(f"    Domain: {prompt_title}")
        print(f"    Pruned Branches: {prompt_pruned}")
        print(f"    Confidence: {prompt_conf}")

        assert "自律ドローン" in prompt_title or "ドローン" in prompt_title, f"Expected Drone domain, got: {prompt_title}"
        assert "branches" in prompt_pruned, f"Expected pruned branches, got: {prompt_pruned}"

        # 思考レシートを開いて、プロンプトに対応した証拠が出力されているか確認
        page.click("#btn-open-receipt")
        page.wait_for_timeout(500)
        rcpt_harvested = page.inner_text("#rcpt-harvested")
        rcpt_root = page.inner_text("#rcpt-root-cause")
        print(f"  Receipt Harvested Data: {rcpt_harvested}")
        print(f"  Receipt Converged Root: {rcpt_root}")

        assert "outer facts" in rcpt_harvested or "harvested" in rcpt_harvested
        assert "activeBypassUntilZ" in rcpt_root or "バグ" in rcpt_root

        shot_prompt = os.path.join(artifacts_dir, "screen_reverse_mindmap_prompt_dynamic_convergence.png")
        page.screenshot(path=shot_prompt)
        print(f"  📸 Saved Dynamic Prompt Convergence View to: {shot_prompt}")

        page.keyboard.press("Escape")
        page.wait_for_timeout(300)

        # 8. Python循環参照プロンプトの検証 & 具体的データ名・コード抜粋・ファクトのインスペクター検証
        print("\n[STEP 8] Testing Python Circular Import Prompt & Concrete Data/Snippet Inspector...")
        python_prompt = "Pythonコードの循環インポート例外の真因を特定して"
        page.fill("#prompt-input", python_prompt)
        page.click("#btn-run-prompt")
        page.wait_for_timeout(2000)

        # 外周ノード（symptom_1: genesis_mainframe_core.py:42）をクリック
        page.evaluate("""() => {
            const studio = window.meshStudio;
            const node = studio.nodes.find(n => n.id === 'symptom_1');
            if (node) studio.selectNode(node);
        }""")
        page.wait_for_timeout(500)

        insp_html = page.inner_html("#insp-extra")
        insp_title = page.inner_text("#insp-title")
        print(f"  Selected Node Title: {insp_title}")
        print(f"  Inspector Contains 'genesis_mainframe_core.py': {'genesis_mainframe_core.py' in insp_html}")
        print(f"  Inspector Contains Code Snippet: {'from core.reverse_mindmap_engine' in insp_html}")
        print(f"  Inspector Contains Harvested Fact: {'抽出された核心事実' in insp_html}")

        assert "genesis_mainframe_core.py" in insp_title or "genesis_mainframe_core.py" in insp_html
        assert "from core.reverse_mindmap_engine" in insp_html, "Must display concrete code snippet in inspector!"
        assert "抽出された核心事実" in insp_html, "Must display extracted factual evidence!"

        shot_snippet = os.path.join(artifacts_dir, "screen_reverse_mindmap_concrete_code_snippet_inspector.png")
        page.screenshot(path=shot_snippet)
        print(f"  📸 Saved Concrete Data & Code Snippet View to: {shot_snippet}")

        # インスペクターを閉じる
        page.keyboard.press("Escape")
        page.wait_for_timeout(400)

        # 9. プロンプトバー折りたたみ・最小化トグルの検証
        print("\n[STEP 9] Testing Floating Prompt Bar Minimize / Expand Toggle...")
        bar_minimized_before = page.evaluate("() => document.querySelector('.prompt-control-bar').classList.contains('minimized')")
        print(f"  Prompt Bar Minimized Before: {bar_minimized_before}")
        assert bar_minimized_before == False, "Prompt bar should initially be expanded"

        page.click("#btn-toggle-prompt")
        page.wait_for_timeout(400)
        bar_minimized_after = page.evaluate("() => document.querySelector('.prompt-control-bar').classList.contains('minimized')")
        print(f"  Prompt Bar Minimized After: {bar_minimized_after}")
        assert bar_minimized_after == True, "Prompt bar should be minimized after clicking toggle button"

        shot_minimized = os.path.join(artifacts_dir, "screen_reverse_mindmap_prompt_minimized.png")
        page.screenshot(path=shot_minimized)
        print(f"  📸 Saved Minimized Prompt Bar View to: {shot_minimized}")

        # 展開に戻す
        page.click("#btn-toggle-prompt")
        page.wait_for_timeout(300)

        # 10. Zoom コントロール & Pan ドラッグの検証
        print("\n[STEP 10] Testing Canvas Pan & Smooth Zoom Controls...")
        # ズーム前のカメラズーム値
        zoom_init = page.evaluate("() => window.meshStudio.camera.zoom")
        print(f"  Initial Zoom: {zoom_init:.2f}")

        # 拡大ボタンを2回クリック
        page.click("button[title*='拡大']")
        page.wait_for_timeout(200)
        page.click("button[title*='拡大']")
        page.wait_for_timeout(600)
        zoom_zoomed = page.evaluate("() => window.meshStudio.camera.zoom")
        print(f"  After 2x Zoom In: {zoom_zoomed:.2f}")
        assert zoom_zoomed > zoom_init, f"Zoom should have increased: {zoom_zoomed} > {zoom_init}"

        # キャンバスドラッグ (Pan)
        canvas_box = page.locator("#mindmap-canvas").bounding_box()
        page.mouse.move(canvas_box["x"] + 400, canvas_box["y"] + 300)
        page.mouse.down()
        page.mouse.move(canvas_box["x"] + 250, canvas_box["y"] + 200, steps=5)
        page.mouse.up()
        page.wait_for_timeout(400)

        cam_pan_x = page.evaluate("() => window.meshStudio.camera.x")
        cam_pan_y = page.evaluate("() => window.meshStudio.camera.y")
        print(f"  After Canvas Pan: Camera X={cam_pan_x:.1f}, Camera Y={cam_pan_y:.1f}")

        # 視点リセットボタンをクリック
        page.click("button[title*='リセット']")
        page.wait_for_timeout(600)
        cam_reset_zoom = page.evaluate("() => window.meshStudio.camera.targetZoom")
        print(f"  After Reset View: Target Zoom={cam_reset_zoom:.2f}")
        assert abs(cam_reset_zoom - 1.0) < 0.05, f"Target zoom should reset to 1.0, got: {cam_reset_zoom}"

        # 11. ノード選択時のカメラ自動左スライド（インスペクター被り完全解消）の検証
        print("\n[STEP 11] Testing Camera Auto-Slide when Inspector Opens (No UI Occlusion)...")
        # ノード未選択状態
        page.evaluate("() => window.meshStudio.selectNode(null)")
        page.wait_for_timeout(400)
        cam_target_center = page.evaluate("() => window.meshStudio.camera.targetX")
        print(f"  Camera Target X (No Inspector): {cam_target_center}")
        assert cam_target_center == 0, f"Expected Target X = 0, got {cam_target_center}"

        # 外周ノードを選択してインスペクターを開く
        page.evaluate("""() => {
            const studio = window.meshStudio;
            const node = studio.nodes.find(n => n.id === 'symptom_2') || studio.nodes[1];
            studio.selectNode(node);
        }""")
        page.wait_for_timeout(700)
        cam_target_slide = page.evaluate("() => window.meshStudio.camera.targetX")
        cam_current_x = page.evaluate("() => window.meshStudio.camera.x")
        print(f"  Camera Target X (Inspector Active): {cam_target_slide}")
        print(f"  Camera Current X: {cam_current_x:.1f}")
        assert cam_target_slide == -180, f"Camera Target X should be -180 to prevent occlusion, got: {cam_target_slide}"
        assert cam_current_x < -100, f"Camera should have smoothly lerped left, got: {cam_current_x}"

        shot_collision_free = os.path.join(artifacts_dir, "screen_reverse_mindmap_collision_free_pan_zoom.png")
        page.screenshot(path=shot_collision_free)
        print(f"  📸 Saved Collision-Free Pan/Zoom/Slide View to: {shot_collision_free}")

        browser.close()

    print("\n========================================================")
    print("🎉 ALL REVERSE MINDMAP STUDIO TESTS PASSED 100%!")
    print("========================================================")

if __name__ == "__main__":
    test_reverse_mindmap_studio()
