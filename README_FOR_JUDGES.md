# 🎬 GENESIS CINEMA STUDIO: Official Judge Reproduction Guide
> **Agentic Cinema: The Blockbuster Hackathon (Google Cloud & Replit Track)**  
> **Repository**: [https://github.com/genesis-agent/genesis-cinema-studio](https://github.com/genesis-agent/genesis-cinema-studio)  
> **License**: Apache License 2.0  

---

## ⚡ 1-Minute Quick Start on Replit (Zero-Setup)

### Step 1: Open in Replit
Click the **"Run on Replit"** button or import this repository directly into Replit:
1. Fork or import repository into your Replit account.
2. Hit the big green **"Run"** button at the top.
3. Replit automatically resolves `replit.nix` packages and starts the server on port `8080`.

### Step 2: Open Director Web UI
The interactive Virtual Production Studio web interface opens instantly in the Replit Webview:
- **Local / Replit Webview URL**: `http://localhost:8080`

---

## 💻 Local Machine Reproduction Steps

If running locally on Windows / macOS / Linux:

```bash
# 1. Clone the repository
git clone https://github.com/genesis-agent/genesis-cinema-studio.git
cd genesis-cinema-studio

# 2. Install dependencies
pip install -r requirements.txt

# 3. Launch Cinema Studio Server
python GENESIS_CINEMA_STUDIO/server.py

# 4. Open browser at http://localhost:8080
```

---

## 🧪 Key Features Verification Checklist for Judges

| Feature | Where to Test in UI | Expected Result |
| :--- | :--- | :--- |
| **1. 4-View Character Matting & Defringe** | Click `[🎭 キャスト選択]` ➔ `[新キャスト作成]` | Upload 4 photos or sheet ➔ 32-bit transparent PNGs generated with zero white fringe halos. |
| **2. 360° Street View Spatial Summoning** | Select any cast in vault ➔ Toggle `[演者召喚]` | Actor appears seamlessly on Asakusa/Harajuku street with contact drop shadows and ambient ground occlusion. |
| **3. Mocap & Pose-Acting Transfer** | In Character Studio, click `[🎬 簡易モーキャプ・演技]` | Drag & drop sample MP4 ➔ 33-point MediaPipe skeleton extracted ➔ Gemma 4 generates stage directions & Veo prompt in 8.5ms ($0 cost). |
| **4. 3-Minute Master Demo Video** | Run `python build_agentic_cinema_3min_demo.py` | Full 1080p 180-second cinematic master video rendered to `outputs/GENESIS_Agentic_Cinema_3Min_Demo.mp4`. |

---

## 🤖 Architecture Overview: Google Cloud & Edge Gemma 4

```
[ Director Brief / Mocap MP4 ]
            │
            ▼
 ┌────────────────────────────────────────────────────────┐
 │   Google Cloud Gemini 3.8 & Edge Gemma 4 Hybrid Swarm  │
 │   - Gemini 3.8 Pro: Screenplay & Multi-Scene Director │
 │   - Edge Gemma 4: 8.5ms $0-Cost Dialogue & Acting Cues│
 │   - MediaPipe Pose: 33-Point 3D Skeleton Extraction    │
 │   - Telea Inpaint Defringe: Hollywood 32-Bit Vault     │
 └────────────────────────────────────────────────────────┘
            │
            ▼
 ┌────────────────────────────────────────────────────────┐
 │   Replit Collaborative Studio & Video Assembly         │
 │   - 4-Screen NLE Timeline (Director / 4K / Asset / Cue)│
 │   - Google 360° Street View Real-World Summoning       │
 │   - FFmpeg 1080p / 4K Broadcast Master Output          │
 └────────────────────────────────────────────────────────┘
```
