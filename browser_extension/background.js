// background.js - μTRON Brain Bridge Service Worker

let bridgeSocket = null;
const BRIDGE_URL = "ws://127.0.0.1:31415/bridge";

// クロール状態管理
let crawlState = {
    active: false,
    index: 0,
    total: 0,
    tabId: null
};

// 脳（ローカルブリッジ）との接続
function connectToBrain() {
    try {
        bridgeSocket = new WebSocket(BRIDGE_URL);
        bridgeSocket.onopen = () => {
            console.log("[μTRON] Connected to Local Brain");
            chrome.storage.session.set({ bridgeStatus: "connected" });
        };
        bridgeSocket.onmessage = (event) => {
            const data = JSON.parse(event.data);
            chrome.runtime.sendMessage({ type: "BRAIN_PULSE", data: data }).catch(() => {});
        };
        bridgeSocket.onclose = () => {
            chrome.storage.session.set({ bridgeStatus: "disconnected" });
            setTimeout(connectToBrain, 5000);
        };
    } catch (e) {
        setTimeout(connectToBrain, 5000);
    }
}
connectToBrain();

// サイドパネル設定
chrome.sidePanel.setPanelBehavior({ openPanelOnActionClick: true }).catch(() => {});

// メッセージハンドリング
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    // 0. 本家 Gemini (gemini.google.com) からのリアルタイムプロンプトをサイドパネルへ即座に転送
    if (message.type === "GEMINI_LIVE_PROMPT") {
        console.log("[μTRON Background] Broadcast Live Prompt to SidePanel:", message.prompt);
        chrome.storage.local.set({ last_gemini_prompt: message.prompt, prompt_time: Date.now() });
        chrome.runtime.sendMessage(message).catch(() => {});
        sendResponse({ status: "forwarded" });
        return true;
    }

    // 1. 通常のコンテキスト同期 / インジェスト
    if (message.type === "SYNC_CONTEXT") {
        if (message.data && message.data.action === "INGEST") {
            fetch("http://127.0.0.1:31415/ingest", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    platform: message.data.platform,
                    title: message.data.title,
                    content: message.data.content
                })
            });
        } else if (bridgeSocket && bridgeSocket.readyState === WebSocket.OPEN) {
            bridgeSocket.send(JSON.stringify(message.data));
        }
    }

    // 2. クロール開始司令
    if (message.type === "START_CRAWL") {
        crawlState.active = true;
        crawlState.index = 0;
        crawlState.tabId = sender.tab ? sender.tab.id : message.tabId;
        console.log("[μTRON] Crawl Process Started.");
    }

    // 3. ページ側からの「次は何をすればいい？」への回答
    if (message.type === "GET_CRAWL_TASK") {
        sendResponse(crawlState);
    }

    // 4. 進捗報告の転送（サイドパネルへ）
    if (message.type === "CRAWL_PROGRESS") {
        crawlState.index = message.current;
        crawlState.total = message.total;
        chrome.runtime.sendMessage(message).catch(() => {});
    }

    // 5. 完了報告
    if (message.type === "CRAWL_FINISHED") {
        crawlState.active = false;
        chrome.runtime.sendMessage({ type: "CRAWL_FINISHED" }).catch(() => {});
    }

    return true;
});
