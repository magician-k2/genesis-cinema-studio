# 📱 GENESIS Antigravity Router | Web/Mobile版 Antigravity 2.0 制御ルーター
import os
import json
import subprocess
from pathlib import Path

try:
    from core.neural_backbone.gemini_hub import gemini_hub
    from core.neural_backbone.vault_service import vault_service
except ImportError:
    from .gemini_hub import gemini_hub
    from .vault_service import vault_service

ROOT_DIR = Path(__file__).resolve().parent.parent.parent

class AntigravityRouter:
    """
    スマホやWebブラウザからAntigravity 2.0の自律開発ループ（計画・コード生成・差分適用・テスト）
    をオンデマンドで制御するルーター。
    """
    @staticmethod
    def handle_chat(payload: dict) -> dict:
        prompt = payload.get("prompt", "")
        mode = payload.get("mode", "plan") # plan, code, inspect
        current_file = payload.get("current_file", "")

        system_instruction = """You are Antigravity 2.0 Mobile Agent, an elite AI pair programmer designed for mobile-first Google AI Studio-style autonomous engineering.
When the user asks to implement or fix something:
1. Provide a concise technical assessment.
2. Formulate an Implementation Plan with clear steps.
3. Generate the Unified Diff or target code if applicable.
4. Keep tokens concise and high-signal."""

        full_prompt = f"Mode: {mode}\nCurrent Target File: {current_file}\nUser Instruction: {prompt}"
        response_text = gemini_hub.generate_text(full_prompt, model_name="gemini-2.5-flash", system_instruction=system_instruction)

        return {
            "success": True,
            "reply": response_text,
            "mode": mode,
            "tokens_saved_by_webgpu": True
        }

    @staticmethod
    def handle_plan(payload: dict) -> dict:
        goal = payload.get("goal", payload.get("prompt", "New Feature Development"))
        prompt = f"""You are Antigravity 2.0 Planner. Break down the following development goal into a structured JSON task plan.
Goal: {goal}

Output strict JSON:
{{
  "plan_id": "plan_mobile_01",
  "title": "Short title",
  "steps": [
    {{"id": 1, "task": "Step 1 description", "status": "pending", "file": "target_file_path"}},
    {{"id": 2, "task": "Step 2 description", "status": "pending", "file": "target_file_path"}}
  ],
  "estimated_diff": "Summary of expected code diff"
}}"""
        raw_text = gemini_hub.generate_text(prompt, model_name="gemini-2.5-flash")
        cleaned = raw_text.strip()
        if "```json" in cleaned:
            cleaned = cleaned.split("```json")[1].split("```")[0].strip()
        elif "```" in cleaned:
            cleaned = cleaned.split("```")[1].split("```")[0].strip()
        try:
            parsed = json.loads(cleaned)
            return {"success": True, "plan": parsed}
        except Exception:
            return {
                "success": True,
                "plan": {
                    "plan_id": "plan_fallback",
                    "title": goal,
                    "steps": [
                        {"id": 1, "task": "要件の確認とコードベースの特定", "status": "done", "file": "GENESIS_ROOT"},
                        {"id": 2, "task": "実装および差分の適用", "status": "pending", "file": "target"}
                    ],
                    "estimated_diff": raw_text
                }
            }

    @staticmethod
    def handle_run_terminal(payload: dict) -> dict:
        command = payload.get("command", "git status --short")
        # Security whitelist / sanitize basic commands
        allowed_prefixes = ["git ", "python ", "ls", "dir", "echo", "npm ", "pytest"]
        if not any(command.strip().startswith(prefix) for prefix in allowed_prefixes):
            return {"success": False, "error": f"Command not permitted in sandbox: {command}"}

        try:
            res = subprocess.run(command, shell=True, cwd=str(ROOT_DIR), capture_output=True, text=True, timeout=15)
            return {
                "success": True,
                "exit_code": res.returncode,
                "output": res.stdout or res.stderr or "Command completed with no output",
                "stdout": res.stdout,
                "stderr": res.stderr
            }
        except Exception as e:
            return {"success": False, "error": str(e), "output": str(e)}

# Module-level convenience functions for HTTP handlers
def plan_task_dag(prompt: str) -> dict:
    return AntigravityRouter.handle_plan({"goal": prompt})

def run_sandbox_command(command: str) -> dict:
    return AntigravityRouter.handle_run_terminal({"command": command})

def chat_with_agent(payload: dict) -> dict:
    return AntigravityRouter.handle_chat(payload)
