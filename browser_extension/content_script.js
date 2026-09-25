// content_script.js - GENESIS μTRON XAI Tab Integration

console.log("[GENESIS XAI] Content Script Active on:", window.location.href);

// 🎯 本家 Gemini (gemini.google.com) のプロンプト送信を100%確実に検知するエンジン
function setupGeminiLiveCapture() {
    let lastTypedText = "";
    let lastSentText = "";
    let lastSentTime = 0;

    function sendPromptToSidePanel(text) {
        if (!text) return;
        text = text.trim();
        const now = Date.now();
        if (text.length < 2) return;
        if (text === lastSentText && (now - lastSentTime) < 2500) return;
        lastSentText = text;
        lastSentTime = now;
        console.log("[GENESIS XAI] Sending Prompt to SidePanel:", text);

        try {
            chrome.runtime.sendMessage({
                type: "GEMINI_LIVE_PROMPT",
                prompt: text,
                timestamp: Date.now()
            });
        } catch (e) {
            console.log("[GENESIS XAI] Runtime send error:", e);
        }

        try {
            chrome.storage.local.set({ 
                last_gemini_prompt: text, 
                prompt_time: Date.now() 
            });
        } catch (e) {}
    }

    // 1. 入力中のテキストを常時キャプチャ（Enterで空になる問題を完全防止）
    document.addEventListener('input', (e) => {
        const target = e.target;
        if (target && (target.isContentEditable || target.tagName === 'TEXTAREA' || target.tagName === 'INPUT')) {
            const val = (target.innerText || target.value || target.textContent || "").trim();
            if (val) lastTypedText = val;
        }
    }, true);

    document.addEventListener('keyup', (e) => {
        const target = e.target;
        if (target && (target.isContentEditable || target.tagName === 'TEXTAREA' || target.tagName === 'INPUT')) {
            const val = (target.innerText || target.value || target.textContent || "").trim();
            if (val) lastTypedText = val;
        }
    }, true);

    // 2. Enterキー押下検知
    window.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            const activeEl = document.activeElement;
            const currentVal = activeEl ? (activeEl.innerText || activeEl.value || activeEl.textContent || "").trim() : "";
            const textToSend = currentVal || lastTypedText;
            if (textToSend) {
                sendPromptToSidePanel(textToSend);
            }
        }
    }, true);

    // 3. 送信ボタン（紙飛行機アイコン、送信ボタン、aria-label等）クリック検知
    window.addEventListener('click', (e) => {
        const btn = e.target.closest('button, .send-button, [aria-label*="送信"], [aria-label*="Send"]');
        if (btn) {
            const activeEl = document.querySelector('div[contenteditable="true"], textarea, rich-textarea');
            const currentVal = activeEl ? (activeEl.innerText || activeEl.value || activeEl.textContent || "").trim() : "";
            const textToSend = currentVal || lastTypedText;
            if (textToSend) {
                sendPromptToSidePanel(textToSend);
            }
        }
    }, true);

    // 4. 🔥 最強の保証: MutationObserver でチャット画面の「ユーザー発言吹き出し」を自動検知
    // 画面にユーザーの質問が描画された瞬間に、そこから直接テキストを取得する！
    function scanLatestUserMessage() {
        // Geminiのユーザー発言用セレクタ候補
        const selectors = [
            '.user-query-container',
            '.user-query',
            'user-query',
            'div[data-message-author-role="user"]',
            '.query-text',
            'div[class*="user-query"]',
            'div[class*="query-content"]'
        ];

        let foundNodes = [];
        for (const sel of selectors) {
            const nodes = document.querySelectorAll(sel);
            if (nodes && nodes.length > 0) {
                foundNodes = Array.from(nodes);
                break;
            }
        }

        // フォールバック: 画面上の全要素から探す
        if (foundNodes.length === 0) {
            const allElements = document.querySelectorAll('p, div');
            for (let i = allElements.length - 1; i >= 0; i--) {
                const el = allElements[i];
                // ユーザーの質問吹き出しは通常背景が暗く、ある程度の長さのテキストを持つ
                if (el.children.length === 0 && el.innerText && el.innerText.length > 4 && el.innerText.length < 500) {
                    const text = el.innerText.trim();
                    // GeminiのシステムテキストやUIラベルを除外
                    if (!text.includes("Gemini") && !text.includes("チャット") && !text.includes("共有") && !text.includes("ログイン")) {
                        // 候補
                    }
                }
            }
        }

        if (foundNodes.length > 0) {
            const lastNode = foundNodes[foundNodes.length - 1];
            const text = (lastNode.innerText || lastNode.textContent || "").trim();
            if (text) {
                sendPromptToSidePanel(text);
            }
        }
    }

    // 初回スキャン（すでに画面に質問がある場合）
    setTimeout(scanLatestUserMessage, 1500);

    // DOM変更を常時監視
    const observer = new MutationObserver(() => {
        scanLatestUserMessage();
    });

    observer.observe(document.body, {
        childList: true,
        subtree: true
    });

    // 5. サイドパネルからの問い合わせメッセージに応答
    chrome.runtime.onMessage.addListener((msg, sender, sendResponse) => {
        if (msg.type === "REQUEST_LATEST_GEMINI_PROMPT") {
            scanLatestUserMessage();
            sendResponse({ prompt: lastSentText || lastTypedText });
        }
        return true;
    });
}

// 起動
if (window.location.hostname.includes("gemini.google.com")) {
    setupGeminiLiveCapture();
}
