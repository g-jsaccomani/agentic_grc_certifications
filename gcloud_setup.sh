#!/usr/bin/env bash
# ==============================================================================
# PROJECT AGENTIC GRC: GCP PROVISIONING & CONFIGURATION SCRIPT
# Automated Auditing and Verification of GRC Compliance (ISO/IEC 27001:2022)
# ==============================================================================

set -euo pipefail

# 1. Project Configuration
PROJECT_ID="${PROJECT_ID:-$(gcloud config get-value project 2>/dev/null || true)}"
REGION="${REGION:-us-central1}"
MODEL_ARMOR_TEMPLATE="${MODEL_ARMOR_TEMPLATE:-g-rc-safety-baseline}"

if [ -z "$PROJECT_ID" ]; then
  echo "[ERROR] GCP Project ID is not set. Please set PROJECT_ID environment variable or run 'gcloud config set project <PROJECT_ID>'."
  exit 1
fi

echo "============================================================"
echo "Initializing Agentic GRC Cloud Platform in Project: ${PROJECT_ID}"
echo "Region: ${REGION}"
echo "============================================================"

# Step 1: Enable Core Google Cloud APIs
echo "[1/4] Enabling required Google Cloud APIs..."
gcloud services enable \
    modelarmor.googleapis.com \
    discoveryengine.googleapis.com \
    run.googleapis.com \
    aiplatform.googleapis.com \
    cloudasset.googleapis.com \
    bigquery.googleapis.com \
    cloudkms.googleapis.com \
    securitycenter.googleapis.com \
    --project="${PROJECT_ID}"

echo "APIs enabled successfully."

# Step 2: Create or Verify Model Armor Safety Template
echo "[2/4] Setting up Model Armor Safety Template (${MODEL_ARMOR_TEMPLATE})..."
if gcloud model-armor templates describe "${MODEL_ARMOR_TEMPLATE}" --location="${REGION}" --project="${PROJECT_ID}" >/dev/null 2>&1; then
    echo "Model Armor template '${MODEL_ARMOR_TEMPLATE}' already exists. Skipping creation."
else
    echo "Creating Model Armor template '${MODEL_ARMOR_TEMPLATE}'..."
    gcloud model-armor templates create "${MODEL_ARMOR_TEMPLATE}" \
        --location="${REGION}" \
        --rai-settings-filters='[{"filterType":"HATE_SPEECH","confidenceLevel":"MEDIUM_AND_ABOVE"}]' \
        --pi-and-jailbreak-filter-settings-enforcement=enabled \
        --pi-and-jailbreak-filter-settings-confidence-level=medium-and-above \
        --malicious-uri-filter-settings-enforcement=enabled \
        --project="${PROJECT_ID}"
    echo "Model Armor template created."
fi

# Step 3: Configure Service Agent Permissions for GEAP & Cloud Run
echo "[3/4] Configuring Service Agent IAM bindings..."
PROJECT_NUMBER=$(gcloud projects describe "${PROJECT_ID}" --format="value(projectNumber)")
echo "GCP Project Number: ${PROJECT_NUMBER}"

# Grant Model Armor usage permissions to Vertex AI service agent (GEAP Engine)
echo "Granting roles/modelarmor.user to Vertex AI service agent..."
gcloud projects add-iam-policy-binding "${PROJECT_ID}" \
    --member="serviceAccount:service-${PROJECT_NUMBER}@gcp-sa-aiplatform.iam.gserviceaccount.com" \
    --role="roles/modelarmor.user" \
    --condition=None || true

# Authorize Discovery Engine Service Agent to invoke secure Cloud Run MCP server
echo "Granting roles/run.invoker to Discovery Engine service agent..."
gcloud projects add-iam-policy-binding "${PROJECT_ID}" \
    --member="serviceAccount:service-${PROJECT_NUMBER}@gcp-sa-discoveryengine.iam.gserviceaccount.com" \
    --role="roles/run.invoker" \
    --condition=None || true

# Step 4: Organization Policy Guidance
echo "[4/4] Organization Constraint Note:"
echo "------------------------------------------------------------"
echo "To allow custom MCP server connectors for Gemini Enterprise:"
echo "Navigate to IAM & Admin > Org Policies in GCP Console:"
echo "1. Search constraint: 'Disable custom mcp server connector for gemini enterprise'"
echo "2. Set enforcement to OFF (Override parent policy)"
echo "------------------------------------------------------------"
echo "Agentic GRC Cloud Platform initialization complete!"
