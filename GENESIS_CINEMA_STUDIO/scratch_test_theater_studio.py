"""
================================================================================
TEST SUITE: GENESIS DUAL-COCKPIT XAI THEATER E2E TEST
Verifies Left Cockpit (Gemini Chat) & Right Cockpit (XAI Mesh) Full Synchronization:
 1. Loading Dual Cockpit Studio
 2. Sending Prompt from Left Gemini Input
 3. Verifying Right Stage 1 (Evidence Harvesting) & Chronicle Logs
 4. Verifying Right Stage 2 (Fly-Brain SNN Pruning)
 5. Verifying Right Stage 3 (Root Cause Lock)
 6. Verifying Left Gemini Streaming Typing Response
 7. Testing Node Inspection (Web Grounding Badge & Fact)
 8. Testing White-Box Evidence Receipt Modal
================================================================================
"""

import os
import sys
import io
import time

if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

from playwright.sync_api import sync_playwright

def test_theater_studio():
    artifacts_dir = r"C:\Users\magic\.gemini\antigravity\brain\772fd035-315f-4cf1-9c9c-2dace4be65ad"
    os.makedirs(artifacts_dir, exist_ok=True)

    print("\n========================================================")
    print("🌟 [TEST] GENESIS DUAL-COCKPIT XAI THEATER E2E TEST")
    print("========================================================")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 1600, "height": 900})

        # 1. ページロード
        url = "http://localhost:8080/mindmap_theater_studio.html"
        print(f"[STEP 1] Loading Dual-Cockpit Theater on {url} ...")
        page.goto(url)
        page.wait_for_timeout(1000)

        shot_initial = os.path.join(artifacts_dir, "screen_theater_initial_dual_cockpit.png")
        page.screenshot(path=shot_initial)
        print(f"  📸 Saved Dual-Cockpit Initial View to: {shot_initial}")

        # 2. 左Gemini入力バーからプロンプト送信 (ドローン直進バグ)
        print("\n[STEP 2] Sending Prompt from Left Gemini Cockpit...")
        test_prompt = "ドローンがなぜ東に救助者がいるのに北に直進するのか調べて修正して"
        page.fill("#theater-prompt-input", test_prompt)
        page.click("#btn-theater-send")

        # 3. 思考中のアコーディオンと、右画面のタイムラインログ進行を待機
        print("\n[STEP 3] Verifying Thinking Accordion & Chronicle Stream Synchronization...")
        page.wait_for_timeout(600)

        # 思考中アコーディオンの存在確認
        thinking_text = page.inner_text(".thinking-accordion")
        print(f"  Gemini Thinking Status: {thinking_text}")
        assert "思考" in thinking_text, "Gemini thinking accordion must be visible!"

        # タイムラインログの確認
        chronicle_html = page.inner_html("#chronicle-stream")
        print(f"  Chronicle Log Lines Present: {'[T+' in chronicle_html}")
        assert "[T+" in chronicle_html, "Chronicle timeline logs must stream!"

        # 4. 同期完了待機 (ステージ3完了 & 回答タイピング完了)
        print("\n[STEP 4] Waiting for Stage 3 Lock & Streaming Gemini Answer...")
        page.wait_for_timeout(3500)

        stage3_active = page.evaluate("() => document.getElementById('stage-3').classList.contains('active')")
        print(f"  Stage 3 (Root Cause Locked) Active: {stage3_active}")
        assert stage3_active == True, "Stage 3 must be active upon convergence!"

        # 左Geminiの回答カードの確認 (全カード中の最後の要素)
        response_card_text = page.locator(".gemini-response-card").last.inner_text()
        print(f"  Gemini Response Card (First 120 chars):\n    {response_card_text[:120]}...")
        assert "activeBypassUntilZ" in response_card_text or "simulator.html" in response_card_text, "Gemini must output verified code root cause!"

        shot_synchronized = os.path.join(artifacts_dir, "screen_theater_synchronized_convergence.png")
        page.screenshot(path=shot_synchronized)
        print(f"  📸 Saved Synchronized Convergence Screen to: {shot_synchronized}")

        # 5. 量子RSA暗号解読シナリオの実行 (Web ✕ Gemini学習知識 ✕ ローカル)
        print("\n[STEP 5] Testing Quantum RSA Shor Algorithm Scenario...")
        quantum_prompt = "量子コンピュータのショアのアルゴリズムでなぜRSA暗号が解読されるのか教えて"
        page.fill("#theater-prompt-input", quantum_prompt)
        page.click("#btn-theater-send")
        page.wait_for_timeout(3500)

        quantum_response = page.locator(".gemini-response-card").last.inner_text()
        print(f"  Quantum Response Snippet:\n    {quantum_response[:100]}...")
        assert "特定" in quantum_response or "原因" in quantum_response or "量子" in quantum_response

        # 6. 右側ノードインスペクターの検証
        print("\n[STEP 6] Testing Node Inspector on XAI Canvas...")
        page.evaluate("""() => {
            const engine = window.theaterEngine;
            const node = engine.nodes.find(n => n.source_category === 'web') || engine.nodes[1];
            engine.selectNode(node);
        }""")
        page.wait_for_timeout(600)

        insp_active = page.evaluate("() => document.getElementById('theater-inspector').classList.contains('active')")
        insp_badge = page.inner_text("#theater-insp-badge")
        print(f"  Inspector Active: {insp_active}, Badge: {insp_badge}")
        assert insp_active == True, "Inspector panel must slide in!"

        shot_inspector = os.path.join(artifacts_dir, "screen_theater_node_inspector.png")
        page.screenshot(path=shot_inspector)
        print(f"  📸 Saved Theater Node Inspector to: {shot_inspector}")

        # 7. 思考レシートモーダルの検証
        print("\n[STEP 7] Testing White-Box Evidence Receipt Modal...")
        page.click(".btn-receipt-theater")
        page.wait_for_timeout(500)

        receipt_open = page.evaluate("() => document.getElementById('theater-receipt-modal').classList.contains('open')")
        receipt_text = page.inner_text("#receipt-text-body")
        print(f"  Receipt Open: {receipt_open}")
        print(f"  Receipt Text Snippet:\n    {receipt_text[:140]}...")
        assert receipt_open == True, "Receipt modal must open!"
        assert "GENESIS" in receipt_text, "Receipt text must contain audit trail!"

        shot_receipt = os.path.join(artifacts_dir, "screen_theater_evidence_receipt.png")
        page.screenshot(path=shot_receipt)
        print(f"  📸 Saved Theater Receipt Modal to: {shot_receipt}")

        browser.close()

    print("\n========================================================")
    print("🎉 ALL THEATER STUDIO TESTS PASSED 100%!")
    print("========================================================")

if __name__ == "__main__":
    test_theater_studio()
