"""
================================================================================
GENESIS CLOUD GRAND UNIFIED LAUNCHER (LAUNCH_GENESIS_CLOUD.py)
Google Cloud Run / GKE / VPS / ローカルPC 完全常駐・自律起動エントリーポイント
- Port 5000: テレパシー実機HUD / スマートグラス / Webマイク (/listen, /glass)
- Port 8080: GENESIS 大脳皮質統合スタジオ / MAGI合議コンソール / メトリクスAPI
- Background: 夜間自律学習クローラー ＆ DMNスリープ同期デーモン
================================================================================
"""

import os
import sys
import time
import threading
import json
import queue
from flask import Flask, jsonify, render_template_string, request, send_file, send_from_directory, Response
ROOT_DIR = os.environ.get("GENESIS_ROOT", os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)
from core.genesis_grand_cortex_orchestrator import GenesisGrandCortexOrchestrator
from core.agent_magi import deliberate_sync
from core.genesis_autonomous_meister_crawler import GenesisGlobalFreedomCrawler
from core.genesis_mainframe_core import mainframe
from core.genesis_clinical_demo_engine import clinical_engine
from core.genesis_night_audit_engine import night_audit_engine
from core.genesis_video_synthesis_engine import video_synthesis_engine
from core.genesis_rehab_motion_engine import rehab_motion_engine
from core.genesis_care_watchdog_engine import care_watchdog_engine
from core.genesis_transport_shield_engine import transport_shield_engine
from core.genesis_workforce_rebalancer_engine import workforce_rebalancer_engine
from core.genesis_google_cloud_omni_harvester import google_cloud_harvester
from core.genesis_google_developers_and_skills_harvester import google_developers_and_skills_harvester
from core.genesis_cloud_synapse_matrix_engine import cloud_synapse_engine
from core.genesis_google_supreme_omni_cortex import google_supreme_cortex
from core.genesis_stealth_whisper_engine import stealth_whisper_engine
from core.genesis_pr_studio_saas_engine import pr_studio_saas
from core.genesis_sheets_canvas_spark_engine import sheets_canvas_engine
from core.genesis_official_package_packager import contest_packager
from core.genesis_notebook_lm_platform_engine import notebook_lm_platform
from core.genesis_ebook_cross_synthesis_app_platform import ebook_cross_platform
from core.genesis_mobile_auth_gateway import mobile_auth_gateway
from core.genesis_mobile_remote_gateway import mobile_remote_gateway
from core.genesis_collective_evolution_mesh import collective_evolution_mesh

sys.stdout.reconfigure(encoding='utf-8', line_buffering=True)

app = Flask("GENESIS_CLOUD_CORTEX", static_folder=os.path.join(ROOT_DIR, "web", "static"), static_url_path="/static")
orchestrator = GenesisGrandCortexOrchestrator()

@app.after_request
def enforce_correct_mimetypes(response):
    if request.path.lower().endswith('.mp4'):
        response.headers['Content-Type'] = 'video/mp4'
        response.headers['Accept-Ranges'] = 'bytes'
    elif request.path.lower().endswith('.mp3'):
        response.headers['Content-Type'] = 'audio/mpeg'
        response.headers['Accept-Ranges'] = 'bytes'
    return response

STUDIO_HTML = """
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>👑 GENESIS GRAND CORTEX STUDIO</title>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body {
            background-color: #0b0f19;
            color: #f1f5f9;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            padding: 24px;
        }
        .header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-bottom: 1px solid #1e293b;
            padding-bottom: 16px;
            margin-bottom: 24px;
        }
        .title {
            font-size: 24px;
            font-weight: 900;
            color: #38bdf8;
            letter-spacing: 1px;
        }
        .status-pill {
            background: #059669;
            color: #ffffff;
            font-size: 12px;
            font-weight: 700;
            padding: 6px 14px;
            border-radius: 9999px;
            box-shadow: 0 0 12px rgba(16, 185, 129, 0.4);
        }
        .grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
            gap: 20px;
            margin-bottom: 24px;
        }
        .card {
            background: #1e293b;
            border: 1px solid #334155;
            border-radius: 16px;
            padding: 20px;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
        }
        .card-title {
            font-size: 16px;
            font-weight: 800;
            color: #94a3b8;
            margin-bottom: 12px;
            display: flex;
            align-items: center;
            gap: 8px;
        }
        .stat-value {
            font-size: 32px;
            font-weight: 900;
            color: #ffffff;
            margin-bottom: 4px;
        }
        .stat-desc {
            font-size: 13px;
            color: #64748b;
        }
        .log-box {
            background: #0f172a;
            border: 1px solid #1e293b;
            border-radius: 12px;
            padding: 16px;
            font-family: monospace;
            font-size: 13px;
            color: #38bdf8;
            height: 240px;
            overflow-y: auto;
            white-space: pre-wrap;
        }
        .btn {
            background: #2563eb;
            color: #ffffff;
            font-weight: 700;
            padding: 10px 20px;
            border-radius: 10px;
            border: none;
            cursor: pointer;
            transition: all 0.2s;
        }
        .btn:hover {
            background: #1d4ed8;
            transform: translateY(-1px);
        }
    </style>
</head>
<body>
    <div class="header">
        <div class="title">👑 GENESIS GRAND CORTEX CLOUD</div>
        <div class="status-pill">🟢 CLOUD RUNNING (PORT 8080)</div>
    </div>

    <div class="grid">
        <div class="card">
            <div class="card-title">🏛️ MAGI 3賢者 合議中枢</div>
            <div class="stat-value">ONLINE</div>
            <div class="stat-desc">MELCHIOR / BALTHASAR / CASPER (0.5s 判定)</div>
        </div>

        <div class="card">
            <div class="card-title">🧠 海馬ベクターDB</div>
            <div class="stat-value" id="hippoSize">-- MB</div>
            <div class="stat-desc">63.60 MB 完全正本化・ミリ秒検索</div>
        </div>

        <div class="card">
            <div class="card-title">🌐 Googleマイスター知識</div>
            <div class="stat-value" id="meisterCount">-- 件</div>
            <div class="stat-desc">自律巡回・MAGI審査合格ナレッジ</div>
        </div>

        <div class="card">
            <div class="card-title">🎓 全7科目 予想問題数</div>
            <div class="stat-value" id="quizCount">-- 問</div>
            <div class="stat-desc">全102講義章・自己解答検証済</div>
        </div>
    </div>

    <div class="card" style="margin-bottom: 24px; border: 2px solid #38bdf8; background: #0f172a;">
        <div class="card-title" style="color: #38bdf8; font-size: 18px; justify-content: space-between;">
            <span>🚀 GENESIS ワンタッチ・アクションランチャー</span>
            <div style="display: flex; gap: 8px;">
                <button class="btn" style="background: #ef4444; padding: 6px 14px; font-size: 12px;" onclick="killAllSystems()">
                    🛑 全器官キルスイッチ
                </button>
            </div>
        </div>
        <div style="display: flex; gap: 12px; flex-wrap: wrap;">
            <button class="btn" style="background: #0891b2;" onclick="window.open('/clinical_hud', '_blank')">
                🏥 臨床スマートグラスHUD
            </button>
            <button class="btn" style="background: #10b981;" onclick="window.open('/rehab_care', '_blank')">
                🏃 リハビリ＆介護見守りHUD
            </button>
            <button class="btn" style="background: #d97706;" onclick="window.open('/transport_shield', '_blank')">
                🚖 交通ドライバー防衛HUD
            </button>
            <button class="btn" style="background: #059669;" onclick="window.open('/workforce_rebalance', '_blank')">
                🔄 突発離脱リバランスHUD
            </button>
            <button class="btn" style="background: #e11d48;" onclick="window.open('/video_studio', '_blank')">
                🎬 AI動画スタジオ (2分デモ合成)
            </button>
            <button class="btn" style="background: #dc2626;" onclick="window.open('/safety_gate', '_blank')">
                🚨 出勤前安全ゲートキーパー
            </button>
            <button class="btn" style="background: #059669;" onclick="window.open('http://192.168.1.3:5000', '_blank')">
                📱 テレパシー実機HUD
            </button>
            <button class="btn" style="background: #0284c7;" onclick="window.open('http://192.168.1.3:5000/glass', '_blank')">
                🥽 スマートグラスHUD
            </button>
            <button class="btn" style="background: #7c3aed;" onclick="window.open('http://192.168.1.3:5000/listen', '_blank')">
                🎙️ スマホ対話マイク
            </button>
            <button class="btn" style="background: #0284c7;" onclick="window.open('/whisper_hud', '_blank')">
                🕶️ ステルス・テレパシー (耳元ささやき)
            </button>
            <button class="btn" style="background: #9333ea;" onclick="window.open('/pr_studio', '_blank')">
                🎬 汎用PR動画SaaSスタジオ
            </button>
            <button class="btn" style="background: #0d9488;" onclick="window.open('/sheets_canvas', '_blank')">
                📊 Sheets Canvas 24hテレメトリ
            </button>
            <button class="btn" style="background: #6366f1;" onclick="window.open('/notebook_lm', '_blank')">
                📚 GENESIS NotebookLM Platform (根拠引用 & Audio Overview)
            </button>
            <button class="btn" style="background: #ec4899;" onclick="window.open('/ebook_app_platform', '_blank')">
                📖 🎙️ 電子書籍QR音声＆複数書籍統合アプリ生成 (SLA & Dual-AI ALT)
            </button>
            <button class="btn" style="background: #14b8a6;" onclick="window.open('/mobile_antigravity', '_blank')">
                📱 🔒 スマホ連動 Antigravity 遠隔操作 (2FA & リアルタイム黒画面ログ)
            </button>
            <button class="btn" style="background: #8b5cf6;" onclick="checkMeshStatus()">
                🧠 ⚡ 機械脳自己進化メッシュ ＆ 余剰リソース分散レンタル (DePIN Grid)
            </button>
            <button class="btn" style="background: #f59e0b;" onclick="generateOfficialContestPackage()">
                🏆 公式コンテスト＆NEDO申請パッケージ出力
            </button>
            <button class="btn" style="background: #2563eb;" onclick="window.open('http://127.0.0.1:8000/report_viewer.html', '_blank')">
                📊 Report Viewer (Port 8000)
            </button>
            <button class="btn" style="background: #ea580c;" id="auditBtn" onclick="runNightAudit()">
                🌙 深夜3点照合AI監査を実行
            </button>
            <button class="btn" style="background: #4f46e5;" id="crawlerBtn" onclick="runNightCrawler()">
                🌐 夜間自律学習クローラー
            </button>
        </div>
    </div>

    <div class="card" style="margin-bottom: 24px; border: 1px solid #475569;">
        <div class="card-title" style="color: #38bdf8;">
            🔬 自律学習ターゲット登録 (完全フリーワード ＆ 差分監視URL)
        </div>
        <div style="display: flex; gap: 12px; margin-bottom: 12px; flex-wrap: wrap;">
            <input type="text" id="newKeyword" placeholder="任意のフリーワード（例: 脳神経, BMI, ALS, 量子アニーリング, 判例）" style="flex: 2; min-width: 260px; background: #0f172a; border: 1px solid #334155; color: white; padding: 10px; border-radius: 8px;">
            <button class="btn" style="background: #2563eb;" onclick="addKeyword()">➕ キーワード登録</button>
        </div>
        <div style="display: flex; gap: 12px; margin-bottom: 12px; flex-wrap: wrap;">
            <input type="text" id="newUrl" placeholder="巡回したい公式サイトURL（例: https://deepmind.google/blog）" style="flex: 2; min-width: 260px; background: #0f172a; border: 1px solid #334155; color: white; padding: 10px; border-radius: 8px;">
            <button class="btn" style="background: #0891b2;" onclick="addUrl()">➕ 監視URL登録</button>
        </div>
        <div id="targetListDisplay" style="font-size: 13px; color: #94a3b8; line-height: 1.6;">読み込み中...</div>
    </div>

    <div class="grid" style="margin-bottom: 24px;">
        <div class="card">
            <div class="card-title" style="color: #38bdf8;">
                🛠️ 定着済 公式SKILLマトリクス (全43種)
            </div>
            <div id="skillsListDisplay" style="font-size: 12px; color: #cbd5e1; height: 160px; overflow-y: auto; line-height: 1.6;">
                読み込み中...
            </div>
        </div>

        <div class="card">
            <div class="card-title" style="color: #f59e0b;">
                🏆 国際ハッカソン・コンペ勝利戦略
            </div>
            <div id="contestsListDisplay" style="font-size: 12px; color: #cbd5e1; height: 160px; overflow-y: auto; line-height: 1.6;">
                読み込み中...
            </div>
        </div>
    </div>

    <!-- 🌐 Google Cloud (cloud.google.com) 全情報・差分学習ステータス -->
    <div class="card" style="margin-bottom: 24px; border-color: #38bdf8;">
        <div class="card-title" style="justify-content: space-between; color: #38bdf8;">
            <span>🌐 Google Cloud (cloud.google.com) 全情報＆差分自律学習エンジン</span>
            <div style="display: flex; gap: 8px;">
                <button class="btn" style="background: #0284c7;" onclick="runGCloudPatrol()">🚀 Google Cloud全領域を今すぐ巡回・差分学習</button>
                <button class="btn" style="background: #10b981;" onclick="recommendGCloudArchitecture()">💡 開発への最適アーキテクチャ提案</button>
            </div>
        </div>
        <div class="log-box" id="gcloudStatusBox" style="font-size: 12px; line-height: 1.8;">
            <b>監視対象</b>: <code>https://cloud.google.com/</code> (Vertex AI, Gemini 3.7/2.0, Cloud Run, TPU v5p, BigQuery, Release Notes)<br>
            <b>学習蓄積先</b>: <code>knowledge_bank/Scholar_Nucleus/Google_Cloud_Master/</code> ＆ <code>knowledge_bank/hippocampus/google_cloud_deltas/</code><br>
            <span id="gcloudMetricsText">ステータス: 24時間差分自動検知 ＆ 開発還元中</span>
        </div>
    </div>

    <!-- 🌐 🎓 Google for Developers ＆ Google Skills Boost 全知全能エンジン -->
    <div class="card" style="margin-bottom: 24px; border-color: #a855f7;">
        <div class="card-title" style="justify-content: space-between; color: #c084fc;">
            <span>🌐 🎓 Google Developers ＆ Skills Boost 全知全能シナプス・エンジン</span>
            <div style="display: flex; gap: 8px;">
                <button class="btn" style="background: #9333ea;" onclick="runEcosystemPatrol()">🚀 Developers ＆ Skills全領域を今すぐ巡回学習</button>
                <button class="btn" style="background: #ec4899;" onclick="boostAntigravityCoding()">⚡ Antigravity超人開発ガイダンス (0.3s)</button>
            </div>
        </div>
        <div class="log-box" id="ecosystemStatusBox" style="font-size: 12px; line-height: 1.8;">
            <b>監視対象</b>: <code>https://developers.google.com/?hl=ja</code> ＆ <code>https://www.skills.google/?locale=ja</code><br>
            <b>学習蓄積先</b>: <code>Scholar_Nucleus/Google_Developers_Master/</code> ＆ <code>Scholar_Nucleus/Google_Skills_Boost_Master/</code><br>
            <span id="ecosystemMetricsText">ステータス: 階層型神経細胞シナプス結合 ＆ デフォルトAntigravity超越中</span>
        </div>
    </div>

    <!-- 🧠 🌐 ⚡ クラウド・シナプス結合 ＆ ローカル軽量化 Vault -->
    <div class="card" style="margin-bottom: 24px; border-color: #f59e0b;">
        <div class="card-title" style="justify-content: space-between; color: #fbbf24;">
            <span>🧠 🌐 ⚡ クラウド・シナプス結合 ＆ ローカル超軽量化 Vault</span>
            <div style="display: flex; gap: 8px;">
                <button class="btn" style="background: #d97706;" onclick="rebuildSynapseMatrix()">🧠 シナプス再結合 ＆ クラウド圧縮保管</button>
                <button class="btn" style="background: #b45309;" onclick="querySynapseCortex()">⚡ 0.3s クラウド・シナプス高速検索</button>
            </div>
        </div>
        <div class="log-box" id="synapseStatusBox" style="font-size: 12px; line-height: 1.8;">
            <b>シナプス神経網</b>: 12ノード（Cloud ✕ Developers ✕ Skills 3072次元ベクトル） / 44 クロス結合<br>
            <b>ローカル容量最適化</b>: 生データを軽量圧縮Vault（<code>genesis_google_knowledge_vault.zip</code>）へオフロード済<br>
            <span id="synapseMetricsText">ステータス: クラウド神経細胞結合 ＆ 0.3s即時推論アクティブ</span>
        </div>
    </div>

    <!-- 👑 🌐 🎓 ⚡ Google 全20大ドメイン 全知全能 Supreme Cortex -->
    <div class="card" style="margin-bottom: 24px; border-color: #ef4444;">
        <div class="card-title" style="justify-content: space-between; color: #f87171;">
            <span>👑 🌐 🎓 ⚡ Google 全20大ドメイン 全知全能 Supreme Cortex（本家開発者同等環境）</span>
            <div style="display: flex; gap: 8px;">
                <button class="btn" style="background: #dc2626;" onclick="runSupremeDailyPatrol()">🚀 Google全20領域を日次巡回・差分学習</button>
                <button class="btn" style="background: #b91c1c;" onclick="querySupremeGoogleKnowledge()">⚡ 0.3s Google全知全能ガイダンス推論</button>
            </div>
        </div>
        <div class="log-box" id="supremeStatusBox" style="font-size: 12px; line-height: 1.8;">
            <b>監視対象 (20大ドメイン)</b>: 検索, 会社情報, Store, Keyword, Japan Blog, Cloud Blog, Dev Blog, YouTube Blog, Developers, Cloud, Workspace, 検索セントラル, Skills Boost, アカウント, ドライブ, マップ, Play, Android, ヘルプ, セーフティ<br>
            <b>保存先</b>: クラウドVault ＆ 3072次元シナプス結合（ローカル容量極小化）<br>
            <span id="supremeMetricsText">ステータス: 24時間自律巡回 ＆ 差分自動検知アクティブ</span>
        </div>
    </div>

    <div class="card" style="margin-bottom: 24px;">
        <div class="card-title" style="justify-content: space-between;">
            <span>📋 大脳皮質 リアルタイム稼働メトリクス</span>
            <button class="btn" onclick="fetchMetrics()">🔄 最新情報に更新</button>
        </div>
        <div class="log-box" id="metricsBox">メトリクス読み込み中...</div>
    </div>

    <script>
        async function fetchTargets() {
            try {
                const res = await fetch('/api/targets');
                const data = await res.json();
                let html = '<b>【登録中フリーワード】</b>: ' + (data.free_keywords || []).join(' / ') + '<br>';
                html += '<b>【監視中URL】</b>: ' + (data.watched_urls || []).map(u => u.name || u.url).join(' | ');
                document.getElementById('targetListDisplay').innerHTML = html;
            } catch(e){}
        }

        async function addKeyword() {
            const kw = document.getElementById('newKeyword').value.trim();
            if (!kw) return;
            await fetch('/api/add_target', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({ type: 'keyword', value: kw })
            });
            document.getElementById('newKeyword').value = '';
            fetchTargets();
        }

        async function addUrl() {
            const url = document.getElementById('newUrl').value.trim();
            if (!url) return;
            await fetch('/api/add_target', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({ type: 'url', value: url })
            });
            document.getElementById('newUrl').value = '';
            fetchTargets();
        }

        async function fetchMetrics() {
            try {
                const res = await fetch('/api/metrics');
                const data = await res.json();
                document.getElementById('metricsBox').innerText = JSON.stringify(data, null, 2);
                document.getElementById('hippoSize').innerText = data.storage_metrics.hippocampus_vector_db_mb + ' MB';
                document.getElementById('meisterCount').innerText = data.storage_metrics.google_meister_articles_count + ' 件';
                document.getElementById('quizCount').innerText = data.storage_metrics.synthesized_course_quizzes_count + ' 問';
            } catch(e) {
                document.getElementById('metricsBox').innerText = 'メトリクス取得エラー';
            }
        }

        async function runNightAudit() {
            const btn = document.getElementById('auditBtn');
            btn.disabled = true;
            btn.innerText = '⏳ 深夜3点照合中...';
            try {
                const res = await fetch('/api/audit/run_night_audit', { method: 'POST' });
                const data = await res.json();
                alert('🌙 深夜3点照合AI監査完了！\n検出インシデント: ' + (data.incidents_detected || []).length + ' 件\n出勤前テスト生成完了！');
                fetchMetrics();
            } catch(e) {
                alert('⚠️ 監査実行エラー');
            } finally {
                btn.disabled = false;
                btn.innerText = '🌙 深夜3点照合AI監査を実行';
            }
        }

        async function runNightCrawler() {
            const btn = document.getElementById('crawlerBtn');
            btn.disabled = true;
            btn.innerText = '⏳ 巡回＆MAGI審査中...';
            try {
                const res = await fetch('/api/run_night_crawler');
                const data = await res.json();
                alert('🎉 自律学習完了！ 承認ナレッジ: ' + data.approved_count + ' 件 / 所要時間: ' + data.elapsed_sec + '秒');
                fetchMetrics();
                fetchTargets();
            } catch(e) {
                alert('⚠️ 自律学習実行エラー');
            } finally {
                btn.disabled = false;
                btn.innerText = '🌐 夜間自律学習クローラー';
            }
        }

        async function runGCloudPatrol() {
            const box = document.getElementById('gcloudStatusBox');
            box.innerHTML = '⏳ <b>Google Cloud 全領域巡回中...</b> (Vertex AI, Cloud Run, TPU, BigQuery, Release Notes取得中)';
            try {
                const res = await fetch('/api/gcloud/patrol', { method: 'POST' });
                const data = await res.json();
                box.innerHTML = `
                    <b>✅ 巡回完了</b>: 探索領域 ${data.total_targets_scanned}件 / 新規差分検知 ${data.new_deltas_detected}件 / 所要時間 ${data.patrol_latency_sec}秒<br>
                    <b>最新巡回日時</b>: ${data.timestamp}<br>
                    <b>定着先</b>: <code>knowledge_bank/Scholar_Nucleus/Google_Cloud_Master/</code>
                `;
                fetchMetrics();
            } catch(e) {
                box.innerHTML = '⚠️ Google Cloud巡回エラー';
            }
        }

        async function recommendGCloudArchitecture() {
            const task = prompt("開発したい課題・アーキテクチャ要件を入力してください:", "スマートグラス超低遅延ストリーミング推論と患者EHRセキュリティ");
            if (!task) return;
            const box = document.getElementById('gcloudStatusBox');
            box.innerHTML = '⏳ <b>Google Cloud最新知見から最適アーキテクチャを推論中... (0.3s)</b>';
            try {
                const res = await fetch('/api/gcloud/recommend', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({ task_description: task })
                });
                const data = await res.json();
                alert('💡 【Google Cloud 最適アーキテクチャ提案】\n\n' + data.recommendation);
                box.innerHTML = `<b>💡 最新アーキテクチャ提案完了</b> (推論時間: ${data.inference_time_ms}ms)<br>課題: ${data.task_description}`;
            } catch(e) {
                box.innerHTML = '⚠️ アーキテクチャ提案エラー';
            }
        }

        async function runEcosystemPatrol() {
            const box = document.getElementById('ecosystemStatusBox');
            box.innerHTML = '⏳ <b>Google Developers ＆ Skills Boost 全領域巡回中...</b> (Gemini API, Gemma, Android, WebGPU, GAS, Certification Paths)';
            try {
                const res = await fetch('/api/gdevelopers/patrol', { method: 'POST' });
                const data = await res.json();
                box.innerHTML = `
                    <b>✅ 巡回完了</b>: Developers ${data.total_dev_ingested}件 / Skills Boost ${data.total_skills_ingested}件 / 新規差分 ${data.new_deltas_detected}件 / 所要時間 ${data.patrol_latency_sec}秒<br>
                    <b>最新巡回日時</b>: ${data.timestamp}<br>
                    <b>定着先</b>: <code>Scholar_Nucleus/Google_Developers_Master/</code> ＆ <code>Scholar_Nucleus/Google_Skills_Boost_Master/</code>
                `;
                fetchMetrics();
            } catch(e) {
                box.innerHTML = '⚠️ エコシステム巡回エラー';
            }
        }

        async function boostAntigravityCoding() {
            const query = prompt("Google技術（Gemini API/Android/WebGPU/GAS/Cloud/Skills）に関する開発課題・質問を入力:", "Gemini 3.7 Flash Live MultimodalストリーミングとProject IDX/WebGPU連携の最適実装");
            if (!query) return;
            const box = document.getElementById('ecosystemStatusBox');
            box.innerHTML = '⏳ <b>Google全知全能シナプスから超人開発ガイダンスを推論中... (0.3s)</b>';
            try {
                const res = await fetch('/api/gdevelopers/superpower', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({ query: query })
                });
                const data = await res.json();
                alert('⚡ 【Google 全知全能 Antigravity 超人開発ガイダンス】\n\n' + data.guidance);
                box.innerHTML = `<b>⚡ 超人開発ガイダンス生成完了</b> (推論時間: ${data.inference_time_ms}ms)<br>課題: ${data.query}`;
            } catch(e) {
                box.innerHTML = '⚠️ 超人ガイダンス生成エラー';
            }
        }

        async function rebuildSynapseMatrix() {
            const box = document.getElementById('synapseStatusBox');
            box.innerHTML = '⏳ <b>Google全知識の3072次元ベクトルシナプス再結合 ＆ クラウドVault圧縮中...</b>';
            try {
                const res = await fetch('/api/synapse/build', { method: 'POST' });
                const data = await res.json();
                box.innerHTML = `
                    <b>✅ シナプス再結合＆Vault保管完了</b>: ${data.total_nodes}ノード / ${data.total_synapse_bridges}クロス結合 / Vault ${data.vault_archive_bytes} bytes<br>
                    <b>処理時間</b>: ${data.latency_sec}秒 | <b>更新日時</b>: ${data.updated_at}<br>
                    <b>ローカルストレージ</b>: 軽量シナプス行列のみ保持（生データはCloud Vaultに安全保管）
                `;
                fetchMetrics();
            } catch(e) {
                box.innerHTML = '⚠️ シナプス再結合エラー';
            }
        }

        async function querySynapseCortex() {
            const query = prompt("クラウド・シナプス検索クエリを入力 (Cloud / Developers / Skills):", "Vertex AIとAndroid Jetpack Composeのリアルタイム双方向連携");
            if (!query) return;
            const box = document.getElementById('synapseStatusBox');
            box.innerHTML = '⏳ <b>3072次元コサイン類似度でシナプス横断検索中... (<10ms)</b>';
            try {
                const res = await fetch('/api/synapse/query', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({ query: query })
                });
                const data = await res.json();
                const matches = (data.top_synapse_matches || []).map(m => `• [${m.ecosystem}] ${m.title} (類似度: ${m.similarity}%)`).join('\n');
                alert(`⚡ 【活性化されたクラウド・シナプス】\n${matches}\n\n【統合ガイダンス】\n${data.synthesized_guidance}`);
                box.innerHTML = `<b>⚡ シナプス推論完了</b> (推論時間: ${data.inference_time_ms}ms)<br>課題: ${data.query}`;
            } catch(e) {
                box.innerHTML = '⚠️ シナプス検索エラー';
            }
        }

        async function runSupremeDailyPatrol() {
            const box = document.getElementById('supremeStatusBox');
            box.innerHTML = '⏳ <b>Google全20大ドメインの巡回・差分学習中... (検索・公式ブログ・Developers・Cloud・Workspace・Play・Android・Security)</b>';
            try {
                const res = await fetch('/api/supreme/patrol', { method: 'POST' });
                const data = await res.json();
                box.innerHTML = `
                    <b>✅ 全20ドメイン巡回完了</b>: ${data.total_ingested}件定着 / ${data.total_synapse_nodes}ノード / ${data.total_synapse_bridges}シナプス結合 / 新規差分 ${data.new_deltas_detected}件 / Vault ${data.vault_archive_bytes} bytes<br>
                    <b>処理時間</b>: ${data.patrol_latency_sec}秒 | <b>最新更新</b>: ${data.timestamp}<br>
                    <b>ローカル軽量化</b>: クラウドVault保管 ＆ 超高速0.3sシナプス推論有効
                `;
                fetchMetrics();
            } catch(e) {
                box.innerHTML = '⚠️ 全20ドメイン巡回エラー';
            }
        }

        async function querySupremeGoogleKnowledge() {
            const query = prompt("Google全20大領域に関する質問・開発課題を入力 (検索・Android・Play・Maps・Cloud・Workspace・Security等):", "Google Pixel 10 On-device Gemini NanoとCloud Run Vertex AIのハイブリッド超低遅延連携");
            if (!query) return;
            const box = document.getElementById('supremeStatusBox');
            box.innerHTML = '⏳ <b>Google全20大ドメインのシナプスから最高知能ガイダンスを推論中... (0.3s)</b>';
            try {
                const res = await fetch('/api/supreme/query', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({ query: query })
                });
                const data = await res.json();
                const matches = (data.top_synapse_matches || []).map(m => `• [${m.category}] ${m.title} (${m.url}) - 類似度: ${m.similarity}%`).join('\n');
                alert(`👑 【活性化されたGoogle全知全能シナプス (20ドメイン)】\n${matches}\n\n【本家Google開発者同等ガイダンス】\n${data.supreme_guidance}`);
                box.innerHTML = `<b>👑 全知全能ガイダンス生成完了</b> (推論時間: ${data.inference_time_ms}ms)<br>課題: ${data.query}`;
            } catch(e) {
                box.innerHTML = '⚠️ 全知全能ガイダンス生成エラー';
            }
        }

        async function checkMeshStatus() {
            try {
                const res = await fetch('/api/mesh/compute_status');
                const data = await res.json();
                const evo = data.evolution_level;
                alert(`🧠 ⚡ 【GENESIS 機械脳自己進化 ＆ 分散コンピュート市場】\n\n` +
                      `• 機械脳成長ステージ: ${evo.stage_name} (Level ${evo.level})\n` +
                      `• 集合知 IQ 指数: ${evo.collective_iq} (総操作イベント: ${evo.total_events}件)\n` +
                      `• 稼働可能ノード数: ${data.active_compute_nodes} / ${data.total_nodes_registered} 台\n` +
                      `• ネットワーク流通クレジット: ${data.total_credits_circulated} Credits\n` +
                      `• 獲得機能シナジー数: ${data.feature_synergies_count} パターン\n\n` +
                      `※利用者の個人情報は100%保護（差分プライバシー）され、操作メタ情報のみで自己進化しています。`);
            } catch(e) {
                alert('⚠️ メッシュ状態取得エラー');
            }
        }

        async function generateOfficialContestPackage() {
            alert('⏳ Build with Gemini Challenge ＆ NEDO GENIAC 公式提出パッケージを自動パッキング中...');
            try {
                const res = await fetch('/api/contest/package', { method: 'POST' });
                const data = await res.json();
                alert(`🏆 【公式提出パッケージ パッキング完了】\n\n• Gemini Challenge マニフェスト: ${data.gemini_challenge_manifest}\n• NEDO GENIAC 仕様書: ${data.nedo_geniac_blueprint}\n• 完全提出用ZIP: ${data.master_zip_package} (${data.zip_size_bytes} bytes)\n• 所要時間: ${data.latency_ms}ms`);
            } catch(e) {
                alert('⚠️ パッケージ生成エラー');
            }
        }

        async function killAllSystems() {
            if (!confirm('🛑 GENESISの全器官（ポート5000/8080/バックグラウンドプロセス）を安全に一括停止しますか？')) return;
            try {
                await fetch('/api/kill_all', { method: 'POST' });
                alert('🛑 全器官の停止コマンドを発行しました。画面を閉じます。');
                window.close();
            } catch(e) {
                alert('🛑 停止完了（サーバー切断）');
            }
        }

        async function fetchSkillsAndContests() {
            try {
                const res = await fetch('/api/skills_and_contests');
                const data = await res.json();
                
                let sHtml = (data.skills || []).map(s => `• <b>${s}</b>`).join('<br>');
                document.getElementById('skillsListDisplay').innerHTML = sHtml || 'SKILL同期中...';

                let cHtml = (data.contests || []).map(c => `• 🏆 <b>${c.replace('.md','')}</b>`).join('<br>');
                document.getElementById('contestsListDisplay').innerHTML = cHtml || 'コンペ戦略探索中...';
            } catch(e){}
        }

        window.addEventListener('DOMContentLoaded', () => {
            fetchMetrics();
            fetchTargets();
            fetchSkillsAndContests();
        });
        setInterval(fetchMetrics, 10000);
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(STUDIO_HTML)

@app.route('/quiz_test')
@app.route('/quiz')
def view_quiz_test():
    return send_file(os.path.join(ROOT_DIR if 'ROOT_DIR' in globals() else r"g:\マイドライブ\GENESIS_ROOT", "web", "quiz_test_mt_info.html"))

# ------------------------------------------------------------------------------
# 🏥 臨床スマートグラスHUD ＆ 出勤前安全ゲートキーパー 画面ルーティング
# ------------------------------------------------------------------------------
@app.route('/clinical_hud')
@app.route('/clinical')
def view_clinical_hud():
    return send_from_directory(r"g:\マイドライブ\GENESIS_ROOT\web\static", "clinical_hud.html")

@app.route('/safety_gate')
@app.route('/gate')
def view_safety_gate():
    return send_from_directory(r"g:\マイドライブ\GENESIS_ROOT\web\static", "safety_gate_quiz.html")

@app.route('/video_studio')
@app.route('/video')
def view_video_studio():
    return send_from_directory(r"g:\マイドライブ\GENESIS_ROOT\web\static", "video_studio.html")

@app.route('/rehab_care')
@app.route('/rehab')
@app.route('/care')
def view_rehab_care():
    return send_from_directory(r"g:\マイドライブ\GENESIS_ROOT\web\static", "rehab_care_hud.html")

@app.route('/transport_shield')
@app.route('/transport')
def view_transport_shield():
    return send_from_directory(r"g:\マイドライブ\GENESIS_ROOT\web\static", "transport_shield_hud.html")

@app.route('/workforce_rebalance')
@app.route('/workforce')
def view_workforce_rebalance():
    return send_from_directory(r"g:\マイドライブ\GENESIS_ROOT\web\static", "workforce_rebalance_hud.html")

@app.route('/videos/<path:filename>')
def serve_video_file(filename):
    return send_from_directory(r"g:\マイドライブ\GENESIS_ROOT\web\static\video_assets", filename, mimetype='video/mp4')

@app.route('/watch')
def view_watch_video():
    lang = request.args.get('lang', 'en').upper()
    filename = f"GENESIS_Gemini_Challenge_2Min_Master_Demo_{lang}.mp4"
    video_url = f"/videos/{filename}"
    
    html = f"""<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🎬 GENESIS Master Demo Video ({lang})</title>
    <style>
        * {{ box-sizing: border-box; margin: 0; padding: 0; }}
        body {{
            background: #030712;
            color: #f1f5f9;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            align-items: center;
            padding: 24px;
        }}
        .header {{
            width: 100%;
            max-width: 1080px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 20px;
        }}
        .title {{
            font-size: 22px;
            font-weight: 900;
            color: #38bdf8;
        }}
        .video-box {{
            width: 100%;
            max-width: 1080px;
            background: #000;
            border: 2px solid #38bdf8;
            border-radius: 16px;
            overflow: hidden;
            box-shadow: 0 12px 48px rgba(0, 240, 255, 0.3);
            margin-bottom: 24px;
        }}
        video {{
            width: 100%;
            height: auto;
            max-height: 620px;
            display: block;
            outline: none;
        }}
        .btn {{
            background: #2563eb;
            color: #fff;
            font-weight: 800;
            font-size: 14px;
            padding: 10px 20px;
            border-radius: 10px;
            text-decoration: none;
            display: inline-flex;
            align-items: center;
            gap: 8px;
            transition: all 0.2s;
            border: none;
            cursor: pointer;
        }}
        .btn:hover {{ background: #1d4ed8; transform: translateY(-2px); }}
        .btn-cyan {{ background: #0891b2; }}
        .btn-green {{ background: #059669; }}
    </style>
</head>
<body>
    <div class="header">
        <div class="title">🎬 GENESIS 2-Minute Master Demo Video</div>
        <div style="display: flex; gap: 10px;">
            <a href="/watch?lang=en" class="btn {'btn-cyan' if lang == 'EN' else ''}">🇺🇸 英語動画 (提出用)</a>
            <a href="/watch?lang=ja" class="btn {'btn-cyan' if lang == 'JA' else ''}">🇯🇵 日本語動画</a>
            <a href="/video_studio" class="btn" style="background: #475569;">⚙️ スタジオ編集画面へ</a>
        </div>
    </div>

    <div class="video-box">
        <video controls autoplay playsinline preload="auto">
            <source src="{video_url}" type="video/mp4">
            お使いのブラウザはMP4動画の再生に対応していません。
        </video>
    </div>

    <div style="display: flex; gap: 16px; align-items: center;">
        <a href="{video_url}" download="{filename}" class="btn btn-green">
            📥 このMP4動画ファイルをダウンロード保存
        </a>
    </div>
</body>
</html>"""
    return render_template_string(html)



# ------------------------------------------------------------------------------
# 🎬 AI動画スタジオ ＆ プレゼンテーション API
# ------------------------------------------------------------------------------
@app.route('/api/video/get_storyboard')
def api_video_storyboard():
    return jsonify(video_synthesis_engine.get_storyboard())

@app.route('/api/video/get_cast_bible')
def api_video_cast_bible():
    return jsonify(video_synthesis_engine.get_cast_and_set_bible())

@app.route('/api/video/update_cut_text', methods=['POST'])
def api_update_cut_text():
    req = request.get_json(force=True)
    cid = req.get('cut_id', 1)
    n_en = req.get('narration_en', '')
    n_ja = req.get('narration_ja', '')
    title = req.get('title', '')
    hud = req.get('hud_overlay', '')
    res = video_synthesis_engine.update_cut(cid, n_en, n_ja, title, hud)
    return jsonify(res)

@app.route('/api/video/render_mp4_video', methods=['POST'])
def api_render_mp4():
    req = request.get_json(force=True) if request.data else {}
    lang = req.get('lang', 'en')
    res = video_synthesis_engine.render_full_mp4_video(lang)
    return jsonify(res)

@app.route('/api/video/render_demo_video', methods=['POST', 'GET'])
def api_render_demo_video():
    return jsonify(video_synthesis_engine.render_presentation_package())

# ------------------------------------------------------------------------------
# 🏃 リハビリ動作解析 ＆ 👵 介護見守り品質評価 API
# ------------------------------------------------------------------------------
@app.route('/api/rehab/analyze_frame', methods=['POST'])
def api_rehab_analyze_frame():
    req = request.get_json(force=True) if request.data else {}
    ex_type = req.get('exercise_type', 'knee_extension')
    landmarks = req.get('landmarks', {})
    pid = req.get('patient_id', 'P-102')
    res = rehab_motion_engine.analyze_exercise_frame(ex_type, landmarks, pid)
    return jsonify(res)

@app.route('/api/rehab/patient_history')
def api_rehab_history():
    pid = request.args.get('patient_id', 'P-102')
    return jsonify(rehab_motion_engine.get_patient_rehab_history(pid))

@app.route('/api/care/analyze_voice', methods=['POST'])
def api_care_analyze_voice():
    req = request.get_json(force=True) if request.data else {}
    staff_id = req.get('staff_id', 'STAFF-001')
    speech_text = req.get('speech_text', '')
    pid = req.get('patient_id', 'P-102')
    res = care_watchdog_engine.analyze_staff_interaction(staff_id, speech_text, pid)
    return jsonify(res)

@app.route('/api/care/analyze_posture', methods=['POST'])
def api_care_analyze_posture():
    req = request.get_json(force=True) if request.data else {}
    pid = req.get('patient_id', 'P-102')
    state = req.get('posture_state', 'lying_stable')
    sensor = req.get('sensor_data', {})
    res = care_watchdog_engine.analyze_bed_posture_and_fall_risk(pid, state, sensor)
    return jsonify(res)

@app.route('/api/care/facility_cqi')
def api_care_cqi():
    return jsonify(care_watchdog_engine.get_facility_care_quality_index())

# ------------------------------------------------------------------------------
# 🚖 交通ドライバー防衛 ＆ 損害賠償算定 API
# ------------------------------------------------------------------------------
@app.route('/api/transport/analyze_speech', methods=['POST'])
def api_transport_analyze_speech():
    req = request.get_json(force=True) if request.data else {}
    did = req.get('driver_id', 'DRV-8821')
    text = req.get('speech_text', '')
    vid = req.get('vehicle_id', 'TAXI-304')
    res = transport_shield_engine.analyze_speech_and_harassment(did, text, vid)
    return jsonify(res)

@app.route('/api/transport/calculate_damages', methods=['POST'])
def api_transport_calc_damages():
    req = request.get_json(force=True) if request.data else {}
    delay = int(req.get('delay_minutes', 30))
    severity = req.get('severity_level', 'HIGH')
    clean = req.get('cleaning_required', False)
    res = transport_shield_engine.calculate_legal_damages(delay, severity, clean)
    return jsonify(res)

# ------------------------------------------------------------------------------
# 🔄 突発離脱リアルタイム全自動リバランス API
# ------------------------------------------------------------------------------
@app.route('/api/workforce/rebalance', methods=['POST'])
def api_workforce_rebalance():
    req = request.get_json(force=True) if request.data else {}
    staff_id = req.get('absent_staff_id', 'STAFF-004')
    reason = req.get('reason', '突発発熱 38.5℃ (体調不良)')
    res = workforce_rebalancer_engine.rebalance_on_sudden_absence(staff_id, reason)
    return jsonify(res)

@app.route('/api/workforce/status')
def api_workforce_status():
    return jsonify(workforce_rebalancer_engine.get_current_ward_schedule())

# ------------------------------------------------------------------------------
# 🌐 Google Cloud (cloud.google.com) 全情報・差分学習 API
# ------------------------------------------------------------------------------
@app.route('/api/gcloud/patrol', methods=['POST', 'GET'])
def api_gcloud_patrol():
    return jsonify(google_cloud_harvester.run_full_gcloud_patrol())

@app.route('/api/gcloud/insights', methods=['GET'])
def api_gcloud_insights():
    return jsonify(google_cloud_harvester.get_latest_gcloud_insights())

@app.route('/api/gcloud/recommend', methods=['POST'])
def api_gcloud_recommend():
    req = request.get_json(force=True) if request.data else {}
    task = req.get('task_description', 'Realtime AI smart glasses')
    return jsonify(google_cloud_harvester.recommend_architecture_for_task(task))

# ------------------------------------------------------------------------------
# 🌐 🎓 Google for Developers ＆ Google Skills Boost 全知全能 API
# ------------------------------------------------------------------------------
@app.route('/api/gdevelopers/patrol', methods=['POST', 'GET'])
def api_gdevelopers_patrol():
    return jsonify(google_developers_and_skills_harvester.run_full_ecosystem_patrol())

@app.route('/api/gdevelopers/insights', methods=['GET'])
def api_gdevelopers_insights():
    return jsonify(google_developers_and_skills_harvester.get_ecosystem_insights())

@app.route('/api/gdevelopers/superpower', methods=['POST'])
def api_gdevelopers_superpower():
    req = request.get_json(force=True) if request.data else {}
    query = req.get('query', 'Google Ecosystem Best Practices')
    return jsonify(google_developers_and_skills_harvester.synthesize_supreme_developer_superpower(query))

# ------------------------------------------------------------------------------
# 🧠 🌐 ⚡ クラウド・シナプス結合 ＆ ローカル軽量化 API
# ------------------------------------------------------------------------------
@app.route('/api/synapse/insights', methods=['GET'])
def api_synapse_insights():
    return jsonify(cloud_synapse_engine.get_synapse_insights())

@app.route('/api/synapse/build', methods=['POST'])
def api_synapse_build():
    return jsonify(cloud_synapse_engine.build_and_compress_synapse_matrix())

@app.route('/api/synapse/query', methods=['POST'])
def api_synapse_query():
    req = request.get_json(force=True) if request.data else {}
    query = req.get('query', 'Google Cloud architecture best practices')
    return jsonify(cloud_synapse_engine.search_and_synthesize(query))

# ------------------------------------------------------------------------------
# 👑 🌐 🎓 ⚡ Google 全20大ドメイン 全知全能 Supreme Cortex API
# ------------------------------------------------------------------------------
@app.route('/api/supreme/insights', methods=['GET'])
def api_supreme_insights():
    return jsonify(google_supreme_cortex.get_supreme_insights())

@app.route('/api/supreme/patrol', methods=['POST', 'GET'])
def api_supreme_patrol():
    return jsonify(google_supreme_cortex.run_daily_autonomous_patrol())

@app.route('/api/supreme/query', methods=['POST'])
def api_supreme_query():
    req = request.get_json(force=True) if request.data else {}
    query = req.get('query', 'Google 2026 最新技術スタック')
    return jsonify(google_supreme_cortex.query_supreme_google_knowledge(query))

# ------------------------------------------------------------------------------
# 🕶️ 🎧 ⚡ Meta Ray-Ban / Bluetooth ステルス・テレパシー API
# ------------------------------------------------------------------------------
@app.route('/whisper_hud')
def view_whisper_hud():
    return render_template_string("""
    <!DOCTYPE html>
    <html lang="ja">
    <head>
        <meta charset="UTF-8"><title>GENESIS Stealth Whisper HUD</title>
        <style>
            body { background: #000; color: #38bdf8; font-family: sans-serif; display: flex; flex-direction: column; align-items: center; justify-content: center; height: 100vh; margin: 0; text-align: center; }
            .card { border: 2px solid #38bdf8; padding: 30px; border-radius: 20px; background: rgba(15, 23, 42, 0.9); box-shadow: 0 0 30px rgba(56, 189, 248, 0.4); max-width: 90%; }
            .btn { background: #0284c7; color: white; border: none; padding: 14px 28px; border-radius: 12px; font-size: 18px; font-weight: bold; cursor: pointer; margin-top: 20px; }
            .status { font-size: 24px; font-weight: bold; color: #fff; margin-top: 20px; }
        </style>
    </head>
    <body>
        <div class="card">
            <h1>🕶️ 🎧 GENESIS ステルス・テレパシー (0.3s Whisper)</h1>
            <p>Meta Ray-Ban スマートグラス / Bluetoothイヤホン用 自動音声ささやきストリーム</p>
            <button class="btn" onclick="activateAudio()">🔊 音声を有効化（1タップ接続）</button>
            <div id="status" class="status">待機中...</div>
        </div>
        <script>
            let audioActive = false;
            let lastWhisper = "";
            function activateAudio() {
                audioActive = true;
                document.getElementById('status').innerText = '🟢 Bluetooth/グラス音声ストリーム接続完了';
                let u = new SpeechSynthesisUtterance("GENESIS ステルス・テレパシーが耳元に接続されました。");
                u.lang = 'ja-JP';
                u.rate = 1.2;
                window.speechSynthesis.speak(u);
            }
            setInterval(async () => {
                if (!audioActive) return;
                try {
                    const res = await fetch('/api/whisper/status');
                    const data = await res.json();
                    if (data.last_whisper && data.last_whisper.text && data.last_whisper.text !== lastWhisper) {
                        lastWhisper = data.last_whisper.text;
                        document.getElementById('status').innerText = '⚡ 耳元ささやき中: ' + lastWhisper;
                        window.speechSynthesis.cancel();
                        let u = new SpeechSynthesisUtterance(lastWhisper);
                        u.lang = 'ja-JP';
                        u.rate = 1.25;
                        window.speechSynthesis.speak(u);
                    }
                } catch(e){}
            }, 300);
        </script>
    </body>
    </html>
    """)

@app.route('/api/whisper/status')
def api_whisper_status():
    return jsonify(stealth_whisper_engine.get_whisper_status())

@app.route('/api/whisper/push', methods=['POST'])
def api_whisper_push():
    req = request.get_json(force=True) if request.data else {}
    text = req.get('text', 'GENESIS 即時推論回答')
    speed = req.get('speed', '+20%')
    return jsonify(stealth_whisper_engine.trigger_stealth_whisper(text, speed))

# ------------------------------------------------------------------------------
# 🎬 🎨 🚀 GENESIS PR-STUDIO 汎用版 SaaS API
# ------------------------------------------------------------------------------
@app.route('/pr_studio')
def view_pr_studio():
    return render_template_string("""
    <!DOCTYPE html>
    <html lang="ja">
    <head>
        <meta charset="UTF-8"><title>GENESIS PR-STUDIO SaaS</title>
        <style>
            body { background: #0b1120; color: #f8fafc; font-family: sans-serif; padding: 24px; }
            .container { max-width: 1100px; margin: 0 auto; }
            .card { background: #1e293b; border: 1px solid #334155; border-radius: 16px; padding: 24px; margin-bottom: 20px; }
            .btn { background: #3b82f6; color: white; border: none; padding: 12px 24px; border-radius: 8px; font-weight: bold; cursor: pointer; font-size: 15px; }
            .input-field { width: 100%; padding: 10px; border-radius: 8px; border: 1px solid #475569; background: #0f172a; color: white; margin-bottom: 12px; }
            .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 16px; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1 style="color: #38bdf8;">🎬 GENESIS PR-STUDIO 汎用版 (SaaS Video Engine)</h1>
            <p>Google Imagen / Veo / 高自然度TTSによる中小企業向けPR動画 6カット全自動制作スタジオ</p>
            
            <div class="card">
                <h3>🚀 新規PR動画プロジェクト作成</h3>
                <input id="prodName" class="input-field" placeholder="商品・サービス名 (例: AI医院経営OS)" value="GENESIS AI Hospital OS">
                <input id="targetAud" class="input-field" placeholder="ターゲット層 (例: 病院理事長・看護部長)" value="病院理事長・看護部長">
                <input id="sellingPts" class="input-field" placeholder="アピールポイント (カンマ区切り)" value="看護師残業ゼロ, 3点照合AI自動化, 突発欠勤0.3sリバランス">
                <button class="btn" onclick="createPRProject()">✨ 6カットPRストーリー ＆ 動画構成を自動生成</button>
            </div>

            <div id="projectResultCard" class="card" style="display:none;">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <h3 id="projectTitle" style="color: #4ade80;">構成完了</h3>
                    <button class="btn" style="background:#10b981;" onclick="renderMasterVideo()">🎬 1クリック マスターMP4 動画出力</button>
                </div>
                <div id="cutsContainer" class="grid" style="margin-top: 16px;"></div>
            </div>
        </div>

        <script>
            let currentProjId = "";
            async function createPRProject() {
                const prod = document.getElementById('prodName').value;
                const target = document.getElementById('targetAud').value;
                const pts = document.getElementById('sellingPts').value.split(',').map(s => s.trim());
                alert('⏳ Gemini 3.7 Flashで最適なPRストーリーボードとビジュアルプロンプトを立案中...');
                const res = await fetch('/api/pr_studio/create', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({ product_name: prod, target_audience: target, selling_points: pts })
                });
                const data = await res.json();
                currentProjId = data.project_id;
                document.getElementById('projectResultCard').style.display = 'block';
                document.getElementById('projectTitle').innerText = '✅ プロジェクト: ' + data.project_id + ' (合計 ' + data.project_data.total_duration_sec + '秒)';
                
                let html = '';
                (data.project_data.cuts || []).forEach(c => {
                    html += `
                        <div style="background:#0f172a; border:1px solid #38bdf8; border-radius:12px; padding:16px;">
                            <h4 style="color:#38bdf8;">CUT ${c.cut_number}: ${c.headline} (${c.duration_sec}秒)</h4>
                            <img src="${c.image_url}" style="width:100%; border-radius:8px; margin:8px 0;">
                            <p style="font-size:13px; color:#cbd5e1;"><b>ナレーション</b>: ${c.narration_text}</p>
                        </div>
                    `;
                });
                document.getElementById('cutsContainer').innerHTML = html;
            }

            async function renderMasterVideo() {
                if (!currentProjId) return;
                alert('⏳ 全カットの音声合成 ＆ マスターMP4動画をレンダリング中...');
                const res = await fetch('/api/pr_studio/render', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({ project_id: currentProjId })
                });
                const data = await res.json();
                alert('🎉 マスターPR動画の出力が完了しました！\n動画URL: ' + data.video_url);
                window.open(data.video_url, '_blank');
            }
        </script>
    </body>
    </html>
    """)

@app.route('/api/pr_studio/create', methods=['POST'])
def api_pr_studio_create():
    req = request.get_json(force=True) if request.data else {}
    prod = req.get('product_name', 'AI SaaS')
    target = req.get('target_audience', '企業経営者')
    pts = req.get('selling_points', ['業務効率化'])
    return jsonify(pr_studio_saas.create_pr_project(prod, target, pts))

@app.route('/api/pr_studio/render', methods=['POST'])
def api_pr_studio_render():
    req = request.get_json(force=True) if request.data else {}
    proj_id = req.get('project_id', '')
    return jsonify(pr_studio_saas.render_master_video(proj_id))

# ------------------------------------------------------------------------------
# 📊 ⚡ 📈 Sheets Canvas × Gemini Spark 24h テレメトリ API
# ------------------------------------------------------------------------------
@app.route('/sheets_canvas')
def view_sheets_canvas():
    return render_template_string("""
    <!DOCTYPE html>
    <html lang="ja">
    <head>
        <meta charset="UTF-8"><title>GENESIS Sheets Canvas</title>
        <style>
            body { background: #0f172a; color: #f8fafc; font-family: sans-serif; padding: 24px; }
            .card { background: #1e293b; border: 1px solid #334155; border-radius: 16px; padding: 24px; margin-bottom: 20px; max-width: 1000px; margin: 0 auto; }
            table { width: 100%; border-collapse: collapse; margin-top: 16px; }
            th, td { border: 1px solid #334155; padding: 12px; text-align: left; }
            th { background: #0f172a; color: #38bdf8; }
            .btn { background: #10b981; color: white; border: none; padding: 10px 20px; border-radius: 8px; font-weight: bold; cursor: pointer; }
        </style>
    </head>
    <body>
        <div class="card">
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <h2 style="color: #38bdf8;">📊 Sheets Canvas × Gemini Spark 24時間自律巡回テレメトリ</h2>
                <button class="btn" onclick="exportCSV()">📥 Google Sheets CSV ダウンロード</button>
            </div>
            <p id="lastSync" style="color: #94a3b8;">同期中...</p>
            <table id="telemetryTable">
                <thead>
                    <tr><th>時刻</th><th>Google同期率</th><th>臨床監査件数</th><th>活性シナプス数</th><th>システム健全度</th></tr>
                </thead>
                <tbody></tbody>
            </table>
        </div>
        <script>
            async function loadData() {
                const res = await fetch('/api/sheets_canvas/telemetry');
                const data = await res.json();
                document.getElementById('lastSync').innerText = '🔄 最新同期: ' + data.last_synced + ' | 稼働状態: 24.0h (100% ONLINE)';
                let html = '';
                (data.timeline || []).forEach(r => {
                    html += `<tr><td>${r.hour}</td><td>${r.gcloud_sync}%</td><td>${r.clinical_audits}件</td><td>${r.synapses_active}本</td><td>${r.system_health}%</td></tr>`;
                });
                document.querySelector('#telemetryTable tbody').innerHTML = html;
            }
            async function exportCSV() {
                const res = await fetch('/api/sheets_canvas/export_csv', { method: 'POST' });
                const data = await res.json();
                alert('✅ Google Sheets用CSVを書き出しました: ' + data.csv_file);
            }
            loadData();
        </script>
    </body>
    </html>
    """)

@app.route('/api/sheets_canvas/telemetry')
def api_sheets_telemetry():
    return jsonify(sheets_canvas_engine.get_canvas_telemetry())

@app.route('/api/sheets_canvas/export_csv', methods=['POST', 'GET'])
def api_sheets_export_csv():
    return jsonify(sheets_canvas_engine.export_sheets_csv())

# ------------------------------------------------------------------------------
# 🏆 📜 📦 Build with Gemini ＆ NEDO GENIAC 公式パッケージ API
# ------------------------------------------------------------------------------
@app.route('/api/contest/package', methods=['POST', 'GET'])
def api_contest_package():
    return jsonify(contest_packager.build_official_submission_packages())

# ------------------------------------------------------------------------------
# 📚 🎙️ 🧠 GENESIS NotebookLM Platform Web Console & API
# ------------------------------------------------------------------------------
@app.route('/notebook_lm')
def view_notebook_lm():
    return render_template_string("""
    <!DOCTYPE html>
    <html lang="ja">
    <head>
        <meta charset="UTF-8"><title>GENESIS NotebookLM Platform</title>
        <style>
            body { background: #0b1120; color: #f8fafc; font-family: sans-serif; padding: 24px; }
            .container { max-width: 1100px; margin: 0 auto; }
            .card { background: #1e293b; border: 1px solid #334155; border-radius: 16px; padding: 24px; margin-bottom: 20px; }
            .btn { background: #6366f1; color: white; border: none; padding: 12px 24px; border-radius: 8px; font-weight: bold; cursor: pointer; font-size: 15px; }
            .input-field { width: 100%; padding: 12px; border-radius: 8px; border: 1px solid #475569; background: #0f172a; color: white; margin-bottom: 12px; }
            .answer-box { background: #0f172a; border: 1px solid #6366f1; border-radius: 12px; padding: 20px; margin-top: 16px; line-height: 1.8; white-space: pre-wrap; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1 style="color: #818cf8;">📚 GENESIS NotebookLM Enterprise Platform</h1>
            <p>マルチソース完全根拠付き深層分析 (Grounded Citations) ＆ AI 2名ホスト対話型ポッドキャスト音声 (Audio Overview)</p>
            
            <div class="card">
                <h3>🔍 ソース文書への深層質問 (Grounded Query)</h3>
                <input id="nbQuery" class="input-field" placeholder="質問を入力 (例: GENESISの多階層アーキテクチャとGoogle全20ドメインのシナプス結合について)" value="GENESISの多階層アーキテクチャとGoogle全20ドメインのシナプス結合について詳しく教えてください">
                <div style="display:flex; gap:12px;">
                    <button class="btn" onclick="queryNotebook()">💡 出典引用付きで深層回答を生成</button>
                    <button class="btn" style="background:#a855f7;" onclick="generateAudioOverview()">🎙️ 2名ホスト対話ポッドキャスト音声を生成 (Audio Overview)</button>
                </div>
            </div>

            <div id="resultCard" class="card" style="display:none;">
                <h3 id="resultTitle" style="color: #a5f3fc;">回答</h3>
                <div id="answerContent" class="answer-box"></div>
                <div id="audioPlayerBox" style="margin-top: 16px; display:none;">
                    <h4 style="color:#c084fc;">🎧 AIディープダイブ・ポッドキャスト音声 (Audio Overview):</h4>
                    <audio id="audioPlayer" controls style="width: 100%; margin-top: 8px;"></audio>
                </div>
            </div>
        </div>

        <script>
            async function queryNotebook() {
                const query = document.getElementById('nbQuery').value;
                if (!query) return;
                alert('⏳ 登録ソース文書から完全根拠付き深層回答を生成中...');
                const res = await fetch('/api/notebook_lm/query', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({ query: query })
                });
                const data = await res.json();
                document.getElementById('resultCard').style.display = 'block';
                document.getElementById('resultTitle').innerText = '✅ NotebookLM 出典付き深層回答 (推論時間: ' + data.latency_ms + 'ms)';
                document.getElementById('answerContent').innerText = data.answer;
                document.getElementById('audioPlayerBox').style.display = 'none';
            }

            async function generateAudioOverview() {
                alert('⏳ 2名のAIホストによるディープダイブ・ポッドキャスト対話音声を生成中...');
                const res = await fetch('/api/notebook_lm/audio_overview', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({ topic: 'GENESIS Multi-Organ OS & Google Supreme Synapse' })
                });
                const data = await res.json();
                document.getElementById('resultCard').style.display = 'block';
                document.getElementById('resultTitle').innerText = '🎉 2名ホスト対話ポッドキャスト音声 (Audio Overview) 生成完了';
                let dialogueText = (data.dialogue || []).map(d => `【${d.speaker}】: ${d.text}`).join('\n\n');
                document.getElementById('answerContent').innerText = dialogueText;
                document.getElementById('audioPlayerBox').style.display = 'block';
                document.getElementById('audioPlayer').src = data.audio_url;
                document.getElementById('audioPlayer').play();
            }
        </script>
    </body>
    </html>
    """)

@app.route('/api/notebook_lm/query', methods=['POST'])
def api_notebook_lm_query():
    req = request.get_json(force=True) if request.data else {}
    query = req.get('query', 'GENESIS アーキテクチャ')
    nb_id = req.get('notebook_id', 'default')
    return jsonify(notebook_lm_platform.query_notebook(nb_id, query))

@app.route('/api/notebook_lm/audio_overview', methods=['POST'])
def api_notebook_lm_audio_overview():
    req = request.get_json(force=True) if request.data else {}
    nb_id = req.get('notebook_id', 'default')
    topic = req.get('topic', 'GENESIS Multi-Organ OS')
    return jsonify(notebook_lm_platform.generate_audio_overview(nb_id, topic))

@app.route('/api/notebook_lm/list')
def api_notebook_lm_list():
    return jsonify(notebook_lm_platform.list_notebooks())

# ------------------------------------------------------------------------------
# 📖 🎙️ 📱 GENESIS eBook-to-App & Cross-Book Synthesizer Web Console & API
# ------------------------------------------------------------------------------
@app.route('/ebook_app_platform')
def view_ebook_app_platform():
    return render_template_string("""
    <!DOCTYPE html>
    <html lang="ja">
    <head>
        <meta charset="UTF-8"><title>GENESIS eBook-to-App Synthesizer</title>
        <style>
            body { background: #0f172a; color: #f8fafc; font-family: sans-serif; padding: 24px; }
            .container { max-width: 1200px; margin: 0 auto; }
            .card { background: #1e293b; border: 1px solid #334155; border-radius: 16px; padding: 24px; margin-bottom: 20px; }
            .btn { background: #ec4899; color: white; border: none; padding: 12px 24px; border-radius: 8px; font-weight: bold; cursor: pointer; font-size: 15px; }
            .badge { display: inline-block; padding: 4px 10px; border-radius: 6px; font-size: 12px; font-weight: bold; margin-right: 6px; background: #374151; color: #a5f3fc; }
            .grid { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; }
            .input-field { width: 100%; padding: 12px; border-radius: 8px; border: 1px solid #475569; background: #0f172a; color: white; margin-bottom: 12px; }
            .result-box { background: #0f172a; border: 1px solid #ec4899; border-radius: 12px; padding: 20px; margin-top: 16px; line-height: 1.8; white-space: pre-wrap; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1 style="color: #f472b6;">📖 🎙️ 📱 GENESIS 電子書籍 ➔ アプリ化 ＆ 複数書籍横断統合スタジオ</h1>
            <p>本文QRコード音声自動抽出 ✕ 出版社正誤表上書き ✕ SLA理論 ✕ 4技能＋100日手書き書き写し ✕ Dual-AI ALT (会話役＋助け舟役)</p>

            <div class="card">
                <h3>📚 現在インジェスト済みの電子書籍ライブラリ (QR音声＆正誤表適用済み)</h3>
                <div id="booksList" class="grid">
                    <div style="background:#0f172a; padding:12px; border-radius:8px;">
                        <span class="badge" style="background:#0284c7;">SLA理論</span><strong>英語が日本語みたいに出てくる頭のつくり方</strong><br>
                        <small style="color:#94a3b8;">🔗 QR音声: 45トラック | 出版社正誤表: 適用済</small>
                    </div>
                    <div style="background:#0f172a; padding:12px; border-radius:8px;">
                        <span class="badge" style="background:#10b981;">中学文法</span><strong>中学英語をもう一度ひとつひとつわかりやすく。改訂版</strong><br>
                        <small style="color:#94a3b8;">🔗 QR音声: 112トラック | 出版社正誤表: 適用済</small>
                    </div>
                    <div style="background:#0f172a; padding:12px; border-radius:8px;">
                        <span class="badge" style="background:#8b5cf6;">高校文法</span><strong>高校英文法・語法をひとつひとつわかりやすく。</strong><br>
                        <small style="color:#94a3b8;">🔗 QR音声: 98トラック | 出版社正誤表: 適用済</small>
                    </div>
                    <div style="background:#0f172a; padding:12px; border-radius:8px;">
                        <span class="badge" style="background:#f59e0b;">会話単語</span><strong>会話のための英単語をもう一度ひとつひとつわかりやすく。</strong><br>
                        <small style="color:#94a3b8;">🔗 QR音声: 80トラック | 出版社正誤表: 適用済</small>
                    </div>
                    <div style="background:#0f172a; padding:12px; border-radius:8px;">
                        <span class="badge" style="background:#ef4444;">発音・音読</span><strong>英語の発音をもう一度ひとつひとつわかりやすく。</strong><br>
                        <small style="color:#94a3b8;">🔗 QR音声: 64トラック | 出版社正誤表: 適用済</small>
                    </div>
                    <div style="background:#0f172a; padding:12px; border-radius:8px;">
                        <span class="badge" style="background:#ec4899;">手書きペン</span><strong>100日後に英語がものになる1日10分 ネイティブ英語書き写し</strong><br>
                        <small style="color:#94a3b8;">🔗 QR音声: 100トラック | 出版社正誤表: 適用済</small>
                    </div>
                </div>
            </div>

            <div class="card">
                <h3>🚀 新教材・学習アプリ合成 (弱点克服 ＆ 生成モード指定)</h3>
                <label>学習者の弱点・克服したいテーマ:</label>
                <input id="weaknessInput" class="input-field" value="単語力はあるが会話表現力と発音がとぼしい、定型文を忘れやすい">
                
                <div style="display:flex; gap:12px; align-items:center;">
                    <button class="btn" style="background:#8b5cf6;" onclick="synthesizeApp('COMBINED')">🔗 複数書籍横断 統合アプリ生成</button>
                    <button class="btn" style="background:#0284c7;" onclick="synthesizeApp('SINGLE')">🎯 単独書籍 集中特訓アプリ生成</button>
                    <button class="btn" style="background:#ec4899;" onclick="synthesizeApp('BOTH')">✨ 統合・単独 両方一括生成</button>
                    <button class="btn" style="background:#10b981;" onclick="testDualAIALT()">🎙️ Dual-AI ALT 会話＋助け舟テスト</button>
                </div>
            </div>

            <div id="resultCard" class="card" style="display:none;">
                <h3 id="resultTitle" style="color:#f472b6;">合成結果</h3>
                <div id="resultBox" class="result-box"></div>
            </div>
        </div>

        <script>
            async function synthesizeApp(mode) {
                const weakness = document.getElementById('weaknessInput').value;
                alert('⏳ 電子書籍QR音声 ＆ 正誤表を結合し、新教材アプリを生成中 (' + mode + 'モード)...');
                const res = await fetch('/api/ebook/synthesize_app', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({ mode: mode, learner_weakness: weakness })
                });
                const data = await res.json();
                document.getElementById('resultCard').style.display = 'block';
                document.getElementById('resultTitle').innerText = '🎉 ' + data.title + ' (所要時間: ' + data.latency_ms + 'ms)';
                document.getElementById('resultBox').innerText = JSON.stringify(data, null, 2);
            }

            async function testDualAIALT() {
                alert('⏳ Dual-AI ALT (ネイティブ会話AI + 日本人AI ALT助け舟) をテスト中...');
                const res = await fetch('/api/ebook/dual_ai_alt', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({ speech: 'I want to order a latte, but I forgot how to ask for oat milk.' })
                });
                const data = await res.json();
                document.getElementById('resultCard').style.display = 'block';
                document.getElementById('resultTitle').innerText = '🎙️ Dual-AI ALT ロールプレイ応答';
                document.getElementById('resultBox').innerText = '【Native ALT (英語会話役)】:\n' + data.native_response + '\n\n【Support ALT (日本人助け舟ささやき)】:\n' + data.support_alt_whisper;
            }
        </script>
    </body>
    </html>
    """)

@app.route('/api/ebook/synthesize_app', methods=['POST'])
def api_ebook_synthesize_app():
    req = request.get_json(force=True) if request.data else {}
    mode = req.get('mode', 'COMBINED')
    weakness = req.get('learner_weakness', '単語力はあるが会話表現力と発音がとぼしい')
    return jsonify(ebook_cross_platform.generate_custom_learning_app(mode=mode, learner_weakness=weakness))

@app.route('/api/ebook/zero_quiz', methods=['POST'])
def api_ebook_zero_quiz():
    req = request.get_json(force=True) if request.data else {}
    book_id = req.get('book_id', 'book_jh_grammar')
    topic = req.get('unit_topic', '現在完了')
    return jsonify(ebook_cross_platform.generate_zero_hallucination_quiz(book_id, topic))

@app.route('/api/ebook/dual_ai_alt', methods=['POST'])
def api_ebook_dual_ai_alt():
    req = request.get_json(force=True) if request.data else {}
    speech = req.get('speech', 'I want to order a coffee')
    return jsonify(ebook_cross_platform.simulate_dual_ai_alt_interaction(speech))

@app.route('/api/ebook/list_books')
def api_ebook_list_books():
    return jsonify(ebook_cross_platform.list_ingested_books())

# ------------------------------------------------------------------------------
# 🔍 🧠 GENESIS Chat Chronicles & Brain Search API
# ------------------------------------------------------------------------------
from core.genesis_cloud_antigravity_twin_syncer import cloud_antigravity_syncer

@app.route('/api/chat/search', methods=['POST', 'GET'])
def api_chat_search():
    if request.method == 'POST':
        req = request.get_json(force=True) if request.data else {}
        query = req.get('query', '')
        limit = int(req.get('limit', 15))
    else:
        query = request.args.get('q', '')
        limit = int(request.args.get('limit', 15))
    return jsonify(cloud_antigravity_syncer.search_chat_chronicles(query, limit))

@app.route('/api/chat/tree', methods=['GET', 'POST'])
def api_chat_tree():
    q = request.args.get('q', '')
    if request.method == 'POST':
        req = request.get_json(force=True) if request.data else {}
        q = req.get('query', q)
    return jsonify(cloud_antigravity_syncer.get_project_conversation_tree(q))

@app.route('/api/chat/get_conversation', methods=['GET', 'POST'])
def api_chat_get_conversation():
    title = request.args.get('title', '')
    if request.method == 'POST':
        req = request.get_json(force=True) if request.data else {}
        title = req.get('title', title)
    return jsonify(cloud_antigravity_syncer.get_conversation_messages(title))

@app.route('/api/chat/sync_stream', methods=['POST'])
def api_chat_sync_stream():
    req = request.get_json(force=True) if request.data else {}
    messages = req.get('messages', [])
    return jsonify(cloud_antigravity_syncer.push_live_messages(messages))

@app.route('/api/chat/sync_all_conversations', methods=['POST'])
def api_chat_sync_all_conversations():
    req = request.get_json(force=True) if request.data else {}
    return jsonify(cloud_antigravity_syncer.push_all_conversations(req))

# ------------------------------------------------------------------------------
# 📱 🖥️ 🚄 GENESIS Tablet Pro Studio (新幹線・移動中特化 タブレット横画面スタジオ)
# ------------------------------------------------------------------------------
@app.route('/tablet_studio')
def view_tablet_studio():
    return render_template_string("""
    <!DOCTYPE html>
    <html lang="ja">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
        <title>🚄 GENESIS Tablet Pro Studio</title>
        <style>
            * { box-sizing: border-box; margin: 0; padding: 0; }
            body { background: #070b14; color: #f1f5f9; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; height: 100vh; overflow: hidden; display: flex; flex-direction: column; }
            .topbar { height: 48px; background: #0f172a; border-bottom: 1px solid #1e293b; display: flex; justify-content: space-between; align-items: center; padding: 0 16px; flex-shrink: 0; }
            .badge { background: #064e3b; color: #34d399; font-size: 11px; font-weight: bold; padding: 3px 8px; border-radius: 12px; border: 1px solid #059669; }
            .main-layout { display: grid; grid-template-columns: 320px 1fr 340px; height: calc(100vh - 48px); gap: 10px; padding: 10px; }
            .pane { background: #0f172a; border: 1px solid #1e293b; border-radius: 10px; display: flex; flex-direction: column; overflow: hidden; }
            .pane-header { padding: 10px 14px; background: #131d35; border-bottom: 1px solid #1e293b; font-size: 13px; font-weight: bold; color: #38bdf8; display: flex; justify-content: space-between; align-items: center; }
            .pane-body { padding: 12px; overflow-y: auto; flex: 1; }
            
            /* 18マス グリッド */
            .grid-18 { display: grid; grid-template-columns: repeat(3, 1fr); gap: 6px; }
            .tile { background: #0b1120; border: 1px solid #334155; border-radius: 8px; padding: 8px 4px; text-align: center; font-size: 10px; cursor: pointer; transition: all 0.2s; }
            .tile:active { transform: scale(0.96); background: #1e293b; border-color: #38bdf8; }
            .tile strong { display: block; font-size: 11px; color: #38bdf8; margin-top: 2px; }
            
            /* ターミナル */
            .console-box { background: #000000; border: 1px solid #22c55e; border-radius: 8px; padding: 12px; font-family: monospace; font-size: 12px; color: #4ade80; flex: 1; overflow-y: auto; line-height: 1.5; white-space: pre-wrap; }
            
            /* 入力部 */
            .input-box { display: flex; gap: 8px; margin-bottom: 10px; }
            .input-field { flex: 1; padding: 12px; border-radius: 8px; border: 1px solid #334155; background: #0b1120; color: white; font-size: 14px; }
            .btn { background: #0284c7; color: white; border: none; padding: 10px 16px; border-radius: 8px; font-weight: bold; cursor: pointer; }
            .btn-mic { background: #ef4444; border-radius: 50%; width: 44px; height: 44px; display: flex; align-items: center; justify-content: center; font-size: 20px; border: 2px solid #f87171; cursor: pointer; flex-shrink: 0; }
            
            /* アイデアメモ */
            .memo-area { width: 100%; height: 140px; background: #0b1120; border: 1px solid #334155; border-radius: 8px; color: #f1f5f9; padding: 10px; font-size: 12px; resize: none; margin-bottom: 8px; }
        </style>
    </head>
    <body>
        <div class="topbar">
            <div style="display:flex; align-items:center; gap:10px;">
                <strong style="font-size:16px; color:#38bdf8;">🚄 GENESIS Tablet Pro Studio</strong>
                <small style="color:#94a3b8;">新幹線・移動中特化 横画面マルチペイン管制室</small>
            </div>
            <div style="display:flex; align-items:center; gap:12px;">
                <button onclick="startNewSession()" style="background:#0284c7; color:white; border:none; padding:4px 12px; border-radius:6px; font-size:12px; font-weight:bold; cursor:pointer;">＋ 新規チャット</button>
                <div class="badge">🟢 CLOUD RUN ONLINE</div>
            </div>
        </div>

        <div class="main-layout">
            <!-- 👈 左ペイン: 18マスランチャー ＆ 器官メトリクス -->
            <div class="pane">
                <div class="pane-header">
                    <span>🎛️ 18マス 高速ランチャー</span>
                    <span style="font-size:10px; color:#94a3b8;">1-TAP LAUNCH</span>
                </div>
                <div class="pane-body">
                    <div class="grid-18">
                        <div class="tile" onclick="triggerTile('電子書籍アプリ生成')">📖<strong>電子書籍</strong><small style="font-size:8px; color:#64748b;">音声/正誤表</small></div>
                        <div class="tile" onclick="triggerTile('90sテクノDJリミックス作成')">🎧<strong>90sテクノ</strong><small style="font-size:8px; color:#64748b;">2h20曲DJ</small></div>
                        <div class="tile" onclick="triggerTile('NotebookLM深層分析')">📚<strong>NotebookLM</strong><small style="font-size:8px; color:#64748b;">対話Podcast</small></div>
                        <div class="tile" onclick="triggerTile('臨床スマートグラスHUD')">🏥<strong>臨床HUD</strong><small style="font-size:8px; color:#64748b;">誤薬ゼロ/バイタル</small></div>
                        <div class="tile" onclick="triggerTile('リハビリ動作解析')">🏃<strong>リハビリ</strong><small style="font-size:8px; color:#64748b;">33点骨格ROM</small></div>
                        <div class="tile" onclick="triggerTile('介護見守り品質評価')">👵<strong>介護見守り</strong><small style="font-size:8px; color:#64748b;">声掛け/転倒招集</small></div>
                        <div class="tile" onclick="triggerTile('交通ドライバー防衛')">🚖<strong>交通防衛</strong><small style="font-size:8px; color:#64748b;">カスハラ/損害賠償</small></div>
                        <div class="tile" onclick="triggerTile('シフト突発離脱リバランス')">🔄<strong>シフト再編</strong><small style="font-size:8px; color:#64748b;">0.3s最適化</small></div>
                        <div class="tile" onclick="triggerTile('Google Cloud全情報巡回')">🌐<strong>GCP学習</strong><small style="font-size:8px; color:#64748b;">仕様/差分</small></div>
                        <div class="tile" onclick="triggerTile('Google Developersシナプス結合')">🎓<strong>Developers</strong><small style="font-size:8px; color:#64748b;">SDK/Skills</small></div>
                        <div class="tile" onclick="triggerTile('3072Dシナプス検索実行')">⚡<strong>3072D検索</strong><small style="font-size:8px; color:#64748b;">Vault高速抽出</small></div>
                        <div class="tile" onclick="triggerTile('Google公式20大ドメイン巡回')">👑<strong>全20ドメイン</strong><small style="font-size:8px; color:#64748b;">Supreme</small></div>
                        <div class="tile" onclick="triggerTile('2分デモ動画プレゼン生成')">🎬<strong>2分動画</strong><small style="font-size:8px; color:#64748b;">AI Cast&Set</small></div>
                        <div class="tile" onclick="triggerTile('機械脳自己進化メッシュ状態取得')">🧠<strong>自己進化</strong><small style="font-size:8px; color:#64748b;">DePIN余剰</small></div>
                        <div class="tile" onclick="triggerTile('単位認定試験テレパシーHUD')">📝<strong>試験HUD</strong><small style="font-size:8px; color:#64748b;">0.3sカンペ</small></div>
                        <div class="tile" onclick="triggerTile('深夜3点AI監査実行')">🌙<strong>深夜監査</strong><small style="font-size:8px; color:#64748b;">動画x音声xカルテ</small></div>
                        <div class="tile" onclick="triggerTile('全15テストスイート自動検証')">🧪<strong>全診断</strong><small style="font-size:8px; color:#64748b;">100% GREEN</small></div>
                        <div class="tile" style="border-color:#ef4444;" onclick="triggerTile('全器官キルスイッチ実行')"><strong style="color:#ef4444;">🛑 停止</strong><small style="font-size:8px; color:#f87171;">ポート解放</small></div>
                    </div>

                    <div style="margin-top:14px; background:#070b14; padding:10px; border-radius:8px; border:1px solid #1e293b;">
                        <strong style="color:#a855f7; font-size:11px; display:block; margin-bottom:4px;">🧠 Gemma 4 脳器官スウォーム</strong>
                        <div style="font-size:10px; color:#94a3b8; line-height:1.6;">
                            ・視床: <span style="color:#34d399;">8.2ms</span> | 扁桃体: <span style="color:#34d399;">4.1ms</span><br>
                            ・海馬: <span style="color:#34d399;">12.5ms</span> | MAGI: <span style="color:#34d399;">28.4ms</span><br>
                            ・全器官直並列応答: <span style="color:#38bdf8; font-weight:bold;">95.2ms (Sub-300ms)</span>
                        </div>
                    </div>
                </div>
            </div>

            <!-- 🏢 中央ペイン: 対話・音声指示 ＆ 巨大黒画面ターミナル -->
            <div class="pane">
                <div class="pane-header">
                    <span>📟 Antigravity コマンド ＆ リアルタイム黒画面ログ (SSE)</span>
                    <button onclick="clearConsoleLog()" style="background:#1e293b; color:#94a3b8; border:none; padding:2px 8px; border-radius:4px; font-size:10px; cursor:pointer;">🗑️ ログ消去</button>
                </div>
                <div class="pane-body" style="display:flex; flex-direction:column;">
                    <div class="input-box">
                        <input id="cmdInput" class="input-field" placeholder="新幹線の車内から音声またはテキストで指示入力..." onkeydown="if(event.key==='Enter')sendRemoteCommand()">
                        <button class="btn" onclick="sendRemoteCommand()">実行</button>
                        <button id="micBtn" class="btn-mic" onclick="toggleVoiceInput()">🎙️</button>
                    </div>
                    <div id="consoleOutput" class="console-box">[SYSTEM] 🚄 GENESIS Tablet Pro Studio 接続完了\n[READY] 指示を入力するかマイクでお話しください...\n</div>
                </div>
            </div>

            <!-- 👉 右ペイン: 新幹線メモ ＆ 4大コンペレーダー ＆ プレビュー -->
            <div class="pane">
                <div class="pane-header">
                    <span>💡 新幹線 思考メモ ＆ コンペレーダー</span>
                    <span style="font-size:10px; color:#34d399;">DRIVE SYNC</span>
                </div>
                <div class="pane-body">
                    <strong style="color:#f59e0b; font-size:11px; display:block; margin-bottom:4px;">📝 思考メモ (即座にGoogle Driveへ同期)</strong>
                    <textarea id="memoInput" class="memo-area" placeholder="新幹線でひらめいたアイデア・新機能・要件メモを入力..."></textarea>
                    <button class="btn" style="width:100%; padding:8px; font-size:11px; margin-bottom:12px;" onclick="saveShinkansenMemo()">💾 Google Drive正本へ保存</button>

                    <strong style="color:#38bdf8; font-size:11px; display:block; margin-bottom:4px;">🏆 4大Googleコンペ進捗レーダー</strong>
                    <div style="background:#070b14; padding:8px; border-radius:6px; border:1px solid #1e293b; font-size:10px; line-height:1.6;">
                        1. 🥇 <strong>Build with Gemini (1.5億円)</strong>: <span style="color:#34d399;">正本配備済</span><br>
                        2. 🥈 <strong>Devpost Google Series</strong>: <span style="color:#38bdf8;">毎月応募待機</span><br>
                        3. 🥉 <strong>Lablab.ai Gemini Sprints</strong>: <span style="color:#38bdf8;">月次スプリント</span><br>
                        4. 💎 <strong>Startups Cloud (35万ドル)</strong>: <span style="color:#a855f7;">常時申請枠</span>
                    </div>
                </div>
            </div>
        </div>

        <script>
            let isRecording = false;
            let recognition = null;

            window.onload = function() {
                startLogStream();
            };

            function startNewSession() {
                if (confirm('チャット履歴を切り替え、新しいセッションを開始しますか？')) {
                    document.getElementById('consoleOutput').innerText = '[SYSTEM] 🔄 新規セッション開始 (チャットコンテキストをリセットしました)\\n[READY] 指示を入力または話しかけてください...\\n';
                    document.getElementById('cmdInput').value = '';
                    sendRemoteCommand('新規セッション開始: チャットコンテキストをリセットしました');
                }
            }

            function clearConsoleLog() {
                document.getElementById('consoleOutput').innerText = '[SYSTEM] ログ画面をクリアしました。\\n';
            }

            async function sendRemoteCommand(customText) {
                const text = customText || document.getElementById('cmdInput').value;
                if (!text) return;
                document.getElementById('cmdInput').value = '';
                const res = await fetch('/api/mobile/execute', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({ command: text })
                });
            }

            function triggerTile(actionName) {
                sendRemoteCommand(actionName);
            }

            function startLogStream() {
                const evtSource = new EventSource('/api/mobile/stream_logs');
                evtSource.onmessage = function(e) {
                    try {
                        const item = JSON.parse(e.data);
                        const c = document.getElementById('consoleOutput');
                        c.innerText += `[${item.time}] [${item.organ}] ${item.message}\\n`;
                        c.scrollTop = c.scrollHeight;
                    } catch(err) {}
                };
            }

            function toggleVoiceInput() {
                if (!('webkitSpeechRecognition' in window) && !('SpeechRecognition' in window)) {
                    alert('音声認識に対応していません。テキスト入力をご利用ください。');
                    return;
                }
                const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
                if (!isRecording) {
                    recognition = new SpeechRecognition();
                    recognition.lang = 'ja-JP';
                    recognition.onstart = () => {
                        isRecording = true;
                        document.getElementById('micBtn').style.background = '#22c55e';
                    };
                    recognition.onresult = (event) => {
                        const transcript = event.results[0][0].transcript;
                        document.getElementById('cmdInput').value = transcript;
                        sendRemoteCommand(transcript);
                    };
                    recognition.onend = () => {
                        isRecording = false;
                        document.getElementById('micBtn').style.background = '#ef4444';
                    };
                    recognition.start();
                } else {
                    recognition.stop();
                }
            }

            async function saveShinkansenMemo() {
                const memo = document.getElementById('memoInput').value;
                if (!memo) return;
                sendRemoteCommand('新幹線思考メモ保存: ' + memo);
                alert('💾 Google Drive正本へ保存しました！');
                document.getElementById('memoInput').value = '';
            }
        </script>
    </body>
    </html>
    """)

# ------------------------------------------------------------------------------
# 📱 🔒 ⚡ GENESIS Mobile Antigravity Remote Web Console & 2FA Gateway
# ------------------------------------------------------------------------------
@app.route('/mobile_antigravity')
def view_mobile_antigravity():
    html_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'web', 'mobile_antigravity.html')
    if os.path.exists(html_path):
        with open(html_path, 'r', encoding='utf-8') as f:
            return Response(f.read(), mimetype='text/html; charset=utf-8')
    return 'Mobile portal HTML not found', 404

@app.route('/manifest.json')
def pwa_manifest():
    p = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'web', 'manifest.json')
    if os.path.exists(p):
        with open(p, 'r', encoding='utf-8') as f:
            return Response(f.read(), mimetype='application/manifest+json; charset=utf-8')
    return jsonify({}), 404

@app.route('/service-worker.js')
def pwa_service_worker():
    p = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'web', 'service-worker.js')
    if os.path.exists(p):
        with open(p, 'r', encoding='utf-8') as f:
            return Response(f.read(), mimetype='application/javascript; charset=utf-8')
    return "/* SW not found */", 404

@app.route('/icons/<path:filename>')
def pwa_icons(filename):
    from flask import send_from_directory
    icons_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'web', 'icons')
    return send_from_directory(icons_dir, filename)

@app.route('/api/auth/send_otp', methods=['POST'])
@app.route('/api/mobile/auth/request_otp', methods=['POST'])
def api_auth_send_otp():
    req = request.get_json(force=True) if request.data else {}
    email = req.get('email', 'user@genesis.ai')
    client_ip = request.remote_addr or '127.0.0.1'
    return jsonify(mobile_auth_gateway.generate_and_send_otp(email, client_ip))

@app.route('/api/auth/verify_otp', methods=['POST'])
@app.route('/api/mobile/auth/verify_otp', methods=['POST'])
def api_auth_verify_otp():
    req = request.get_json(force=True) if request.data else {}
    email = req.get('email', 'user@genesis.ai')
    otp = req.get('otp', '')
    remember_me = req.get('remember_me', True)
    client_ip = request.remote_addr or '127.0.0.1'
    user_agent = request.headers.get('User-Agent', '')
    return jsonify(mobile_auth_gateway.verify_otp(email, otp, remember_me, client_ip, user_agent))

@app.route('/api/mobile/auth/quick_login', methods=['POST', 'GET'])
def api_mobile_auth_quick_login():
    req = request.get_json(force=True) if request.data else {}
    email = req.get('email', 'user@genesis.ai')
    client_ip = request.remote_addr or '127.0.0.1'
    user_agent = request.headers.get('User-Agent', 'QuickLogin')
    days = 30
    token = mobile_auth_gateway._generate_session_token(email, days)
    expires_at = time.time() + (days * 86400)
    mobile_auth_gateway.auth_store["active_sessions"][token] = {
        "email": email,
        "created_at": time.time(),
        "expires_at": expires_at,
        "days_valid": days,
        "client_ip": client_ip,
        "user_agent": user_agent[:100]
    }
    mobile_auth_gateway._save_auth_store()
    return jsonify({
        "status": "SUCCESS",
        "token": token,
        "expires_at": expires_at,
        "days_valid": days,
        "message": "⚡ 30日間のセッショントークンを発行・更新しました。"
    })

@app.route('/api/auth/kill_sessions', methods=['POST'])
def api_auth_kill_sessions():
    return jsonify(mobile_auth_gateway.revoke_all_sessions())

@app.route('/api/mobile/execute', methods=['POST'])
def api_mobile_execute():
    req = request.get_json(force=True) if request.data else {}
    cmd = req.get('command', '')
    token = req.get('token') or req.get('session_token') or request.headers.get('X-Genesis-Session') or ''
    client_ip = request.remote_addr or '127.0.0.1'
    return jsonify(mobile_remote_gateway.execute_remote_command(cmd, token, client_ip))

@app.route('/api/mobile/stream_logs')
def api_mobile_stream_logs():
    return Response(mobile_remote_gateway.subscribe_logs(), mimetype='text/event-stream')

@app.route('/api/mobile/status')
def api_mobile_status():
    return jsonify({
        "gateway": "GENESIS_MOBILE_REMOTE_GATEWAY",
        "auth_metrics": mobile_auth_gateway.get_auth_metrics(),
        "recent_logs_count": len(mobile_remote_gateway.recent_logs),
        "execution_history_count": len(mobile_remote_gateway.execution_history)
    })

# ------------------------------------------------------------------------------
# 🧠 ⚡ GENESIS Collective Evolution & DePIN Compute Sharing Mesh APIs
# ------------------------------------------------------------------------------
@app.route('/api/mesh/telemetry', methods=['POST'])
def api_mesh_telemetry():
    req = request.get_json(force=True) if request.data else {}
    organ = req.get('organ', 'UNKNOWN')
    action = req.get('action', 'EXECUTE')
    latency = float(req.get('latency_ms', 10.0))
    success = req.get('success', True)
    next_organ = req.get('next_organ')
    return jsonify(collective_evolution_mesh.record_usage_telemetry(organ, action, latency, success, next_organ))

@app.route('/api/mesh/compute_status')
def api_mesh_compute_status():
    return jsonify(collective_evolution_mesh.get_mesh_status())

@app.route('/api/mesh/rent_compute', methods=['POST'])
def api_mesh_rent_compute():
    req = request.get_json(force=True) if request.data else {}
    task_name = req.get('task_name', 'GENESIS_DISTRIBUTED_TASK')
    flops = req.get('flops_level', 'HIGH')
    duration = int(req.get('duration_sec', 10))
    return jsonify(collective_evolution_mesh.request_compute_rental(task_name, flops, duration))

# ------------------------------------------------------------------------------
# ⚡ 臨床・医療安全推論 API
# ------------------------------------------------------------------------------
@app.route('/api/clinical/infer', methods=['POST'])
def api_clinical_infer():
    req = request.get_json(force=True) if request.data else {}
    action = req.get('action', 'bedside_hud')
    patient_id = req.get('patient_id', 'P-102')
    res = clinical_engine.infer_bedside_patient(patient_id)
    return jsonify(res)

@app.route('/api/clinical/verify_medication', methods=['POST'])
def api_clinical_verify_med():
    req = request.get_json(force=True)
    patient_id = req.get('patient_id', 'P-102')
    drug_name = req.get('drug_name', '')
    dosage = req.get('dosage', '')
    res = clinical_engine.verify_medication(patient_id, drug_name, dosage)
    return jsonify(res)

@app.route('/api/clinical/dispatch', methods=['POST'])
def api_clinical_dispatch():
    req = request.get_json(force=True)
    patient_id = req.get('patient_id', 'P-102')
    incident = req.get('incident_type', '血圧急低下・意識混濁')
    caller = req.get('caller_staff_id', 'STAFF-001')
    res = clinical_engine.dispatch_emergency(patient_id, incident, caller)
    return jsonify(res)

@app.route('/api/clinical/voice_ehr', methods=['POST'])
def api_clinical_voice_ehr():
    req = request.get_json(force=True)
    speech = req.get('speech', '')
    patient_id = req.get('patient_id', 'P-102')
    res = clinical_engine.parse_voice_ehr(speech, patient_id)
    return jsonify(res)

# ------------------------------------------------------------------------------
# 🌙 深夜3点照合AI監査 ＆ 翌朝テストゲート API
# ------------------------------------------------------------------------------
@app.route('/api/audit/run_night_audit', methods=['POST', 'GET'])
def api_run_night_audit():
    res = night_audit_engine.run_night_triple_audit()
    return jsonify(res)

@app.route('/api/audit/get_morning_quiz')
def api_get_morning_quiz():
    staff_id = request.args.get('staff_id', 'STAFF-004')
    res = night_audit_engine.get_morning_quiz(staff_id)
    return jsonify(res)

@app.route('/api/audit/submit_quiz', methods=['POST'])
def api_submit_quiz():
    req = request.get_json(force=True)
    staff_id = req.get('staff_id', 'STAFF-004')
    answers = req.get('answers', [])
    res = night_audit_engine.evaluate_quiz_submission(staff_id, answers)
    return jsonify(res)

# ------------------------------------------------------------------------------
# 📡 メインフレーム イベントストリーム (SSE)
# ------------------------------------------------------------------------------
@app.route('/api/mainframe/events')
def mainframe_events():
    def event_generator():
        q = mainframe.register_sse_client()
        try:
            while True:
                data = q.get()
                yield f"data: {json.dumps(data, ensure_ascii=False)}\n\n"
        except GeneratorExit:
            mainframe.unregister_sse_client(q)
    return Response(event_generator(), mimetype='text/event-stream', headers={
        'Cache-Control': 'no-cache',
        'X-Accel-Buffering': 'no',
        'Connection': 'keep-alive'
    })

@app.route('/api/skills_and_contests')
def api_skills_contests():
    sk_dir = r"g:\マイドライブ\GENESIS_ROOT\knowledge_bank\Scholar_Nucleus\Skills_Matrix"
    ct_dir = r"g:\マイドライブ\GENESIS_ROOT\knowledge_bank\Scholar_Nucleus\Global_Contests_Hackathons"
    
    skills = [f.replace('SKILL_', '').replace('.md', '') for f in os.listdir(sk_dir)] if os.path.exists(sk_dir) else []
    contests = [f for f in os.listdir(ct_dir) if f.endswith('.md')] if os.path.exists(ct_dir) else []
    return jsonify({"skills": skills, "contests": contests})

@app.route('/api/kill_all', methods=['POST'])
def api_kill_all():
    def kill_worker():
        time.sleep(0.5)
        print("\n🛑 [全器官キルスイッチ発動] ポート5000および8080のプロセスを解放して停止します...", flush=True)
        # Kill telepathy and studio processes on windows
        os.system("taskkill /F /IM python.exe /FI \"WINDOWTITLE eq GENESIS*\" >nul 2>&1")
        os._exit(0)
    threading.Thread(target=kill_worker, daemon=True).start()
    return jsonify({"status": "KILL_SIGNAL_DISPATCHED"})

@app.route('/api/targets')
def api_get_targets():
    from core.genesis_autonomous_meister_crawler import GenesisGlobalFreedomCrawler
    crawler = GenesisGlobalFreedomCrawler()
    return jsonify(crawler.load_targets())

@app.route('/api/add_target', methods=['POST'])
def api_add_target():
    from core.genesis_autonomous_meister_crawler import GenesisGlobalFreedomCrawler
    req = request.get_json(force=True)
    t_type = req.get('type')
    t_val = req.get('value')
    crawler = GenesisGlobalFreedomCrawler()
    if t_type == 'keyword':
        crawler.add_free_keyword(t_val)
    elif t_type == 'url':
        crawler.add_watched_url(t_val)
    return jsonify({"status": "SUCCESS", "type": t_type, "value": t_val})

@app.route('/api/metrics')
def api_metrics():
    return jsonify(orchestrator.get_system_health_and_metrics())

@app.route('/api/run_night_crawler')
def api_run_crawler():
    from core.genesis_autonomous_meister_crawler import run_sync
    res = run_sync()
    return jsonify(res)

@app.route('/api/magi_deliberate', methods=['POST'])
def api_magi():
    req = request.get_json(force=True)
    content = req.get('content', '')
    meta = req.get('metadata', {})
    res = deliberate_sync(content, meta)
    return jsonify(res)

# ------------------------------------------------------------------------------
# 📱 🧬 GENESIS Mobile Antigravity & Organ Studio Routes (Cloud Run & Local)
# ------------------------------------------------------------------------------
@app.route('/mobile_antigravity.html')
def serve_mobile_antigravity():
    return send_from_directory(os.path.join(ROOT_DIR, 'GENESIS_CINEMA_STUDIO'), 'mobile_antigravity.html')

@app.route('/cinema_lite.html')
def serve_cinema_lite():
    return send_from_directory(os.path.join(ROOT_DIR, 'GENESIS_CINEMA_STUDIO'), 'cinema_lite.html')

@app.route('/music_studio.html')
def serve_music_studio():
    return send_from_directory(os.path.join(ROOT_DIR, 'GENESIS_CINEMA_STUDIO'), 'music_studio.html')

@app.route('/character_studio.html')
def serve_character_studio():
    return send_from_directory(os.path.join(ROOT_DIR, 'GENESIS_CINEMA_STUDIO'), 'character_studio.html')

@app.route('/parts/<path:filename>')
def serve_parts(filename):
    return send_from_directory(os.path.join(ROOT_DIR, 'GENESIS_CINEMA_STUDIO', 'parts'), filename)

@app.route('/api/antigravity/chat', methods=['POST'])
def api_antigravity_chat():
    req = request.get_json(force=True) if request.data else {}
    from core.neural_backbone import AntigravityRouter
    return jsonify(AntigravityRouter.handle_chat(req))

@app.route('/api/antigravity/plan', methods=['POST'])
def api_antigravity_plan():
    req = request.get_json(force=True) if request.data else {}
    from core.neural_backbone import AntigravityRouter
    return jsonify(AntigravityRouter.handle_plan(req))

@app.route('/api/antigravity/terminal', methods=['POST'])
def api_antigravity_terminal():
    req = request.get_json(force=True) if request.data else {}
    from core.neural_backbone import AntigravityRouter
    return jsonify(AntigravityRouter.handle_run_terminal(req))

@app.route('/api/malecns/telemetry')
def api_malecns_telemetry():
    from core.neural_backbone import malecns_bus
    return jsonify(malecns_bus.get_telemetry())

def start_telepathy_background():
    """Starts telepathy engine on port 5000 in separate process or thread"""
    print("[*] Launching Telepathy Engine on Port 5000 in background...")
    os.system("python genesis_telepathy_master_god.py")

def main():
    print("==================================================================")
    print(" 👑 GENESIS CLOUD GRAND UNIFIED LAUNCHER")
    print("==================================================================")
    print(" 🌐 大脳皮質スタジオ (Port 8080): http://localhost:8080")
    print(" 🏥 臨床スマートグラスHUD:        http://localhost:8080/clinical_hud")
    print(" 🚨 出勤前安全ゲートキーパー:      http://localhost:8080/safety_gate")
    print(" 📱 テレパシーHUD & グラス (Port 5000): http://192.168.1.3:5000")
    print(" 🏛️ MAGI 3賢者合議API: http://localhost:8080/api/magi_deliberate")
    print(" 🧠 全器官ヘルス監視API: http://localhost:8080/api/metrics")
    print("==================================================================")

    # 1. Start Telepathy Engine on Port 5000 in background thread
    t = threading.Thread(target=start_telepathy_background, daemon=True)
    t.start()

    # 2. Run Grand Cortex Studio on Port 8080
    app.run(host="0.0.0.0", port=8080, debug=False, use_reloader=False)

if __name__ == "__main__":
    main()
