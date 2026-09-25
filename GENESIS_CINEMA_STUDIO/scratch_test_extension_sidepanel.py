import os
import time
from playwright.sync_api import sync_playwright

def test_sidepanel_splitter_and_gdocs():
    artifact_dir = r"C:\Users\magic\.gemini\antigravity\brain\772fd035-315f-4cf1-9c9c-2dace4be65ad"
    sidepanel_path = r"file:///G:/マイドライブ/GENESIS_ROOT/browser_extension/sidepanel.html"
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        # サイドパネルの典型的なアスペクト比（幅440px、高さ850px）
        page = browser.new_page(viewport={"width": 440, "height": 850})
        
        print(f"Navigating to {sidepanel_path}...")
        page.goto(sidepanel_path)
        page.wait_for_timeout(1500)
        
        # 1. 質問を受信させて思考ログをストリーム生成
        page.evaluate("window.sideEngine.onLiveGeminiPromptReceived('Google Search GroundingとGemini事前学習メモリを統合して、最新AlphaFold3の構造予測仕様を監査して')")
        page.wait_for_timeout(3000)
        
        # 2. ログ大画面プリセット（📜 75%）をクリック
        page.evaluate("setPanelPreset('log')")
        page.wait_for_timeout(1000)
        shot_log_preset = os.path.join(artifact_dir, "screen_sidepanel_log_maximized_75.png")
        page.screenshot(path=shot_log_preset)
        print(f"Saved: {shot_log_preset}")
        
        # 3. スプリッターをマウスドラッグして均等（50%）へ移動テスト
        splitter = page.locator("#panel-splitter")
        box = splitter.bounding_box()
        if box:
            page.mouse.move(box["x"] + box["width"] / 2, box["y"] + box["height"] / 2)
            page.mouse.down()
            page.mouse.move(box["x"] + box["width"] / 2, box["y"] + 150)
            page.mouse.up()
            page.wait_for_timeout(1000)
            
        shot_dragged = os.path.join(artifact_dir, "screen_sidepanel_drag_resized.png")
        page.screenshot(path=shot_dragged)
        print(f"Saved: {shot_dragged}")
        
        # 4. 「Google Docs 保存」を実行してトースト表示確認
        # navigator.clipboardモック
        page.evaluate("""() => {
            window.open = () => {}; // ページ遷移ブロック
            exportToGoogleDocs();
        }""")
        page.wait_for_timeout(600)
        shot_gdocs = os.path.join(artifact_dir, "screen_sidepanel_gdocs_exported_toast.png")
        page.screenshot(path=shot_gdocs)
        print(f"Saved: {shot_gdocs}")
        
        browser.close()
        print("SidePanel Splitter & Google Docs test completed successfully!")

if __name__ == "__main__":
    test_sidepanel_splitter_and_gdocs()
