import os
import time
from playwright.sync_api import sync_playwright

def test_rich_deep_log():
    artifact_dir = r"C:\Users\magic\.gemini\antigravity\brain\772fd035-315f-4cf1-9c9c-2dace4be65ad"
    sidepanel_path = r"file:///G:/マイドライブ/GENESIS_ROOT/browser_extension/sidepanel.html"
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 450, "height": 880})
        
        print(f"Navigating to {sidepanel_path}...")
        page.goto(sidepanel_path)
        page.wait_for_timeout(1000)
        
        # ユーザー様の生体脳の質問を送信
        prompt = "生体脳と同じ機能を持つ機械脳を作るには、どのような仕組みや機能を持たせたらいいのかな？"
        page.evaluate(f"window.sideEngine.onLiveGeminiPromptReceived('{prompt}')")
        page.wait_for_timeout(3500)
        
        # ログ大画面プリセット（📜 75%）に切り替え
        page.evaluate("setPanelPreset('log')")
        page.wait_for_timeout(1000)
        
        # スクリーンショット採取（詳細化された超リッチログ）
        shot_rich_log = os.path.join(artifact_dir, "screen_sidepanel_deep_rich_evidence_log.png")
        page.screenshot(path=shot_rich_log)
        print(f"Saved: {shot_rich_log}")
        
        browser.close()
        print("Rich Deep Log test finished successfully!")

if __name__ == "__main__":
    test_rich_deep_log()
