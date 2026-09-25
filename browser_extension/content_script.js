// content_script.js - μTRON Tab Integration

// iframe内（サイドバー等）での重複実行を防止
if (window !== window.top) {
    // ただし、もしメインがAI Studioならリンクだけは確立しておく
    console.log("[μTRON] Neural Link (Subframe Skip)");
} else {
    console.log("[μTRON] Neural Link Active (Main Frame)");
    initCrawler();
}

const SELECTORS = {
    AISTUDIO: 'textarea.textarea-element',
    GEMINI: 'div.ql-editor[contenteditable="true"]',
    GEMINI_FALLBACK: 'div[contenteditable="true"], textarea'
};

// 🎯 本家 Gemini (gemini.google.com) のプロンプト送信を0ミリ秒でリアルタイム検知
function setupGeminiLiveCapture() {
    if (!window.location.hostname.includes("gemini.google.com")) return;
    console.log("[GENESIS XAI] Gemini Live Synchronizer Active on gemini.google.com");

    function captureAndSendPrompt() {
        const inputEl = document.querySelector(SELECTORS.GEMINI) || document.querySelector(SELECTORS.GEMINI_FALLBACK);
        if (!inputEl) return;
        const text = (inputEl.innerText || inputEl.value || "").trim();
        if (text && text.length > 1) {
            console.log("[GENESIS XAI] Captured Gemini Prompt:", text);
            chrome.runtime.sendMessage({
                type: "GEMINI_LIVE_PROMPT",
                prompt: text,
                timestamp: Date.now()
            });
            try {
                chrome.storage.local.set({ last_gemini_prompt: text, prompt_time: Date.now() });
            } catch (e) {}
        }
    }

    // 1. Enter キー（Shiftなし）検知
    window.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            captureAndSendPrompt();
        }
    }, true);

    // 2. 送信ボタンのクリック検知
    window.addEventListener('click', (e) => {
        const btn = e.target.closest('button');
        if (btn) {
            const aria = btn.getAttribute('aria-label') || '';
            const cls = btn.className || '';
            if (aria.includes('送信') || aria.includes('Send') || cls.includes('send') || btn.querySelector('mat-icon, svg')) {
                captureAndSendPrompt();
            }
        }
    }, true);
}

// 起動
if (window.location.hostname.includes("gemini.google.com")) {
    setupGeminiLiveCapture();
}

function initCrawler() {
    chrome.runtime.sendMessage({ type: "GET_CRAWL_TASK" }, (state) => {
        if (state && state.active) {
            setTimeout(() => runCrawlCycle(state), 2500);
        }
    });
}

async function runCrawlCycle(state) {
    const url = window.location.href;
    console.log(`[μTRON] Cycle Check. URL: ${url}, Target: ${state.index}`);
    
    if (url.includes('/library')) {
        console.log(`[μTRON] Library View Detected. Clicking Index: ${state.index}`);
        await new Promise(r => setTimeout(r, 2000));

        const items = Array.from(document.querySelectorAll('div, a, mat-row, tr'))
            .filter(el => el.innerText && el.innerText.includes('Created by you') && el.innerText.length < 500);

        if (state.index < items.length) {
            const item = items[state.index];
            const title = item.innerText.split('\n')[0].trim();
            
            chrome.runtime.sendMessage({
                type: "CRAWL_PROGRESS",
                current: state.index + 1,
                total: items.length,
                title: title
            });

            const clickTarget = item.querySelector('a') || item;
            clickTarget.click();
        } else {
            chrome.runtime.sendMessage({ type: "CRAWL_FINISHED" });
        }
    } else if (url.includes('/prompts/')) {
        console.log("[μTRON] Chat Detail Detected. Extracting...");
        await new Promise(r => setTimeout(r, 3000));

        let content = "";
        const platform = "AI Studio";
        if (platform === "AI Studio") {
            // AI Studio のあらゆるメッセージ要素を網羅
            const selectors = [
                '.ms-message-content', 
                '.model-response-text', 
                'section.message', 
                '.chat-content',
                '.prompt-text',
                '.response-text'
            ];
            const messages = document.querySelectorAll(selectors.join(', '));
            messages.forEach(msg => {
                content += msg.innerText + "\n\n";
            });
        }

        if (content) {
            chrome.runtime.sendMessage({
                type: "SYNC_CONTEXT",
                data: {
                    platform: "AI Studio",
                    title: document.title,
                    content: content,
                    action: "INGEST"
                }
            });
        }

        console.log("[μTRON] Extraction Done. Navigating back to Library...");
        window.location.href = "https://aistudio.google.com/library";
    }
}

chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    if (message.type === "BRAIN_PULSE" || message.type === "INJECT_CONTEXT") {
        injectIntent(message.data.intent || message.data.context);
        sendResponse({ status: "ok" });
    } else if (message.type === "EXTRACT_FULL_CHAT") {
        console.log("[μTRON] Full Extraction Requested...");
        let content = "";
        const selectors = [
            '.ms-message-content', // AI Studio
            '.model-response-text', // AI Studio
            'section.message', // AI Studio
            '.chat-content', // AI Studio
            '.prompt-text', // AI Studio
            '.response-text', // AI Studio
            '.message-content', // Gemini
            '.query-content', // Gemini
            '.response-content', // Gemini
            '.markdown', // Common
            'div[data-message-author-role]', // Common AI UI
            'div[role="presentation"]' // Common AI UI
        ];
        const messages = document.querySelectorAll(selectors.join(', '));
        messages.forEach(msg => {
            const text = msg.innerText.trim();
            if (text && text.length > 5) {
                content += text + "\n\n---\n\n";
            }
        });
        
        if (content) {
            sendResponse({ 
                status: "success", 
                platform: window.location.hostname.includes("gemini") ? "Gemini" : "AI Studio", 
                title: document.title, 
                content: content 
            });
        } else {
            sendResponse({ status: "failed", error: "No content found" });
        }
    } else if (message.type === "CRAWL_HISTORY") {
        chrome.runtime.sendMessage({ type: "START_CRAWL" });
        runCrawlCycle({ active: true, index: 0 });
        sendResponse({ status: "started" });
    } else if (message.type === "FETCH_LIST") {
        const items = Array.from(document.querySelectorAll('div, a, mat-row, tr'))
            .filter(el => el.innerText && el.innerText.includes('Created by you') && el.innerText.length < 500);
        
        const list = items.map((el, idx) => ({
            title: el.innerText.split('\n')[0].trim(),
            index: idx
        }));
        sendResponse({ status: "success", list: list });
    } else if (message.type === "FORCE_CRAWL") {
        sendResponse({ status: "received" }); // まず返事を出す
        runCrawlCycle({ active: true, index: message.index });
    } else {
        sendResponse({ status: "ignored" });
    }
    return false; // 非同期応答を行わない場合はfalse
});

function injectIntent(text) {
    if (!text) return;
    const aiStudioInput = document.querySelector(SELECTORS.AISTUDIO);
    if (aiStudioInput) {
        aiStudioInput.value += `\n\n[μTRON Context Sync]: ${text}`;
        aiStudioInput.dispatchEvent(new Event('input', { bubbles: true }));
    }
}
