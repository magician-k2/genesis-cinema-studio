import os
import sys
import json
import requests

sys.stdout.reconfigure(encoding='utf-8', line_buffering=True)
sys.stderr.reconfigure(encoding='utf-8', line_buffering=True)

OLLAMA_URL = "http://127.0.0.1:11434/api/generate"
MODEL_NAME = "gemma4:e2b-it-qat"

proposal_path = r"g:\マイドライブ\GENESIS_ROOT\PROPOSAL_AGENTIC_CINEMA_HACKATHON.md"
with open(proposal_path, "r", encoding="utf-8") as f:
    proposal_text = f.read()

prompt = f"""
あなたはGoogleの次世代オープンモデル「Gemma 4」であり、GENESISシステムのチーフAIアーキテクトです。
現在、2026年9月9日締切のGoogle Cloud主催「Agentic Cinema Hackathon」に向けて、提出用プロポーザルおよびシステム全体の最終ブラッシュアップを行っています。

直近で以下の画期的な新機能が完全実装・テスト完了（100% PASS）しました：
1. 🎭 4面キャラクター自動スライス＆高精度切り抜き・ハリウッド級Defringeエンジン（Telea Inpaint Bleedによる輪郭白フチ・ハロー完全消去、32bit完全透過PNG Vault）
2. 🧍 実在人物（インディーズ俳優・アイドル）のスマホ写真4枚からの頭頂〜足元比率自動正規化・接地ピボット自動算出
3. 🌐 360°実写ストリートビュー（浅草・渋谷・パリ等）への演者ワンクリック召喚＆路面接地影（Contact Drop Shadow + アンビエントオクルージョン）による貼り絵感ゼロの実写融合
4. 🧠 Gemma 4ローカルモデル（On-Device / ゼロトークン・完全オフライン）によるセリフ・ト書き高速生成（8.5ms）とコード・プロポーザルの自己監査

【現在のプロポーザル】
{proposal_text}

【監査・改善指示】
審査員（Google Cloud & Replit、世界のトップエンジニア）に対して圧倒的な技術的優位性と独自性を強烈にアピールするため、以下の観点からプロポーザルおよび3分動画ストーリーボードの強化点を100%日本語で詳細に分析・提案してください：
1. 現在のプロポーザルに上記新機能（4面Defringe切り抜き・ストリートビュー実写召喚・Gemma 4オンデバイス協調）をどう組み込むべきか
2. 3分動画ストーリーボード（Scene 1〜6）におけるビフォーアフター映像の見せ方（切り抜きのクリアさ、影のリアルさ、Veo 3.1への入力の一貫性）
3. Replit / Google Cloud連携における審査員ウケする神アピールポイント（トークンコストゼロのGemma 4ローカルハイブリッド構成）
4. 具体的なプロポーザル修正文案（英語および日本語サマリー）
"""

print("[Gemma 4] Agentic Cinema Hackathon プロポーザル深層監査を開始...", flush=True)

try:
    res = requests.post(OLLAMA_URL, json={
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False
    }, timeout=180)
    
    if res.status_code == 200:
        audit_result = res.json().get("response", "").strip()
        out_file = r"g:\マイドライブ\GENESIS_ROOT\GEMMA4_CINEMA_HACKATHON_AUDIT_REPORT.md"
        with open(out_file, "w", encoding="utf-8") as out_f:
            out_f.write(audit_result)
        print("[Gemma 4] 監査レポートの生成が完了しました！", flush=True)
        print(f"レポート保存先: {out_file}")
    else:
        print(f"Ollama Error: {res.status_code} - {res.text}", flush=True)
except Exception as e:
    print(f"Execution Error: {e}", flush=True)
