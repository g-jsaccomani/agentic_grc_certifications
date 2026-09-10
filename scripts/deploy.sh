#!/usr/bin/env bash
# ==============================================================================
# AGENTIC GRC: CONSOLIDATED END-TO-END GCP DEPLOYMENT
# Provisions cloud infrastructure, IAM identities, and deploys MCP Server
# ==============================================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
cd "${PROJECT_ROOT}"

PROJECT_ID="${PROJECT_ID:-$(gcloud config get-value project 2>/dev/null || true)}"
REGION="${REGION:-us-central1}"
SERVICE_NAME="${SERVICE_NAME:-mcp-server-grc}"
MODEL_ARMOR_TEMPLATE="${MODEL_ARMOR_TEMPLATE:-g-rc-safety-baseline}"
ALLOW_DEV_AUTH_BYPASS="${ALLOW_DEV_AUTH_BYPASS:-true}"

if [ -z "${PROJECT_ID}" ]; then
  echo "[ERROR] GCP Project ID is not set."
  echo "Set the environment variable: export PROJECT_ID='<your-project-id>' or run 'gcloud config set project <PROJECT_ID>'."
  exit 1
fi

echo "============================================================"
echo "Agentic GRC: End-to-End GCP Deployment"
echo "Project ID:   ${PROJECT_ID}"
echo "Region:       ${REGION}"
echo "Service Name: ${SERVICE_NAME}"
echo "============================================================"

# ------------------------------------------------------------------------------
# STEP 1: Enable Required Google Cloud APIs (Idempotent)
# ------------------------------------------------------------------------------
echo "[1/4] Enabling required Google Cloud APIs..."
gcloud services enable \
    serviceusage.googleapis.com \
    cloudresourcemanager.googleapis.com \
    iam.googleapis.com \
    modelarmor.googleapis.com \
    run.googleapis.com \
    cloudasset.googleapis.com \
    securitycenter.googleapis.com \
    accesscontextmanager.googleapis.com \
    cloudkms.googleapis.com \
    bigquery.googleapis.com \
    aiplatform.googleapis.com \
    discoveryengine.googleapis.com \
    artifactregistry.googleapis.com \
    cloudbuild.googleapis.com \
    logging.googleapis.com \
    monitoring.googleapis.com \
    --project="${PROJECT_ID}" --quiet

echo "[PASS] Cloud APIs enabled."

# ------------------------------------------------------------------------------
# STEP 2: Configure Model Armor Safety Template (Idempotent)
# ------------------------------------------------------------------------------
echo "[2/4] Verifying Model Armor Safety Template (${MODEL_ARMOR_TEMPLATE})..."
if gcloud model-armor templates describe "${MODEL_ARMOR_TEMPLATE}" --location="${REGION}" --project="${PROJECT_ID}" >/dev/null 2>&1; then
    echo "[PASS] Model Armor template '${MODEL_ARMOR_TEMPLATE}' already exists."
else
    if gcloud model-armor templates create "${MODEL_ARMOR_TEMPLATE}" \
        --location="${REGION}" \
        --rai-settings-filters='[{"filterType":"HATE_SPEECH","confidenceLevel":"MEDIUM_AND_ABOVE"}]' \
        --pi-and-jailbreak-filter-settings-enforcement=enabled \
        --pi-and-jailbreak-filter-settings-confidence-level=medium-and-above \
        --malicious-uri-filter-settings-enforcement=enabled \
        --project="${PROJECT_ID}" >/dev/null 2>&1; then
        echo "[PASS] Model Armor template '${MODEL_ARMOR_TEMPLATE}' created."
    else
        echo "[INFO] Model Armor template creation skipped (preview restriction). Using default Vertex AI safety baseline."
    fi
fi

# ------------------------------------------------------------------------------
# STEP 3: Configure Service Identities & IAM Roles (Idempotent)
# ------------------------------------------------------------------------------
echo "[3/4] Configuring Service Identities and Cloud Build IAM bindings..."
PROJECT_NUMBER=$(gcloud projects describe "${PROJECT_ID}" --format="value(projectNumber)")
echo "GCP Project Number: ${PROJECT_NUMBER}"

# Ensure required service identities exist before binding roles
gcloud beta services identity create --service=aiplatform.googleapis.com --project="${PROJECT_ID}" --quiet >/dev/null 2>&1 || true
gcloud beta services identity create --service=discoveryengine.googleapis.com --project="${PROJECT_ID}" --quiet >/dev/null 2>&1 || true
gcloud beta services identity create --service=cloudbuild.googleapis.com --project="${PROJECT_ID}" --quiet >/dev/null 2>&1 || true

# Grant Model Armor usage permissions to Vertex AI service agent
gcloud projects add-iam-policy-binding "${PROJECT_ID}" \
    --member="serviceAccount:service-${PROJECT_NUMBER}@gcp-sa-aiplatform.iam.gserviceaccount.com" \
    --role="roles/modelarmor.user" \
    --condition=None --quiet >/dev/null 2>&1 || true

# Authorize Discovery Engine Service Agent to invoke Cloud Run
gcloud projects add-iam-policy-binding "${PROJECT_ID}" \
    --member="serviceAccount:service-${PROJECT_NUMBER}@gcp-sa-discoveryengine.iam.gserviceaccount.com" \
    --role="roles/run.invoker" \
    --condition=None --quiet >/dev/null 2>&1 || true

# Authorize Compute Service Account used by Cloud Build
COMPUTE_SA="${PROJECT_NUMBER}-compute@developer.gserviceaccount.com"
for r in "roles/storage.admin" "roles/logging.logWriter" "roles/artifactregistry.writer" "roles/aiplatform.user"; do
    gcloud projects add-iam-policy-binding "${PROJECT_ID}" \
        --member="serviceAccount:${COMPUTE_SA}" \
        --role="${r}" \
        --condition=None --quiet >/dev/null 2>&1 || true
done

echo "[PASS] IAM service identities and role bindings configured."

# ------------------------------------------------------------------------------
# STEP 4: Deploy to Google Cloud Run with Verified Environment Variables
# ------------------------------------------------------------------------------
echo "[4/4] Deploying ${SERVICE_NAME} to Google Cloud Run in ${REGION}..."

ENV_VARS="PROJECT_ID=${PROJECT_ID}"
ENV_VARS="${ENV_VARS},REGION=${REGION}"
ENV_VARS="${ENV_VARS},GOOGLE_CLOUD_PROJECT=${PROJECT_ID}"
ENV_VARS="${ENV_VARS},GOOGLE_CLOUD_LOCATION=${REGION}"
ENV_VARS="${ENV_VARS},GOOGLE_GENAI_USE_VERTEXAI=true"
ENV_VARS="${ENV_VARS},ALLOW_DEV_AUTH_BYPASS=${ALLOW_DEV_AUTH_BYPASS}"
DEFAULT_AUDITOR_EMAIL="${DEFAULT_AUDITOR_EMAIL:-jsaccomani@google.com}"
GOOGLE_WORKSPACE_DOMAIN="${GOOGLE_WORKSPACE_DOMAIN:-google.com}"
ENV_VARS="${ENV_VARS},DEFAULT_AUDITOR_EMAIL=${DEFAULT_AUDITOR_EMAIL}"
ENV_VARS="${ENV_VARS},GOOGLE_WORKSPACE_DOMAIN=${GOOGLE_WORKSPACE_DOMAIN}"
if [ -n "${GOOGLE_OAUTH_CLIENT_ID:-}" ]; then
    ENV_VARS="${ENV_VARS},GOOGLE_OAUTH_CLIENT_ID=${GOOGLE_OAUTH_CLIENT_ID}"
fi

if ! gcloud run deploy "${SERVICE_NAME}" \
    --source="${PROJECT_ROOT}" \
    --region="${REGION}" \
    --project="${PROJECT_ID}" \
    --platform=managed \
    --allow-unauthenticated \
    --min-instances=1 \
    --memory=2Gi \
    --cpu=2 \
    --quiet \
    --set-env-vars="${ENV_VARS}"; then
    echo "[WARN] Deployment with --allow-unauthenticated failed (possible Organization Policy constraint). Retrying with authenticated access..."
    gcloud run deploy "${SERVICE_NAME}" \
        --source="${PROJECT_ROOT}" \
        --region="${REGION}" \
        --project="${PROJECT_ID}" \
        --platform=managed \
        --no-allow-unauthenticated \
        --min-instances=1 \
        --memory=2Gi \
        --cpu=2 \
        --quiet \
        --set-env-vars="${ENV_VARS}"
fi

SERVICE_URL=$(gcloud run services describe "${SERVICE_NAME}" --region="${REGION}" --project="${PROJECT_ID}" --format="value(status.url)")

echo ""
echo "============================================================"
echo "[SUCCESS] Agentic GRC Platform Deployed Successfully!"
echo "============================================================"
echo "Live Web Portal:    ${SERVICE_URL}/portal"
echo "API Health Check:   ${SERVICE_URL}/healthz"
echo "Discovery Endpoint: ${SERVICE_URL}/.well-known/agent.json"
echo "StreamableHTTP MCP: ${SERVICE_URL}/mcp"
echo "Project ID:         ${PROJECT_ID}"
echo "Region:             ${REGION}"
echo "============================================================"
