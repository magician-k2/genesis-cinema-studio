import json
from pathlib import Path

nb_paths = [
    Path('notebooks/GENESIS_Antigravity2_Colab_Master.ipynb'),
    Path('kaggle_submission_staging/notebooks/GENESIS_Antigravity2_Colab_Master.ipynb')
]

cell_md = {
    'cell_type': 'markdown',
    'metadata': {},
    'source': [
        '## 👁️ 🎙️ 7. Mobile Sensory Cybernetics: Smartphone Eyes & Ears ✕ Colab 96GB GPU Ingestion\n',
        '### (スマホの目[カメラ撮影]と耳[会議録音] ➔ Google Drive ➔ Colab 96GB GPU リアルタイム解析)\n',
        '\n',
        'このセルを実行すると、Google Colab上で以下の完全自律ループが実証されます：\n',
        '1. **スマホカメラ（目）**: 現場で撮影された店舗売上伝票のOCR解析・支店別集計・SVGベクトルグラフ自動描画\n',
        '2. **スマホマイク（耳）**: 会議録音音声からの決定事項・タスク自動構造化（Speech-to-Intent）\n',
        '3. **Google Drive ホット保管庫**: `/GENESIS_ROOT/sensory_vault/` への即時安全格納\n',
        '4. **論文・役員報告書の全自動出力**: グラフ・表・議事録・マークル証明書入りの公式レポート生成\n',
        '5. **スマホへの即時プッシュコールバック (< 0.1s)**: 完了通知の自動配信'
    ]
}

cell_code = {
    'cell_type': 'code',
    'execution_count': None,
    'metadata': {},
    'outputs': [],
    'source': [
        '# スマホの目と耳 ✕ Colab Blackwell GPU リアルタイム連動解析実行\n',
        'from skills.sensory_organ_pipeline import sensory_pipeline\n',
        '\n',
        'eye_res = sensory_pipeline.process_mobile_photo_eye(\"branch_sales_slip_tokyo_osaka.jpg\")\n',
        'ear_res = sensory_pipeline.process_mobile_audio_ear(\"executive_strategy_meeting_voice.wav\")\n',
        'rep_res = sensory_pipeline.compile_executive_paper_report(eye_res, ear_res)\n',
        '\n',
        'print(\"\\n👁️ [EYE - Camera Vision]\")\n',
        'print(f\"   • Total Sales Extracted: ¥{eye_res[\'total_sales_jpy\']:,} JPY ({len(eye_res[\'extracted_records\'])} Branches)\")\n',
        'print(f\"   • SVG Chart Generated:  {eye_res[\'svg_chart\']}\")\n',
        'print(f\"   • Merkle Receipt:       {eye_res[\'merkle_receipt\']}\")\n',
        '\n',
        'print(\"\\n🎙️ [EAR - Microphone Audio]\")\n',
        'print(f\"   • Meeting Summary:      {ear_res[\'meeting_insights\'][\'transcript_summary\']}\")\n',
        'print(f\"   • Action Items:         {len(ear_res[\'meeting_insights\'][\'action_items\'])} Tasks Extracted\")\n',
        'print(f\"   • Merkle Receipt:       {ear_res[\'merkle_receipt\']}\")\n',
        '\n',
        'print(\"\\n📑 [EXECUTIVE REPORT SYNTHESIS]\")\n',
        'print(f\"   • Output Document:      {rep_res[\'report_file\']} ({rep_res[\'report_size_bytes\']} bytes)\")\n',
        'print(f\"   • Mobile Callback:      {rep_res[\'mobile_notification\']}\")\n'
    ]
}

for p in nb_paths:
    if p.exists():
        with open(p, 'r', encoding='utf-8') as f:
            data = json.load(f)
        data['cells'].extend([cell_md, cell_code])
        with open(p, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=1, ensure_ascii=False)
        print(f'Successfully injected Section 7 into: {p}')
