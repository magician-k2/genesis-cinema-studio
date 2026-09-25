// background.js - GENESIS μTRON XAI Service Worker

// 1. ツールバーのアイコンをクリックした際に確実にサイドパネルを開く設定
chrome.sidePanel.setPanelBehavior({ openPanelOnActionClick: true }).catch(() => {});

if (chrome.action && chrome.action.onClicked) {
    chrome.action.onClicked.addListener(async (tab) => {
        try {
            await chrome.sidePanel.open({ windowId: tab.windowId });
        } catch (e) {
            console.log("[GENESIS XAI] Side panel open triggered via action click:", e);
        }
    });
}

// 2. 本家 Gemini (gemini.google.com) からのリアルタイムプロンプトをサイドパネルへ即座に転送
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    if (message.type === "GEMINI_LIVE_PROMPT") {
        console.log("[GENESIS XAI Background] Broadcast Live Prompt to SidePanel:", message.prompt);
        chrome.storage.local.set({ 
            last_gemini_prompt: message.prompt, 
            prompt_time: Date.now() 
        });
        // 接続中のサイドパネルへブロードキャスト
        chrome.runtime.sendMessage(message).catch(() => {});
        sendResponse({ status: "forwarded" });
        return true;
    }

    if (message.type === "SYNC_CONTEXT") {
        sendResponse({ status: "synced" });
        return true;
    }

    return true;
});
