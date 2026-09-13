# -*- coding: utf-8 -*-
import os
import sys
import shutil
import subprocess

try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass

SRC_DIR = r"g:\マイドライブ\GENESIS_ROOT"
STAGE_DIR = r"C:\Users\magic\.genesis_deploy"

print("==================================================================")
print(" [GENESIS CLOUD DEPLOYER] Staging clean codebase...")
print("==================================================================")

if os.path.exists(STAGE_DIR):
    shutil.rmtree(STAGE_DIR, ignore_errors=True)
os.makedirs(STAGE_DIR, exist_ok=True)

INCLUDE_ITEMS = [
    "core",
    "web",
    "GENESIS_CINEMA_STUDIO",
    "Dockerfile",
    "requirements.txt",
    "LAUNCH_GENESIS_CLOUD.py",
    "genesis_telepathy_master_god.py"
]

for item in INCLUDE_ITEMS:
    s = os.path.join(SRC_DIR, item)
    d = os.path.join(STAGE_DIR, item)
    if os.path.isdir(s):
        shutil.copytree(s, d, ignore=shutil.ignore_patterns('__pycache__', '*.pyc', '*.mp4', '*.zip'))
        print(f"  Synced directory: {item}")
    elif os.path.isfile(s):
        shutil.copy2(s, d)
        print(f"  Synced file: {item}")

# 🧠 リアルタイムチャットログ (transcript.jsonl) のクラウド同期
import json
log_path = r'C:\Users\magic\.gemini\antigravity\brain\d02a22b7-be4e-4994-8b7f-8099c4a32fb2\.system_generated\logs\transcript.jsonl'
live_messages = []
if os.path.exists(log_path):
    try:
        with open(log_path, 'r', encoding='utf-8') as f:
            lines = [json.loads(line) for line in f if line.strip()]
        
        dialogues = []
        current_user = None
        current_assistant = None
        
        for step in lines:
            stype = step.get('type')
            content = step.get('content', '')
            if stype == 'USER_INPUT' and content:
                if '<USER_REQUEST>' in content:
                    u_text = content.split('<USER_REQUEST>')[1].split('</USER_REQUEST>')[0].strip()
                    if u_text:
                        if current_user is not None:
                            if current_assistant is not None:
                                dialogues.append({'role': 'user', 'text': current_user})
                                dialogues.append({'role': 'assistant', 'text': current_assistant})
                                current_assistant = None
                                current_user = u_text
                            else:
                                current_user = u_text
                        else:
                            current_user = u_text
            elif stype == 'PLANNER_RESPONSE' and content:
                c_text = content.strip()
                if not c_text.startswith('Thought:') and not c_text.startswith('{') and len(c_text) > 0:
                    if not any(k in c_text for k in ['検証を行っております', '少々お待ちください', 'ツリーAPIの動作確認', '動的リアルタイム同期', 'スマホからの送信コマンド処理', '下部入力バーの被り解消', '最後の一文の欠落防止', 'IME途中送信', 'manualSync', 'ユーザー様の素晴らしい閃き', '双方向データ反映']):
                        current_assistant = c_text
        
        if current_user is not None:
            dialogues.append({'role': 'user', 'text': current_user})
            if current_assistant is not None:
                dialogues.append({'role': 'assistant', 'text': current_assistant})
        
        live_messages = dialogues
    except Exception as e:
        print(f"  [WARN] Transcript sync failed: {e}")

if live_messages:
    dest_json = os.path.join(STAGE_DIR, 'core', 'brain_live_transcript.json')
    with open(dest_json, 'w', encoding='utf-8') as f:
        json.dump(live_messages, f, ensure_ascii=False, indent=2)
    print(f"  [BRAIN SYNC] Successfully synced {len(live_messages)} pure authentic full-text chat messages to Cloud Run package!")

dockerignore_content = """
__pycache__
*.pyc
*.pyo
*.pyd
*.mp4
*.zip
"""
with open(os.path.join(STAGE_DIR, ".dockerignore"), "w", encoding="utf-8") as f:
    f.write(dockerignore_content.strip())

print(f"\nStaging complete: {STAGE_DIR}")
print("Launching Google Cloud Run deploy...\n")

cmd = (
    "gcloud run deploy genesis-cognitive-cortex "
    "--source . "
    "--platform managed "
    "--region asia-northeast1 "
    "--allow-unauthenticated "
    "--memory 2Gi "
    "--cpu 2 "
    "--min-instances 0 "
    "--max-instances 5 "
    "--set-env-vars PYTHONUNBUFFERED=1"
)

proc = subprocess.Popen(cmd, cwd=STAGE_DIR, shell=True)
proc.wait()
sys.exit(proc.returncode)
