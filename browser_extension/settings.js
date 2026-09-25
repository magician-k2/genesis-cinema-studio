/* settings.js – Google API 設定ウィザード (配布用セキュア鍵注入 + 開発者フルオート対応) */

// ==========================================
// 🛠️ 開発者（magician.k2）専用 フルオート設定
// ==========================================
// ここにキーを設定しておくと、設定画面を開いた瞬間に自動タイピング＆自動接続が走ります。
// ※ 【重要】一般ユーザーに配布する際は、必ずここを空（""）に戻してください。
const DEV_CLIENT_ID = "";
const DEV_CLIENT_SECRET = "";
// ==========================================

const apiElems = {
    docs:   document.getElementById('api-docs'),
    drive:  document.getElementById('api-drive'),
    sheets: document.getElementById('api-sheets'),
    gemini: document.getElementById('api-gemini')
};
const authRadios = document.getElementsByName('auth');
const oauthBtn   = document.getElementById('btn-auth-oauth');
const saInput    = document.getElementById('sa-file');
const saStatus   = document.getElementById('sa-status');
const saveBtn    = document.getElementById('btn-save');
const statusDiv  = document.getElementById('status');
const sdkSection = document.getElementById('sdk-section');
const codeBlock  = document.getElementById('code-snippet');
const copyBtn    = document.getElementById('btn-copy');

const inputClientId = document.getElementById('input-client-id');
const inputClientSecret = document.getElementById('input-client-secret');
const uriDisplay = document.getElementById('redirect-uri-display');
const btnCopyUri = document.getElementById('btn-copy-uri');

const dropZone = document.getElementById('drop-zone');
const jsonUpload = document.getElementById('json-upload');

/* ---------- 初期化 ---------- */
const REDIRECT_URI = chrome.identity.getRedirectURL();
uriDisplay.textContent = REDIRECT_URI;

btnCopyUri.addEventListener('click', async () => {
    await navigator.clipboard.writeText(REDIRECT_URI);
    btnCopyUri.textContent = 'コピー完了!';
    setTimeout(() => { btnCopyUri.textContent = 'コピー'; }, 2000);
});

// 保存済みの Client ID / Secret があれば復元
chrome.storage.local.get(['muTronClientId', 'muTronClientSecret'], (result) => {
    if (result.muTronClientId) inputClientId.value = result.muTronClientId;
    if (result.muTronClientSecret) inputClientSecret.value = result.muTronClientSecret;
});

// ⚡ サイバータイピング演出：ファイルから抽出したキーを自動注入
async function autoInjectKeys(clientId, clientSecret) {
    statusDiv.textContent = '⚡ マスターキーを自動解析して注入しています...';
    statusDiv.style.color = '#a78bfa';
    
    inputClientId.value = "";
    inputClientSecret.value = "";
    
    // タイピングアニメーション
    for (let i = 0; i < clientId.length; i++) {
        inputClientId.value += clientId[i];
        await new Promise(r => setTimeout(r, 10));
    }
    for (let i = 0; i < clientSecret.length; i++) {
        inputClientSecret.value += clientSecret[i];
        await new Promise(r => setTimeout(r, 10));
    }
    
    statusDiv.textContent = '✅ 自動注入完了。接続を開始します...';
    statusDiv.style.color = '#4ade80';
    
    // そのまま自動で接続ボタンを押す
    setTimeout(() => { oauthBtn.click(); }, 500);
}

/* ---------- Drag & Drop JSON 解析 ---------- */
function handleFile(file) {
    if (!file) return;
    const reader = new FileReader();
    reader.onload = async (e) => {
        try {
            const data = JSON.parse(e.target.result);
            const web = data.web || data.installed;
            if (!web || !web.client_id || !web.client_secret) throw new Error("不正なJSONファイルです");
            await autoInjectKeys(web.client_id, web.client_secret);
        } catch (err) {
            statusDiv.textContent = '⚠️ ' + err.message;
            statusDiv.style.color = '#ef4444';
        }
    };
    reader.readAsText(file);
}

dropZone.addEventListener('click', () => jsonUpload.click());
jsonUpload.addEventListener('change', (e) => handleFile(e.target.files[0]));

dropZone.addEventListener('dragover', (e) => {
    e.preventDefault();
    dropZone.style.background = 'rgba(0, 242, 255, 0.2)';
});
dropZone.addEventListener('dragleave', (e) => {
    e.preventDefault();
    dropZone.style.background = 'rgba(0, 0, 0, 0.2)';
});
dropZone.addEventListener('drop', (e) => {
    e.preventDefault();
    dropZone.style.background = 'rgba(0, 0, 0, 0.2)';
    handleFile(e.dataTransfer.files[0]);
});

// ⚡ 開発者モード：DEVキーが設定されていればページロード時にフルオート発動
if (DEV_CLIENT_ID && DEV_CLIENT_ID !== "") {
    setTimeout(() => { autoInjectKeys(DEV_CLIENT_ID, DEV_CLIENT_SECRET); }, 500);
}

/* ---------- UI 切替 ---------- */
function toggleAuthUI(){
    const val = [...authRadios].find(r=>r.checked).value;
    document.getElementById('oauth-section').style.display = (val==='oauth') ? 'block':'none';
    document.getElementById('sa-section').style.display    = (val==='sa')   ? 'block':'none';
}
authRadios.forEach(r=>r.addEventListener('change', toggleAuthUI));
toggleAuthUI();

/* ---------- AES‑GCM 暗号化 ---------- */
async function getEncryptionKey() {
    const rawKey = "mu_tron_static_32byte_key_____"; // 30 bytes
    // 32バイト(256ビット)にするため調整
    const paddedKey = (rawKey + "00").slice(0, 32); 
    const encoder = new TextEncoder();
    return await crypto.subtle.importKey(
        "raw",
        encoder.encode(paddedKey),
        { name: "AES-GCM" },
        false,
        ["encrypt", "decrypt"]
    );
}

async function encryptObj(obj){
    const data = new TextEncoder().encode(JSON.stringify(obj));
    const iv = crypto.getRandomValues(new Uint8Array(12));
    const encKey = await getEncryptionKey();
    const ct = await crypto.subtle.encrypt({name:'AES-GCM', iv}, encKey, data);
    return {iv:Array.from(iv), data:Array.from(new Uint8Array(ct))};
}

/* ---------- OAuth PKCE フロー ---------- */
oauthBtn.addEventListener('click', async () => {
    const clientId = inputClientId.value.trim();
    const clientSecret = inputClientSecret.value.trim();

    if (!clientId || !clientSecret) {
        statusDiv.textContent = '⚠️ クライアントID と クライアントシークレット を入力してください。';
        statusDiv.style.color = '#ef4444';
        return;
    }

    // Chrome Local に保存
    await chrome.storage.local.set({
        muTronClientId: clientId,
        muTronClientSecret: clientSecret
    });

    statusDiv.textContent = '🔄 認証情報を FastAPI サーバーと同期中...';
    statusDiv.style.color = '#00f2ff';

    try {
        // 1. FastAPI 側に Client Secret を送信して JSON を作らせる
        const secretRes = await fetch('http://127.0.0.1:31415/auth/save_client_secret', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({ client_id: clientId, client_secret: clientSecret })
        });
        
        if (!secretRes.ok) throw new Error('FastAPI への Secret 保存に失敗しました。サーバーが起動しているか確認してください。');

        statusDiv.textContent = '🔄 Googleの認証ポップアップを開いています...';
        
        // 2. OAuth ポップアップを開く
        const scope = encodeURIComponent('https://www.googleapis.com/auth/drive https://www.googleapis.com/auth/documents https://www.googleapis.com/auth/spreadsheets');
        const authUrl = `https://accounts.google.com/o/oauth2/v2/auth?client_id=${clientId}`
            + `&response_type=code&redirect_uri=${encodeURIComponent(REDIRECT_URI)}`
            + `&scope=${scope}&access_type=offline&code_challenge_method=plain&code_challenge=mu_tron_challenge`;

        const respUrl = await new Promise((resolve, reject) => {
            chrome.identity.launchWebAuthFlow({url:authUrl, interactive:true}, (url) => {
                if (chrome.runtime.lastError) reject(chrome.runtime.lastError);
                else resolve(url);
            });
        });
        
        const code = (new URL(respUrl)).searchParams.get('code');
        if (!code){
            throw new Error('認証コード取得失敗');
        }

        statusDiv.textContent = '🔄 アクセストークンを取得中...';

        // 3. アクセストークン取得をサーバーへ委譲
        const payload = {code, redirect_uri: REDIRECT_URI};
        const res = await fetch('http://127.0.0.1:31415/auth/oauth/token', {
            method:'POST',
            headers:{'Content-Type':'application/json'},
            body:JSON.stringify(payload)
        });
        const data = await res.json();
        
        if(data.status === 'ok') {
            statusDiv.textContent = '✅ OAuth 認証成功！ニューラル接続が確立されました。';
            statusDiv.style.color = '#4ade80';
        } else {
            throw new Error(JSON.stringify(data));
        }
    } catch(e) {
        console.error(e);
        statusDiv.textContent = '⚠️ エラー: ' + e.message;
        statusDiv.style.color = '#ef4444';
    }
});

/* ---------- Service Account アップロード ---------- */
saInput.addEventListener('change', async e => {
    const file = e.target.files[0];
    if (!file) return;
    const json = await file.text();
    const enc = await encryptObj(JSON.parse(json));
    await chrome.storage.local.set({serviceAccount: enc});
    saStatus.textContent = '✅ Service Account がローカルに保存されました';
});

/* ---------- 設定保存 & FastAPI 同期 ---------- */
saveBtn.addEventListener('click', async () => {
    const chosen = Object.entries(apiElems)
        .filter(([,el])=>el.checked)
        .map(([k])=>k);
    if (chosen.length===0){
        statusDiv.textContent = '⚠️ 少なくとも 1 つの API を選択してください';
        statusDiv.style.color = '#ef4444';
        return;
    }
    const auth = [...authRadios].find(r=>r.checked).value;
    const config = {apis: chosen, auth};
    
    statusDiv.textContent = '🔄 設定を保存中...';
    statusDiv.style.color = '#00f2ff';

    const enc = await encryptObj(config);
    await chrome.storage.local.set({muTronGoogleConfig: enc});
    
    statusDiv.textContent = '✅ 設定保存完了。SDK を生成しました！';
    statusDiv.style.color = '#4ade80';
    
    generateSDK(chosen, auth);
});

/* ---------- SDK 生成 ---------- */
async function generateSDK(apis, auth){
    try {
        const r = await fetch(`http://127.0.0.1:31415/auth/sdk_template?apis=${apis.join(',')}&auth=${auth}`);
        const data = await r.json();
        codeBlock.textContent = data.code;
        sdkSection.style.display = 'block';
    } catch(e) {
        codeBlock.textContent = "# FastAPIサーバー (http://localhost:8001) に接続できませんでした。\n# サーバーが起動しているか確認してください。\n\n# Error details: " + e.message;
        sdkSection.style.display = 'block';
    }
}

/* ---------- コピーボタン ---------- */
copyBtn.addEventListener('click', async () => {
    await navigator.clipboard.writeText(codeBlock.textContent);
    const orig = copyBtn.textContent;
    copyBtn.textContent = '✅ コピーしました！';
    setTimeout(() => { copyBtn.textContent = orig; }, 2000);
});
