import os
import time
from playwright.sync_api import sync_playwright

def test_sidepanel():
    artifact_dir = r"C:\Users\magic\.gemini\antigravity\brain\772fd035-315f-4cf1-9c9c-2dace4be65ad"
    sidepanel_path = r"file:///G:/マイドライブ/GENESIS_ROOT/browser_extension/sidepanel.html"
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 440, "height": 850})
        
        print(f"Navigating to {sidepanel_path}...")
        page.goto(sidepanel_path)
        page.wait_for_timeout(1500)
        
        # 1. 初期ドローンシナリオ
        shot_initial = os.path.join(artifact_dir, "screen_sidepanel_initial_cockpit.png")
        page.screenshot(path=shot_initial)
        print(f"Saved: {shot_initial}")
        
        # 2. 本家Geminiでの新しい質問（Web検索グラウンディング重視）をリアルタイム受信シミュレーション
        page.evaluate("window.sideEngine.onLiveGeminiPromptReceived('Google Search GroundingとGemini最新学習データを活用して、2026年最新のAlphaFold3分子構造を可視化して')")
        page.wait_for_timeout(3500)
        shot_grounding = os.path.join(artifact_dir, "screen_sidepanel_live_prompt_grounding.png")
        page.screenshot(path=shot_grounding)
        print(f"Saved: {shot_grounding}")
        
        # 3. エビデンス受領書モーダルを開く
        page.evaluate("openReceiptModal()")
        page.wait_for_timeout(1000)
        shot_receipt = os.path.join(artifact_dir, "screen_sidepanel_evidence_receipt_modal.png")
        page.screenshot(path=shot_receipt)
        print(f"Saved: {shot_receipt}")
            
        browser.close()
        print("Sidepanel test finished successfully!")

if __name__ == "__main__":
    test_sidepanel()
