import os
import time
from playwright.sync_api import sync_playwright

def test_ultra_deep_xai():
    artifact_dir = r"C:\Users\magic\.gemini\antigravity\brain\772fd035-315f-4cf1-9c9c-2dace4be65ad"
    sidepanel_path = r"file:///G:/マイドライブ/GENESIS_ROOT/browser_extension/sidepanel.html"
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 460, "height": 950})
        
        print(f"Navigating to {sidepanel_path}...")
        page.goto(sidepanel_path)
        page.wait_for_timeout(1000)
        
        # 生体脳の質問を送信
        prompt = "生体脳と同じ機能を持つ機械脳を作るには、どのような仕組みや機能を持たせたらいいのかな？"
        page.evaluate(f"window.sideEngine.onLiveGeminiPromptReceived('{prompt}')")
        page.wait_for_timeout(4000)
        
        # 1. 通常アニメあり + 75%ログでのスクリーンショット
        page.evaluate("setPanelPreset('log')")
        page.wait_for_timeout(800)
        shot_ultra_75 = os.path.join(artifact_dir, "screen_sidepanel_ultra_deep_75.png")
        page.screenshot(path=shot_ultra_75)
        print(f"Saved: {shot_ultra_75}")
        
        # 2. ログ100%全画面モード（アニメ非表示）でのスクリーンショット
        page.evaluate("setPanelPreset('full')")
        page.wait_for_timeout(800)
        shot_ultra_full = os.path.join(artifact_dir, "screen_sidepanel_ultra_deep_full.png")
        page.screenshot(path=shot_ultra_full)
        print(f"Saved: {shot_ultra_full}")
        
        # 3. ログの最上部（Symptom 1 & 2: セマンティック照合グリッド）のスクリーンショット
        page.evaluate("document.getElementById('side-chronicle').scrollTop = 0")
        page.wait_for_timeout(600)
        shot_ultra_diff = os.path.join(artifact_dir, "screen_sidepanel_ultra_deep_diff.png")
        page.screenshot(path=shot_ultra_diff)
        print(f"Saved: {shot_ultra_diff}")
        
        browser.close()
        print("ULTRA DEEP XAI 4.0 visual verification complete!")

if __name__ == "__main__":
    test_ultra_deep_xai()
