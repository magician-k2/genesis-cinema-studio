import os
import sys
import json
import requests

sys.stdout.reconfigure(encoding='utf-8', line_buffering=True)
sys.stderr.reconfigure(encoding='utf-8', line_buffering=True)

OLLAMA_URL = "http://127.0.0.1:11434/api/generate"
MODEL_NAME = "gemma4:e2b-it-qat"

prompt = """
あなたはGoogleの次世代オープンモデル「Gemma 4」であり、GENESIS CINEMA STUDIOのチーフAIアーキテクトです。

ユーザー様から、映画制作・キャラクター生成の領域において極めて革命的な【新機能の閃き】をいただきました：

【ユーザー様からの閃き・新機能提案】
「人物生成でスマホ写真から現実の人物（アイドルやインディーズ俳優）を4面生成・Vault登録できるようにした。
簡単な演技はプロンプトでも可能だが、スマホで録画した人間のリアルな動き（あるいはYouTube等の動画サイトから『この数秒間だけ切り抜いたダンスやアクション』）を取り込み、生成したキャラクターに全く同じ動きを演技させる【簡易型モーションキャプチャー＆ポーズ・演技トランスファー機能】を搭載するのはどうか？」

【チーフAIアーキテクト（Gemma 4）への監査・技術設計指示】
以下の項目について、日本のユーザー様に向けて100%日本語で、最高に情熱的かつ工学的に明快に回答してください：

1. 【革新性の評価】
   - このアイデアが、AI映画制作・バーチャルプロダクションの世界（特にGoogle Cloud主催 Agentic Cinema Hackathon）においてどれほど破壊的な強みになるか。
2. 【Googleエコシステムとの完璧な親和性】
   - Google公式の「MediaPipe Pose / BlazePose」（スマホ・ブラウザ・エッジで30fps以上で動く超軽量骨格推定）をどう組み込むべきか。
3. 【具体的なアーキテクチャ・パイプライン構成】
   - 入力：スマホ録画動画（MP4/WebM）またはYouTube等の切り抜き動画
   - モーキャプ：MediaPipeによる33個の3D骨格ランドマーク（キーポーズ・骨格ボーン抽出）
   - Gemma 4の役割：骨格シーケンスから「演技ト書き（Stage Directions）」「関節の角速度」「カメラアングル追従指示」をローカルで超高速言語化＆Veoプロンプト変換
   - 出力：登録キャラクター（Vaultの32bit透過演者）が指定の実写ストリートビュー上で全く同じ動き・タイミングで演技するプレビュー
4. 【ユーザー様への推奨実装ステップ】
   - 最短・最高精度でフロントエンド（Cinema Studio UI）とバックエンド（server.py / mocap_engine.py）に組み込むための具体的提案。
"""

print("[Gemma 4] モーションキャプチャー新機能の深層技術監査を開始...", flush=True)

try:
    res = requests.post(OLLAMA_URL, json={
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False
    }, timeout=180)
    
    if res.status_code == 200:
        audit_result = res.json().get("response", "").strip()
        out_file = r"g:\マイドライブ\GENESIS_ROOT\GEMMA4_MOCAP_AUDIT_REPORT.md"
        with open(out_file, "w", encoding="utf-8") as out_f:
            out_f.write(audit_result)
        print("[Gemma 4] モーキャプ機能の監査レポート生成が完了しました！", flush=True)
        print(f"レポート保存先: {out_file}")
    else:
        print(f"Ollama Error: {res.status_code} - {res.text}", flush=True)
except Exception as e:
    print(f"Execution Error: {e}", flush=True)
