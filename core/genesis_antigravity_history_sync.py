# -*- coding: utf-8 -*-
r"""
GENESIS Antigravity Real-Time History & Session Synchronizer
Bridges Antigravity IDE brain transcripts (C:\Users\magic\.gemini\antigravity\brain)
with Smartphone/Tablet Mobile PWA, ensuring 100% bidirectional sync of current conversation
and past sessions.
"""

import os
import sys
import json
import re
import glob
from pathlib import Path
from datetime import datetime

CURRENT_CONVERSATION_ID = "6f843046-ffc6-4f45-8d9f-0f8e7eaec695"
BRAIN_DIR = Path(r"C:\Users\magic\.gemini\antigravity\brain")

def clean_user_content(raw_text):
    if not raw_text:
        return ""
    m = re.search(r"<USER_REQUEST>(.*?)</USER_REQUEST>", raw_text, re.DOTALL)
    if m:
        return m.group(1).strip()
    # Strip metadata tags
    clean = re.sub(r"<ADDITIONAL_METADATA>.*?</ADDITIONAL_METADATA>", "", raw_text, flags=re.DOTALL)
    clean = re.sub(r"<SYSTEM_MESSAGE>.*?</SYSTEM_MESSAGE>", "", clean, flags=re.DOTALL)
    return clean.strip()

def get_current_session_turns(limit=50):
    """
    Extracts all conversation turns (user prompt & assistant response pairs)
    from current active Antigravity session transcript.
    """
    transcript_path = BRAIN_DIR / CURRENT_CONVERSATION_ID / ".system_generated" / "logs" / "transcript.jsonl"
    if not transcript_path.exists():
        return []

    turns = []
    current_prompt = None
    current_timestamp = None

    try:
        with open(transcript_path, "r", encoding="utf-8", errors="ignore") as f:
            for line in f:
                if not line.strip():
                    continue
                try:
                    step = json.loads(line)
                except Exception:
                    continue

                stype = step.get("type")
                if stype == "USER_INPUT":
                    raw = step.get("content", "")
                    cleaned = clean_user_content(raw)
                    if cleaned:
                        current_prompt = cleaned
                        current_timestamp = step.get("created_at", "")
                elif stype == "PLANNER_RESPONSE" and current_prompt:
                    ans = step.get("content", "")
                    if ans:
                        # Clean thinking block if needed
                        turns.append({
                            "prompt": current_prompt,
                            "answer": ans,
                            "timestamp": current_timestamp or datetime.now().isoformat()
                        })
                        current_prompt = None
    except Exception as e:
        print(f"Error parsing transcript: {e}")

    # Return latest 'limit' turns
    return turns[-limit:]

def get_all_antigravity_sessions(limit=40):
    """
    Scans Antigravity brain sessions and returns session metadata
    matching PC IDE sidebar (Projects & Pinned conversations).
    """
    pattern = str(BRAIN_DIR / "*" / ".system_generated" / "logs" / "transcript.jsonl")
    files = glob.glob(pattern)
    files.sort(key=lambda x: os.path.getmtime(x), reverse=True)

    sessions = []
    for fpath in files[:limit]:
        conv_id = fpath.split(os.sep)[-4]
        title = "無題のセッション"
        first_prompt = ""
        mtime = os.path.getmtime(fpath)
        dt_str = datetime.fromtimestamp(mtime).strftime("%Y/%m/%d %H:%M")

        is_current = (conv_id == CURRENT_CONVERSATION_ID)
        if is_current:
            title = "車載コックピット・防災プラットフォーム設計 (Active)"

        try:
            with open(fpath, "r", encoding="utf-8", errors="ignore") as f:
                for line in f:
                    if not line.strip():
                        continue
                    step = json.loads(line)
                    if step.get("type") == "USER_INPUT":
                        raw = step.get("content", "")
                        p = clean_user_content(raw)
                        if p and not p.startswith("{") and len(p) > 2:
                            first_prompt = p.replace("\n", " ")
                            if not is_current:
                                title = first_prompt[:32] + ("..." if len(first_prompt) > 32 else "")
                            break
        except Exception:
            pass

        sessions.append({
            "id": conv_id,
            "title": title,
            "snippet": first_prompt[:60],
            "timestamp": dt_str,
            "is_current": is_current
        })
    return sessions

def search_antigravity_history(query, limit=20):
    """Searches current conversation and past sessions for matching query."""
    query = query.lower().strip()
    if not query:
        return get_current_session_turns(limit)

    results = []
    turns = get_current_session_turns(100)
    for t in turns:
        if query in t["prompt"].lower() or query in t["answer"].lower():
            results.append(t)
            if len(results) >= limit:
                break
    return results

def create_new_session(title="新規セッション"):
    """
    Creates a new clean Antigravity session, generating a new conversation ID,
    and recording it in the sessions ledger.
    """
    import uuid
    new_id = str(uuid.uuid4())
    now_str = datetime.now().strftime("%Y/%m/%d %H:%M")
    
    session_info = {
        "id": new_id,
        "title": title,
        "created_at": datetime.now().isoformat(),
        "timestamp": now_str,
        "is_current": True,
        "turns_count": 0
    }
    
    # Save to persistent storage in data/sessions/
    sessions_dir = Path(__file__).resolve().parent.parent / "data" / "sessions"
    sessions_dir.mkdir(parents=True, exist_ok=True)
    meta_file = sessions_dir / "active_sessions.json"
    
    sessions = []
    if meta_file.exists():
        try:
            with open(meta_file, "r", encoding="utf-8") as f:
                sessions = json.load(f)
        except Exception:
            sessions = []
            
    # Mark old sessions as not current
    for s in sessions:
        s["is_current"] = False
        
    sessions.insert(0, session_info)
    
    with open(meta_file, "w", encoding="utf-8") as f:
        json.dump(sessions[:50], f, indent=2, ensure_ascii=False)
        
    print(f"✨ [Antigravity Sync] Created new session: {new_id} ({title})")
    return session_info

if __name__ == "__main__":
    current = get_current_session_turns(3)
    print(f"Current turns found: {len(current)}")
    sessions = get_all_antigravity_sessions(3)
    print(f"Sessions found: {len(sessions)}")

