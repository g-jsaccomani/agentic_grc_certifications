#!/usr/bin/env bash
# ==============================================================================
# AGENTIC GRC: ONE-CLICK CLIENT BOOTSTRAP SCRIPT
# Designed for complete beginners running inside Google Cloud Shell
# ==============================================================================

set -euo pipefail

BOLD="\033[1m"
GREEN="\033[0;32m"
YELLOW="\033[1;33m"
BLUE="\033[0;34m"
RED="\033[0;31m"
NC="\033[0m"

echo -e "${BOLD}${BLUE}================================================================${NC}"
echo -e "${BOLD}${BLUE}     AGENTIC GRC: AUTOMATED CLIENT FIRST-STEPS PROVISIONING     ${NC}"
echo -e "${BOLD}${BLUE}================================================================${NC}"

# Auto-locate or clone Terraform files (supports direct execution or curl | bash)
if [ ! -f "main.tf" ]; then
    BOOTSTRAP_DIR="${HOME}/.agentic_grc_bootstrap"
    echo -e "\n${YELLOW}Downloading setup files to ${BOOTSTRAP_DIR}...${NC}"
    rm -rf "${BOOTSTRAP_DIR}"
    git clone --depth 1 https://github.com/g-jsaccomani/agentic_grc_certifications.git "${BOOTSTRAP_DIR}" >/dev/null 2>&1
    cd "${BOOTSTRAP_DIR}/terraform/first_steps"
fi

# 1. Verify Prerequisites
echo -e "\n${BOLD}[1/5] Checking Google Cloud Shell Environment...${NC}"

CURRENT_ACCOUNT=$(gcloud config get-value account 2>/dev/null || true)
if [ -z "${CURRENT_ACCOUNT}" ]; then
    echo -e "${YELLOW}Not logged in. Running gcloud auth login...${NC}"
    gcloud auth login --quiet
    CURRENT_ACCOUNT=$(gcloud config get-value account)
fi
echo -e "Authenticated as: ${BOLD}${GREEN}${CURRENT_ACCOUNT}${NC}"

if ! command -v terraform >/dev/null 2>&1; then
    echo -e "${RED}Error: terraform is not installed. Please run this inside Google Cloud Shell where Terraform is pre-installed.${NC}"
    exit 1
fi
echo -e "Terraform version: $(terraform -version | head -n 1)"

# 2. Detect or Confirm Organization ID
echo -e "\n${BOLD}[2/5] Identifying GCP Organization...${NC}"
DEFAULT_ORG="31564119954"
DETECTED_ORG=$(gcloud organizations list --format="value(name)" 2>/dev/null | head -n 1 | awk -F'/' '{print $NF}' || true)

if [ -n "${DETECTED_ORG}" ]; then
    TARGET_ORG="${DETECTED_ORG}"
    echo -e "Detected Organization ID: ${BOLD}${GREEN}${TARGET_ORG}${NC}"
else
    TARGET_ORG="${DEFAULT_ORG}"
    echo -e "Using Default Organization ID: ${BOLD}${TARGET_ORG}${NC}"
fi

# 3. Detect or Confirm Billing Account
echo -e "\n${BOLD}[3/5] Identifying Billing Account...${NC}"
DEFAULT_BILLING="0180FF-1553BD-6B74BE"
DETECTED_BILLING=$(gcloud billing accounts list --filter="open=true" --format="value(name)" 2>/dev/null | head -n 1 | awk -F'/' '{print $NF}' || true)

if [ -n "${DETECTED_BILLING}" ]; then
    TARGET_BILLING="${DETECTED_BILLING}"
    echo -e "Detected Open Billing Account: ${BOLD}${GREEN}${TARGET_BILLING}${NC}"
else
    TARGET_BILLING="${DEFAULT_BILLING}"
    echo -e "Using Default Billing Account: ${BOLD}${TARGET_BILLING}${NC}"
fi

DEPLOYER_EMAIL="jsaccomani@google.com"

# 4. Generate terraform.tfvars automatically
echo -e "\n${BOLD}[4/5] Generating Configuration File (terraform.tfvars)...${NC}"
cat <<EOF > terraform.tfvars
org_id          = "${TARGET_ORG}"
billing_account = "${TARGET_BILLING}"
folder_name     = "fldr-agentic-grc"
project_prefix  = "agentic-grc"
region          = "us-central1"
deployer_email  = "${DEPLOYER_EMAIL}"
EOF
echo -e "${GREEN}Configuration file generated successfully.${NC}"

# 5. Execute Terraform
echo -e "\n${BOLD}[5/5] Provisioning Folder, Project, APIs, and IAM Roles...${NC}"
echo -e "Running 'terraform init'..."
terraform init -input=false

echo -e "\nApplying infrastructure changes automatically..."
terraform apply -auto-approve -input=false

# 6. Extract Outputs and Display in Large, Plain Text
PROJECT_ID=$(terraform output -raw project_id 2>/dev/null || true)
FOLDER_ID=$(terraform output -raw folder_id 2>/dev/null || true)
AUDITOR_SA=$(terraform output -raw auditor_service_account_email 2>/dev/null || true)

echo -e "\n${BOLD}${GREEN}================================================================${NC}"
echo -e "${BOLD}${GREEN}              FIRST STEPS PROVISIONING COMPLETED!               ${NC}"
echo -e "${BOLD}${GREEN}================================================================${NC}"
echo -e "\n${BOLD}Please copy the line below and send it to the implementation engineer:${NC}"
echo -e "\n----------------------------------------------------------------"
echo -e "PROJECT_ID: ${BOLD}${BLUE}${PROJECT_ID}${NC}"
echo -e "FOLDER_ID:  ${FOLDER_ID}"
echo -e "AUDITOR_SA: ${AUDITOR_SA}"
echo -e "----------------------------------------------------------------\n"
echo -e "No further action is required from you. The engineer will now handle the deployment.\n"
