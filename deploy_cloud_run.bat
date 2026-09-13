@echo off
chcp 65001 > nul
cls
echo ===============================================================================
echo  ☁️ 🚀 GENESIS Google Cloud Run 自動デプロイメントシステム (Production Deploy)
echo  対象: Build with Gemini Challenge ＆ NEDO GENIAC 審査用常駐インスタンス
echo ===============================================================================
echo.

set SERVICE_NAME=genesis-cognitive-cortex
set REGION=asia-northeast1
set MEMORY=2Gi
set CPU=2
set MIN_INSTANCES=0
set MAX_INSTANCES=5

echo [1/4] Google Cloud SDK (gcloud) 認証状態を確認中...
where gcloud >nul 2>nul
if %errorlevel% neq 0 (
    echo.
    echo ❌ [ERROR] gcloud CLI がインストールされていないか PATH に通っていません。
    echo Google Cloud SDK をインストールして 'gcloud auth login' を実行してください。
    echo https://cloud.google.com/sdk/docs/install
    echo.
    pause
    exit /b 1
)

echo ✅ gcloud CLI を検出しました。
echo.

echo [2/4] デプロイ対象プロジェクトを確認中...
call gcloud config get-value project
echo.

echo [3/4] Google Cloud Run へのソースコードアップロード＆ビルドデプロイを開始します...
echo   - サービス名: %SERVICE_NAME%
echo   - リージョン: %REGION%
echo   - メモリ: %MEMORY% / CPU: %CPU%
echo   - 最小インスタンス: %MIN_INSTANCES% (常時ウォーム待機・0.3s即時応答)
echo.

call gcloud run deploy %SERVICE_NAME% ^
    --source . ^
    --platform managed ^
    --region %REGION% ^
    --allow-unauthenticated ^
    --memory %MEMORY% ^
    --cpu %CPU% ^
    --min-instances %MIN_INSTANCES% ^
    --max-instances %MAX_INSTANCES% ^
    --set-env-vars PYTHONUNBUFFERED=1,GEMINI_API_KEY=%GEMINI_API_KEY%

if %errorlevel% neq 0 (
    echo.
    echo ⚠️ デプロイ中にエラーが発生しました。ログを確認してください。
    pause
    exit /b %errorlevel%
)

echo.
echo ===============================================================================
echo  🎉 [DEPLOY SUCCESS] Google Cloud Run への実デプロイが完了しました！
echo ===============================================================================
echo.
echo 公開HTTPS URLを取得中...
for /f "tokens=*" %%i in ('gcloud run services describe %SERVICE_NAME% --platform managed --region %REGION% --format="value(status.url)"') do set SERVICE_URL=%%i

echo 🌐 審査用公開常駐URL: %SERVICE_URL%
echo.
echo このURLをコンテスト提出書類 (PROPOSAL_BUILD_WITH_GEMINI_MASTER.md) に記載して提出可能です。
echo.
pause
