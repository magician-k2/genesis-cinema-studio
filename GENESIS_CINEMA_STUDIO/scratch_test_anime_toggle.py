import os
import time
from playwright.sync_api import sync_playwright

def test_anime_toggle():
    artifact_dir = r"C:\Users\magic\.gemini\antigravity\brain\772fd035-315f-4cf1-9c9c-2dace4be65ad"
    sidepanel_path = r"file:///G:/マイドライブ/GENESIS_ROOT/browser_extension/sidepanel.html"
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 450, "height": 880})
        
        print(f"Navigating to {sidepanel_path}...")
        page.goto(sidepanel_path)
        page.wait_for_timeout(1000)
        
        # 1. 質問送信
        prompt = "生体脳と同じ機能を持つ機械脳を作るには、どのような仕組みや機能を持たせたらいいのかな？"
        page.evaluate(f"window.sideEngine.onLiveGeminiPromptReceived('{prompt}')")
        page.wait_for_timeout(3500)
        
        # 2. 「👁️ アニメ非表示」ボタンをクリックして全画面ログモードに！
        page.click("#btn-toggle-anime")
        page.wait_for_timeout(1000)
        
        shot_hidden = os.path.join(artifact_dir, "screen_sidepanel_anime_hidden_full_log.png")
        page.screenshot(path=shot_hidden)
        print(f"Saved: {shot_hidden}")
        
        # 3. 「👁️ アニメ表示」ボタンをクリックして元に戻す！
        page.click("#btn-toggle-anime")
        page.wait_for_timeout(1000)
        
        shot_restored = os.path.join(artifact_dir, "screen_sidepanel_anime_restored.png")
        page.screenshot(path=shot_restored)
        print(f"Saved: {shot_restored}")
        
        browser.close()
        print("Anime toggle test completed successfully!")

if __name__ == "__main__":
    test_anime_toggle()
