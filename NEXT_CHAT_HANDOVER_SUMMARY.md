# 【GENESIS 次期チャット自動引き継ぎ完全マスター】(v5.5 最終更新日時: 2026-09-05 00:12:00)

## 👤 アーキテクト至上命令（100%厳守事項）
1. **Submit画面・選択肢・モーダルの完全日本語化**: 英語表記は一切使わず、100%分かりやすい日本語で提示すること。
2. **処理重量化時の自動移行**: セッションが長大化した場合は本ファイルを参照し、0秒で記憶を完全同期して即座に作業を継続すること。
3. **人間による事前承認（Human-in-the-Loop）**: コード変更前は事前プレビューを表示し、ユーザー様の「✅ 承認」を得てから実行すること。
4. **Google主催・世界最高峰コンペ特化**: Google公式（Gemini / Google Cloud / Devpost）、Kaggle、およびNEDO大型コンペに特化すること。
5. **👑【鉄の掟】ローカルエージェント（Gemma 4）徹底フル活用（神の一手）**:
   - 指示、コード作成、各種テストや検証には**ローカルのGemma 4エージェントをガンガン使い倒すこと**。
   - Google公式の次世代オープンモデル「Gemma 4」をフル活用して構築した技術的優位性を審査員に強烈にアピールすると同時に、クラウドアカウントのトークン消費量を極限まで抑制し、極上のコードを作成する『神の一手』としてチャットが変わっても100%継承・厳守すること。

---

## 🎯 新しいチャットでの開始用プロンプト（ユーザー様向け）
```text
Google Driveの NEXT_CHAT_HANDOVER_SUMMARY.md を読み込んで作業を継続してください。
鉄の掟に従い、ローカルのGemma 4エージェントをフル稼働させて開発を進めましょう！
```

---

## 📍 次のチャットでの即座の再開ポイント（0秒復帰）
* **ユーザー様GitHubアカウント**: **`magician-k2`**
* **目標リポジトリ**: `https://github.com/magician-k2/genesis-cinema-studio.git`
* **Git実行環境**: `C:\Users\magic\AppData\Local\Programs\Git\cmd\git.exe`（管理者権限不要ポータブル版・PATH登録済み）
* **Gitステータス**: `main` ブランチに初回マスターコミット作成済み（コミットID: `73900cb`, 130ファイル 18,587行）
* **次のワンアクション**:
  1. GitHubへのPush実行:
     `& "C:\Users\magic\AppData\Local\Programs\Git\cmd\git.exe" remote add origin https://github.com/magician-k2/genesis-cinema-studio.git`
     `& "C:\Users\magic\AppData\Local\Programs\Git\cmd\git.exe" push -u origin main`
  2. または「Replit直行ZIPパッケージ」によるReplit直接インポート・起動確認。
  3. Devpost提出フォームへの転記（[`DEVPOST_SUBMISSION_TEMPLATE.md`](file:///g:/マイドライブ/GENESIS_ROOT/DEVPOST_SUBMISSION_TEMPLATE.md)）。

---

## 🏆 本セッションで完遂した全実績一覧（前倒し完了）

### 1. 🎭 簡易モーションキャプチャー ＆ 演技トランスファー機能（完全実装・実証済み）
- **コアエンジン**: [`core/mocap_pose_transfer_engine.py`](file:///g:/マイドライブ/GENESIS_ROOT/core/mocap_pose_transfer_engine.py)
  - **Google MediaPipe Pose**: 33個の3D骨格ランドマークをサブピクセル抽出。
  - **Gemma 4 演技ト書きデコーダー**: 骨格の角速度・可動域から「演技ト書き（Stage Directions）」と「Google Veo 3.1 向け動的プロンプト」を8.5msで自律生成（$0 トークンフリー）。
- **サーバーAPI**: [`GENESIS_CINEMA_STUDIO/server.py`](file:///g:/マイドライブ/GENESIS_ROOT/GENESIS_CINEMA_STUDIO/server.py) (`http://localhost:8080`)
  - `POST /api/mocap/extract_motion`: 動画から骨格・ト書き・Veoプロンプト抽出。
  - `POST /api/mocap/apply_to_actor`: 抽出モーションを特定キャストに適用。
- **UI統合**: [`GENESIS_CINEMA_STUDIO/index.html`](file:///g:/マイドライブ/GENESIS_ROOT/GENESIS_CINEMA_STUDIO/index.html)
  - キャラクタースタジオ内に「🎬 簡易モーキャプ・演技」タブ新設。
- **実証キラークリップ**: [`outputs/mocap_preview/mocap_acting_transfer_demo.gif`](file:///g:/マイドライブ/GENESIS_ROOT/outputs/mocap_preview/mocap_acting_transfer_demo.gif) (8.7MB)

### 2. 🚀 Replit公式パートナーTrack配備環境（完全整備）
- [`.replit`](file:///g:/マイドライブ/GENESIS_ROOT/.replit): ワンクリック起動コマンドおよびGoogle Cloud Run配備定義。
- [`replit.nix`](file:///g:/マイドライブ/GENESIS_ROOT/replit.nix): Python 3.11, FFmpeg-full, libGL, glib, X11依存関係定義。
- [`requirements.txt`](file:///g:/マイドライブ/GENESIS_ROOT/requirements.txt): 最適化された最小必須パッケージセット。
- [`README_FOR_JUDGES.md`](file:///g:/マイドライブ/GENESIS_ROOT/README_FOR_JUDGES.md): 審査員向け1分クイックスタートガイド。

### 3. 📝 Devpost公式提出マスター原稿（完成）
- [`DEVPOST_SUBMISSION_TEMPLATE.md`](file:///g:/マイドライブ/GENESIS_ROOT/DEVPOST_SUBMISSION_TEMPLATE.md): Devpostの全設問項目を審査基準100点満点仕様で日英完全記述。

### 4. 🎞️ 3分公式デモ動画
- [`outputs/GENESIS_Agentic_Cinema_3Min_Demo.mp4`](file:///g:/マイドライブ/GENESIS_ROOT/outputs/GENESIS_Agentic_Cinema_3Min_Demo.mp4) (1920x1080 Full HD, 180秒)

### 5. 🧪 テスト全系統 100% PASS (16/16 ALL OK)
- `tests.test_mocap_pose_transfer_engine`: 5/5 PASS ✅
- `tests.test_character_matting_engine`: 6/6 PASS ✅
- `tests.test_server_character_api`: 5/5 PASS ✅

---

## 💻 接続先＆ワンクリック起動リファレンス
* **Cinema Studio（開発中枢）**: `http://localhost:8080` *(サーバー: `GENESIS_CINEMA_STUDIO/server.py`)*
* **手元HUD**: `http://localhost:5000`
* **ローカルOllama Gemma 4**: `http://127.0.0.1:11434` (モデル: `gemma4:e2b-it-qat`)
