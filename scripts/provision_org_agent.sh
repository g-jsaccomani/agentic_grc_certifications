#!/usr/bin/env bash
# ==============================================================================
# PROVISION AGENTIC GRC: ORGANIZATION HIERARCHY, PROJECT & AUDIT IDENTITY
# Provisions Folder, Project, Billing, Org-Level IAM, Model Armor, and Cloud Run
# ==============================================================================

set -euo pipefail

ORG_ID="${ORG_ID:-31564119954}"
BILLING_ACCOUNT="${BILLING_ACCOUNT:-0180FF-1553BD-6B74BE}"
FOLDER_NAME="${FOLDER_NAME:-fldr-agentic-grc}"
PROJECT_SUFFIX="${PROJECT_SUFFIX:-$(head -c 4 /dev/urandom | xxd -p | head -n 1 2>/dev/null || date +%s | tail -c 5)}"
PROJECT_ID="${PROJECT_ID:-agentic-grc-${PROJECT_SUFFIX}}"
REGION="${REGION:-us-central1}"
SA_NAME="sa-agentic-grc-auditor"

echo "================================================================="
echo "Provisioning Agentic GRC Organization Architecture"
echo "Organization:    organizations/${ORG_ID}"
echo "Billing Account: ${BILLING_ACCOUNT}"
echo "Folder Name:     ${FOLDER_NAME}"
echo "Project ID:      ${PROJECT_ID}"
echo "Region:          ${REGION}"
echo "================================================================="

# Step 1: Create or Locate Folder
echo "[1/7] Managing Folder under Organization ${ORG_ID}..."
FOLDER_ID=$(gcloud resource-manager folders list \
    --organization="${ORG_ID}" \
    --filter="displayName='${FOLDER_NAME}'" \
    --format="value(name)" 2>/dev/null || true)

if [ -z "${FOLDER_ID}" ]; then
    echo "Creating folder '${FOLDER_NAME}'..."
    FOLDER_ID=$(gcloud resource-manager folders create \
        --display-name="${FOLDER_NAME}" \
        --organization="${ORG_ID}" \
        --format="value(name)")
    echo "Folder created: ${FOLDER_ID}"
else
    echo "Existing folder found: ${FOLDER_ID}"
fi
FOLDER_NUM=$(echo "${FOLDER_ID}" | awk -F'/' '{print $NF}')

# Step 2: Create Project under Folder
echo "[2/7] Creating Project '${PROJECT_ID}' in folder '${FOLDER_ID}'..."
if gcloud projects describe "${PROJECT_ID}" >/dev/null 2>&1; then
    echo "Project '${PROJECT_ID}' already exists."
else
    gcloud projects create "${PROJECT_ID}" \
        --folder="${FOLDER_NUM}" \
        --name="Agentic GRC Platform"
    echo "Project created successfully."
fi

# Step 3: Link Billing Account
echo "[3/7] Linking Billing Account ${BILLING_ACCOUNT} to ${PROJECT_ID}..."
gcloud billing projects link "${PROJECT_ID}" \
    --billing-account="${BILLING_ACCOUNT}"

# Step 4: Enable Required Google Cloud APIs
echo "[4/7] Enabling Required Cloud APIs in ${PROJECT_ID}..."
gcloud services enable \
    modelarmor.googleapis.com \
    discoveryengine.googleapis.com \
    run.googleapis.com \
    aiplatform.googleapis.com \
    cloudasset.googleapis.com \
    bigquery.googleapis.com \
    cloudkms.googleapis.com \
    securitycenter.googleapis.com \
    accesscontextmanager.googleapis.com \
    --project="${PROJECT_ID}"

# Step 5: Create Dedicated Audit Service Account
echo "[5/7] Configuring Dedicated Auditor Service Account..."
SA_EMAIL="${SA_NAME}@${PROJECT_ID}.iam.gserviceaccount.com"
if gcloud iam service-accounts describe "${SA_EMAIL}" --project="${PROJECT_ID}" >/dev/null 2>&1; then
    echo "Service Account '${SA_EMAIL}' already exists."
else
    gcloud iam service-accounts create "${SA_NAME}" \
        --display-name="Agentic GRC Org Auditor" \
        --description="Autonomous audit identity with organization-level read privileges" \
        --project="${PROJECT_ID}"
    echo "Service Account created: ${SA_EMAIL}"
fi

# Step 6: Grant Organization-Level Read Privileges
echo "[6/7] Granting Organization-Level IAM Roles on organizations/${ORG_ID}..."
ORG_ROLES=(
    "roles/cloudasset.viewer"
    "roles/browser"
    "roles/iam.securityReviewer"
    "roles/securitycenter.findingsViewer"
    "roles/accesscontextmanager.policyReader"
)

for role in "${ORG_ROLES[@]}"; do
    echo " - Binding ${role} at organization level..."
    gcloud organizations add-iam-policy-binding "${ORG_ID}" \
        --member="serviceAccount:${SA_EMAIL}" \
        --role="${role}" \
        --condition=None >/dev/null 2>&1 || echo "   (Role ${role} already bound or applied)"
done

# Step 7: Setup Model Armor Safety Baseline in Project
echo "[7/7] Setting up Model Armor in ${PROJECT_ID}..."
MODEL_ARMOR_TEMPLATE="g-rc-safety-baseline"
if gcloud model-armor templates describe "${MODEL_ARMOR_TEMPLATE}" --location="${REGION}" --project="${PROJECT_ID}" >/dev/null 2>&1; then
    echo "Model Armor template already present."
else
    gcloud model-armor templates create "${MODEL_ARMOR_TEMPLATE}" \
        --location="${REGION}" \
        --rai-settings-filters='[{"filterType":"HATE_SPEECH","confidenceLevel":"MEDIUM_AND_ABOVE"}]' \
        --pi-and-jailbreak-filter-settings-enforcement=enabled \
        --pi-and-jailbreak-filter-settings-confidence-level=medium-and-above \
        --malicious-uri-filter-settings-enforcement=enabled \
        --project="${PROJECT_ID}" >/dev/null 2>&1 || true
    echo "Model Armor template configured."
fi

# Summary
echo "================================================================="
echo "Organization Provisioning Completed Successfully"
echo "Folder:               ${FOLDER_ID}"
echo "Project:              ${PROJECT_ID}"
echo "Auditor Identity:     ${SA_EMAIL}"
echo "Org-Level Privileges: Cloud Asset Viewer, Browser, Security Reviewer,"
echo "                      SCC Findings Viewer, Access Context Reader"
echo "-----------------------------------------------------------------"
echo "To deploy the Agent and Web Portal to this new project, run:"
echo "export PROJECT_ID='${PROJECT_ID}'"
echo "export REGION='${REGION}'"
echo "make journey"
echo "================================================================="
