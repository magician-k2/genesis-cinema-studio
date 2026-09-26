"""
GENESIS Live Cyberpunk HUD Overlay
2.0 (指揮) ➔ IDE (現場) ➔ SDK (調停) の処理移送をデスクトップ上に直接可視化する最前面HUD
"""
import sys
import tkinter as tk

def show_hud(title="⚡ GENESIS 3重防壁連携", stage="2.0 ➔ IDE 処理移譲", detail="sidepanel.js (LSP監査・現場調整中)", duration_ms=2500):
    root = tk.Tk()
    root.title("GENESIS_ORCHESTRATION_HUD")
    root.attributes("-topmost", True)
    root.overrideredirect(True)
    root.attributes("-alpha", 0.94)

    # 画面サイズ取得
    screen_width = root.winfo_screenwidth()
    width = 460
    height = 76
    x = (screen_width - width) // 2  # 画面中央上部
    y = 24  # 上部から24px

    root.geometry(f"{width}x{height}+{x}+{y}")
    root.configure(bg="#050811")

    # 外枠
    frame = tk.Frame(root, bg="#050811", highlightbackground="#00f0ff", highlightthickness=1.5)
    frame.pack(fill=tk.BOTH, expand=True, padx=1, pady=1)

    # ヘッダー (小さく)
    header_frame = tk.Frame(frame, bg="#050811")
    header_frame.pack(fill=tk.X, padx=12, pady=(6, 2))

    lbl_title = tk.Label(header_frame, text=title, font=("Segoe UI", 9, "bold"), fg="#00f0ff", bg="#050811")
    lbl_title.pack(side=tk.LEFT)

    lbl_status = tk.Label(header_frame, text="LIVE SYNC", font=("Segoe UI", 8, "bold"), fg="#10b981", bg="#050811")
    lbl_status.pack(side=tk.RIGHT)

    # メインメッセージ
    msg_frame = tk.Frame(frame, bg="#050811")
    msg_frame.pack(fill=tk.X, padx=12, pady=(0, 6))

    lbl_main = tk.Label(msg_frame, text=stage, font=("Segoe UI", 11, "bold"), fg="#f8fafc", bg="#050811")
    lbl_main.pack(anchor="w")

    lbl_detail = tk.Label(msg_frame, text=f"▸ {detail}", font=("Consolas", 8), fg="#94a3b8", bg="#050811")
    lbl_detail.pack(anchor="w")

    # 自動消去
    root.after(duration_ms, root.destroy)
    root.mainloop()

if __name__ == "__main__":
    t = sys.argv[1] if len(sys.argv) > 1 else "⚡ GENESIS 3重防壁オーケストレーション"
    s = sys.argv[2] if len(sys.argv) > 2 else "【第1防壁 ➔ 第2防壁】Antigravity 2.0 ➔ IDE 処理移送"
    d = sys.argv[3] if len(sys.argv) > 3 else "sidepanel.js (LSP監査・現場調整)"
    show_hud(t, s, d)
