#!/usr/bin/env bash
# ==============================================================================
# 🚀 GENESIS Cybernetic Brain OS - Google Cloud Run One-Click Deployment Script
# Target: Google Cloud AI Builder Cup 2026 JAPAC Production Environment
# ==============================================================================
set -euo pipefail

PROJECT_ID=${GOOGLE_CLOUD_PROJECT:-"genesis-cybernetics-prod"}
REGION=${GCP_REGION:-"asia-northeast1"}
SERVICE_NAME="genesis-cognitive-mainframe"
IMAGE_TAG="gcr.io/${PROJECT_ID}/${SERVICE_NAME}:$(git rev-parse --short HEAD 2>/dev/null || echo 'latest')"

echo "========================================================"
echo "🌟 Deploying GENESIS to Google Cloud Run..."
echo "Project: ${PROJECT_ID}"
echo "Region:  ${REGION}"
echo "Image:   ${IMAGE_TAG}"
echo "========================================================"

# 1. Enable required Google Cloud APIs
echo "📡 Enabling GCP APIs (Cloud Run, Vertex AI, Eventarc, Artifact Registry)..."
gcloud services enable \
    run.googleapis.com \
    artifactregistry.googleapis.com \
    aiplatform.googleapis.com \
    eventarc.googleapis.com \
    pubsub.googleapis.com \
    cloudbuild.googleapis.com \
    --project="${PROJECT_ID}"

# 2. Build Container Image via Cloud Build
echo "📦 Submitting build to Google Cloud Build..."
gcloud builds submit --tag "${IMAGE_TAG}" --project="${PROJECT_ID}" -f deploy/gcp/Dockerfile .

# 3. Deploy to Cloud Run with Always-on CPU for 1000Hz CPG
echo "⚡ Deploying to Cloud Run with 1000Hz CPG & 5ms Spinal Reflex Arc..."
gcloud run deploy "${SERVICE_NAME}" \
    --image="${IMAGE_TAG}" \
    --region="${REGION}" \
    --platform=managed \
    --allow-unauthenticated \
    --cpu=2 \
    --memory=4Gi \
    --no-cpu-throttling \
    --min-instances=1 \
    --max-instances=100 \
    --set-env-vars="GOOGLE_CLOUD_PROJECT=${PROJECT_ID},GCP_REGION=${REGION},VERTEX_AI_MODEL=gemini-2.5-flash,CPG_FREQ_HZ=1000" \
    --project="${PROJECT_ID}"

# 4. Fetch Live Service URL
SERVICE_URL=$(gcloud run services describe "${SERVICE_NAME}" --platform=managed --region="${REGION}" --project="${PROJECT_ID}" --format='value(status.url)')

echo "========================================================"
echo "✅ GENESIS Cloud Run deployment complete!"
echo "🚗 Live In-Car Cockpit: ${SERVICE_URL}/cognitive"
echo "💓 Health Endpoint:     ${SERVICE_URL}/health"
echo "========================================================"
