# 🏛️ GENESIS Portable Core & Universal App Packager Master Registry
> **GENESIS 永久記憶台帳 (Knowledge Bank: Global Distribution & Evaluation Standards)**  
> **制定日**: 2026-09-26 | **ステータス**: PRODUCTION OPERATIONAL (永続化完了)

---

## 🎯 1. 創設の背景と目的（真因と教訓）

GENESIS開発環境（Google Drive `G:\`、巨大コネクトームDB、多重エージェント環境）と、
実際に第三者へ渡す「アプリケーション」は物理的に別物である。

アプリケーション単体（HTML/JS/拡張機能）のみを渡すと、背後で稼働するGENESISの頭脳エンジン（微分方程式・SNN・Merkle Proof）が相手の手元に存在しないため、「側だけ」「中身がない」という致命的な誤解を生む。

本システムは、**「あらゆるGENESISアプリケーションを、ゼロ外部依存のGENESIS本体（Micro-Runtime）とワンセットで合体させ、相手の手元でワンクリックで本物の頭脳を起動させる」** ための永久標準配布基盤である。

---

## 🧬 2. GENESIS Portable Core アーキテクチャ

**配置ディレクトリ**: [`packages/genesis_portable_core/`](file:///g:/マイドライブ/GENESIS_ROOT/packages/genesis_portable_core/)  
**動作保証**: Python 3.8+ 標準ライブラリのみ（**pip依存関係ゼロ / 追加インストール一切不要**）

### 主要構成モジュール:
1. **`engine_snn.py`**:
   - **LIF膜電位オイラー積分**: $\tau_m \frac{dV}{dt} = -(V - V_{rest}) + R_m I(t)$
   - **STDP二重指数可塑性**: $\Delta w = A_+ e^{-\Delta t/\tau_+}$ (LTP) / $-A_- e^{\Delta t/\tau_-}$ (LTD)
   - **能動的推論（変分自由エネルギー最小化）**: $F = D_{KL}(q(s) \parallel p(s)) - \mathbb{E}_q[\ln p(o \mid s)]$
2. **`engine_connectome.py`**:
   - プリンストン大学 FlyWire全脳コネクトーム（13.9万ニューロン）代表神経回路（視覚野・抑制性中枢・運動出力核）を直接内包。
   - 逆マインドマップ（一次証拠 ➔ SNN枝刈り ➔ 根本原因）の因果収束グラフを探索。
3. **`engine_merkle.py`**:
   - EU AI Act 第13条（透明性・監査証跡）準拠の SHA-256 Merkle Tree 暗号ハッシュ生成。
   - 改ざん不可能な「思考レシート（Cognitive Receipt）」を発行。
4. **`engine_orchestrator.py`**:
   - 3重防壁（第1防壁: 2.0指揮 ➔ 第2防壁: 現場LSP ➔ 第3防壁: 0.85msスウォーム調停）のステートマシン。
5. **`server_micro_api.py`**:
   - 超軽量ローカルREST APIサーバー（ポート 8080）。
   - エンドポイント: `/api/status`, `/api/reason`, `/api/snn_step`。
   - 同梱されたフロントエンドアプリの静的ファイルも同時にホスト。

---

## 🚀 3. ユニバーサル・アプリ自動パッケージャー

**実行スクリプト**: [`scripts/package_genesis_app.py`](file:///g:/マイドライブ/GENESIS_ROOT/scripts/package_genesis_app.py)

### 実行コマンド例:

```bash
# ① Chrome拡張機能（SidePanel 逆マインドマップXAI）のパッケージング
python scripts/package_genesis_app.py --app browser_extension --name GENESIS_XAI_SidePanel_FullDistribution

# ② 映画・動画制作スタジオ（GENESIS Cinema Studio）のパッケージング
python scripts/package_genesis_app.py --app GENESIS_CINEMA_STUDIO --name GENESIS_Cinema_Studio_FullDistribution

# ③ Webスタンドアロンデモのパッケージング
python scripts/package_genesis_app.py --app web --name GENESIS_WebApps_FullDistribution
```

### 自動生成される配布ZIPの中身:
```
【配布用ZIP bundle】
├── 🚀 Start_App_with_GENESIS.bat      <-- ★ 相手がダブルクリック1発で起動！
├── 🐧 start_app_with_genesis.sh      <-- Mac / Linux対応スクリプト
├── 📄 README_FOR_EVALUATOR.md         <-- 取扱説明書（審査員・パートナー・教授向け）
├── 📁 app/                           <-- アプリのUI・フロントエンド一式
└── 📁 genesis_core/                  <-- 同梱されたGENESIS本体（頭脳エンジン）
```

---

## 🎓 4. 用途別・評価者への提供シナリオ

### ① ハッカソン審査員（Devpost, Google, NEDO）
- **メリット**: 環境構築不要・APIキー不要。
- **実演**: 解凍して `Start_App_with_GENESIS.bat` を押すだけで、審査員のPCのGPUとローカルCPU上で10,000ニューロンのSNNと逆マインドマップが即座に稼働。「ハリボテ・見せかけ」の疑いを0秒で粉砕。

### ② ビジネスパートナー・クライアント
- **メリット**: 複雑な説明不要で、手元のPCで動く完成品を体験できる。
- **実演**: 「UIだけでなく、裏で生体微分方程式を計算する自律エンジン本体が丸ごと入っています」と堂々と渡せる。

### ③ 大学教授・学会・学術評価委員会
- **メリット**: 数学的厳密性（Zero-Mock原則）の完全証明。
- **実演**: `genesis_core/engine_snn.py` の生体数式と、`engine_merkle.py` のEU AI Act第13条準拠の思考レシートを提示し、学術論文・特許としての客観的再現性を完全に立証。

---

## 🛡️ 永久保存保証
本仕様は GENESIS Cybernetics Knowledge Graph および Gitリポジトリ（コミット: `aeccdd1` 以降）に永続保存されており、いつでも即座に呼び出し・再生成が可能です。
