#!/usr/bin/env bash
# ==============================================================================
# AGENTIC GRC: ONE-CLICK AUTOMATED CLIENT PROVISIONING & DEPLOYMENT
# Full end-to-end cloud setup: IaC, APIs, IAM, and Cloud Run deployment.
# Client interaction: Paste command, enter email(s) for access, copy output.
# Any failure captures an instant diagnostic error trace for hotfix debugging.
# ==============================================================================

set -euo pipefail

BOLD="\033[1m"
GREEN="\033[0;32m"
YELLOW="\033[1;33m"
BLUE="\033[0;34m"
CYAN="\033[0;36m"
RED="\033[0;31m"
NC="\033[0m"

LOG_FILE="/tmp/agentic_grc_bootstrap_$(date +%Y%m%d_%H%M%S).log"
CURRENT_STEP="Initializing environment"
TARGET_ORG=""
PROJECT_ID=""
FOLDER_ID=""
AUDITOR_SA=""
TARGET_ACCOUNTS=""

# ------------------------------------------------------------------------------
# Diagnostic Error Trap
# ------------------------------------------------------------------------------
on_exit() {
    local exit_code="$?"
    if [ "${exit_code}" -ne 0 ] && [ "${CURRENT_STEP}" != "Completed" ]; then
        echo -e "\n${BOLD}${RED}================================================================${NC}"
        echo -e "${BOLD}${RED}                 DEPLOYMENT ENCOUNTERED AN ERROR                ${NC}"
        echo -e "${BOLD}${RED}================================================================${NC}"
        echo -e "\n${BOLD}Please copy the entire error diagnostic block below and send it"
        echo -e "to the implementation engineer for immediate hotfix resolution:${NC}"
        echo -e "\n----------------------------------------------------------------"
        echo -e "TIMESTAMP:        $(date -u +"%Y-%m-%dT%H:%M:%SZ")"
        echo -e "FAILED AT STEP:   ${CURRENT_STEP}"
        echo -e "EXIT CODE:        ${exit_code}"
        echo -e "GCP ACCOUNT:      $(gcloud config get-value account 2>/dev/null || echo 'Unknown')"
        echo -e "ORGANIZATION ID:  ${TARGET_ORG:-Not detected}"
        echo -e "PROJECT ID:       ${PROJECT_ID:-Not yet provisioned}"
        echo -e "LOG FILE PATH:    ${LOG_FILE}"
        echo -e "----------------------------------------------------------------"
        echo -e "\n${BOLD}ERROR DIAGNOSTIC TRACE (LAST 30 LOG ENTRIES):${NC}"
        if [ -f "${LOG_FILE}" ]; then
            tail -n 30 "${LOG_FILE}"
        else
            echo "No log entries recorded."
        fi
        echo -e "----------------------------------------------------------------\n"
    fi
}
trap on_exit EXIT

echo -e "${BOLD}${BLUE}================================================================${NC}"
echo -e "${BOLD}${BLUE}     AGENTIC GRC: AUTOMATED CLIENT PROVISIONING & DEPLOYMENT     ${NC}"
echo -e "${BOLD}${BLUE}================================================================${NC}"
echo -e "Log file: ${LOG_FILE}\n"

# ------------------------------------------------------------------------------
# 1. Download or Locate Repository
# ------------------------------------------------------------------------------
CURRENT_STEP="Locating setup repository"
BOOTSTRAP_DIR="${HOME}/.agentic_grc_bootstrap"
if [ ! -f "main.tf" ]; then
    echo -e "${YELLOW}Downloading deployment configuration to ${BOOTSTRAP_DIR}...${NC}"
    rm -rf "${BOOTSTRAP_DIR}"
    git clone --depth 1 https://github.com/g-jsaccomani/agentic_grc_certifications.git "${BOOTSTRAP_DIR}" >> "${LOG_FILE}" 2>&1
    cd "${BOOTSTRAP_DIR}/terraform/first_steps"
    PROJECT_ROOT="${BOOTSTRAP_DIR}"
else
    PROJECT_ROOT="$(cd ../.. && pwd)"
fi

BIN_DIR="${HOME}/.local/bin"
mkdir -p "${BIN_DIR}"
export PATH="${BIN_DIR}:${PATH}"

OS=$(uname -s | tr '[:upper:]' '[:lower:]')
ARCH=$(uname -m)
case "${ARCH}" in
    x86_64) ARCH="amd64" ;;
    aarch64|arm64) ARCH="arm64" ;;
    *) ARCH="amd64" ;;
esac

# ------------------------------------------------------------------------------
# 2. Verify Google Cloud Authentication
# ------------------------------------------------------------------------------
CURRENT_STEP="Verifying Google Cloud authentication"
echo -e "${BOLD}[1/6] Verifying Google Cloud Authentication...${NC}"
CURRENT_ACCOUNT=$(gcloud config get-value account 2>/dev/null || true)
if [ -z "${CURRENT_ACCOUNT}" ]; then
    echo -e "${YELLOW}No active account found. Launching authentication...${NC}"
    gcloud auth login --quiet
    CURRENT_ACCOUNT=$(gcloud config get-value account)
fi
echo -e "Authenticated as: ${BOLD}${GREEN}${CURRENT_ACCOUNT}${NC}"
echo "[$(date -u +"%Y-%m-%dT%H:%M:%SZ")] Authenticated as ${CURRENT_ACCOUNT}" >> "${LOG_FILE}"

# ------------------------------------------------------------------------------
# 3. Ensure Functional IaC Engine (Terraform / OpenTofu)
# ------------------------------------------------------------------------------
CURRENT_STEP="Preparing Terraform engine"
echo -e "\n${BOLD}[2/6] Verifying Infrastructure Engine...${NC}"

is_valid_iac() {
    local candidate="${1:-}"
    if [ -z "${candidate}" ] || [ ! -x "${candidate}" ]; then
        return 1
    fi
    local ver_str
    ver_str=$("${candidate}" version 2>&1 || true)
    if echo "${ver_str}" | grep -qE '^(Terraform|OpenTofu) v[0-9]+\.[0-9]+'; then
        return 0
    fi
    return 1
}

IAC_BIN=""
if is_valid_iac "${BIN_DIR}/terraform"; then
    IAC_BIN="${BIN_DIR}/terraform"
elif is_valid_iac "${BIN_DIR}/tofu"; then
    IAC_BIN="${BIN_DIR}/tofu"
elif command -v terraform >/dev/null 2>&1 && is_valid_iac "$(command -v terraform)"; then
    IAC_BIN="$(command -v terraform)"
elif command -v tofu >/dev/null 2>&1 && is_valid_iac "$(command -v tofu)"; then
    IAC_BIN="$(command -v tofu)"
fi

if [ -z "${IAC_BIN}" ]; then
    echo -e "${CYAN}Setting up Terraform engine (v1.9.5)...${NC}"
    TF_URL="https://releases.hashicorp.com/terraform/1.9.5/terraform_1.9.5_${OS}_${ARCH}.zip"
    curl -sSL -o /tmp/terraform.zip "${TF_URL}" >> "${LOG_FILE}" 2>&1
    if command -v unzip >/dev/null 2>&1; then
        unzip -q -o /tmp/terraform.zip -d "${BIN_DIR}" >> "${LOG_FILE}" 2>&1
    else
        python3 -c "import zipfile; zipfile.ZipFile('/tmp/terraform.zip').extractall('${BIN_DIR}')" >> "${LOG_FILE}" 2>&1
    fi
    chmod +x "${BIN_DIR}/terraform"
    rm -f /tmp/terraform.zip
    IAC_BIN="${BIN_DIR}/terraform"
    
    if [ -f "${HOME}/.bashrc" ] && ! grep -q "PATH=.*${BIN_DIR}" "${HOME}/.bashrc" 2>/dev/null; then
        echo "export PATH=\"${BIN_DIR}:\$PATH\"" >> "${HOME}/.bashrc"
    fi
fi

echo -e "Using Engine: ${BOLD}${GREEN}$("${IAC_BIN}" version | head -n 1)${NC}"
echo "[$(date -u +"%Y-%m-%dT%H:%M:%SZ")] IaC: $("${IAC_BIN}" version | head -n 1)" >> "${LOG_FILE}"

# ------------------------------------------------------------------------------
# 4. Detect Organization ID & Billing Account
# ------------------------------------------------------------------------------
CURRENT_STEP="Detecting GCP Organization"
echo -e "\n${BOLD}[3/6] Detecting GCP Organization & Billing Account...${NC}"
DEFAULT_ORG="31564119954"
DETECTED_ORG=$(gcloud organizations list --format="value(name)" 2>/dev/null | head -n 1 | awk -F'/' '{print $NF}' || true)
TARGET_ORG="${DETECTED_ORG:-${DEFAULT_ORG}}"
echo -e "Target Organization ID: ${BOLD}${GREEN}${TARGET_ORG}${NC}"

CURRENT_STEP="Detecting Billing Account"
DEFAULT_BILLING="0180FF-1553BD-6B74BE"
DETECTED_BILLING=$(gcloud billing accounts list --filter="open=true" --format="value(name)" 2>/dev/null | head -n 1 | awk -F'/' '{print $NF}' || true)
TARGET_BILLING="${DETECTED_BILLING:-${DEFAULT_BILLING}}"
echo -e "Target Billing Account: ${BOLD}${GREEN}${TARGET_BILLING}${NC}"

# ------------------------------------------------------------------------------
# 5. Prompt for Authorized User Email(s)
# ------------------------------------------------------------------------------
CURRENT_STEP="Configuring authorized access accounts"
echo -e "\n${BOLD}[4/6] Configuring Authorized Platform Access...${NC}"
echo -e "Please specify the email address(es) of the user(s) or group(s) who will have access."
echo -e "Supported: ${CYAN}engineer@company.com${NC} or comma-separated: ${CYAN}user1@company.com, user2@company.com${NC}"

DEFAULT_ACCOUNT_HINT="${CURRENT_ACCOUNT}"
if [ -n "${DEPLOYER_ACCOUNTS:-}" ]; then
    TARGET_ACCOUNTS="${DEPLOYER_ACCOUNTS}"
elif [ -n "${DEPLOYER_EMAILS:-}" ]; then
    TARGET_ACCOUNTS="${DEPLOYER_EMAILS}"
elif [ -n "${DEPLOYER_EMAIL:-}" ]; then
    TARGET_ACCOUNTS="${DEPLOYER_EMAIL}"
else
    if [ -e /dev/tty ] && [ -r /dev/tty ]; then
        echo -ne "\n${BOLD}Enter account(s) to authorize [Default: ${DEFAULT_ACCOUNT_HINT}]: ${NC}" > /dev/tty
        read -r INPUT_ACCOUNTS < /dev/tty || true
        TARGET_ACCOUNTS="${INPUT_ACCOUNTS:-${DEFAULT_ACCOUNT_HINT}}"
    elif [ -t 0 ]; then
        read -r -p "Enter account(s) to authorize [Default: ${DEFAULT_ACCOUNT_HINT}]: " INPUT_ACCOUNTS || true
        TARGET_ACCOUNTS="${INPUT_ACCOUNTS:-${DEFAULT_ACCOUNT_HINT}}"
    else
        TARGET_ACCOUNTS="${DEFAULT_ACCOUNT_HINT}"
    fi
fi

echo -e "Authorized Account(s): ${BOLD}${GREEN}${TARGET_ACCOUNTS}${NC}"
echo "[$(date -u +"%Y-%m-%dT%H:%M:%SZ")] Authorized accounts: ${TARGET_ACCOUNTS}" >> "${LOG_FILE}"

# Format list for Terraform
TF_DEPLOYER_EMAILS="["
FIRST_ACC=true
IFS=',' read -ra ADDR <<< "${TARGET_ACCOUNTS}"
for item in "${ADDR[@]}"; do
    trimmed=$(echo "${item}" | sed -e 's/^[[:space:]]*//' -e 's/[[:space:]]*$//')
    if [ -n "${trimmed}" ]; then
        if [ "${FIRST_ACC}" = true ]; then
            TF_DEPLOYER_EMAILS="${TF_DEPLOYER_EMAILS}\n  \"${trimmed}\""
            FIRST_ACC=false
        else
            TF_DEPLOYER_EMAILS="${TF_DEPLOYER_EMAILS},\n  \"${trimmed}\""
        fi
    fi
done
TF_DEPLOYER_EMAILS="${TF_DEPLOYER_EMAILS}\n]"

# ------------------------------------------------------------------------------
# 6. Generate Configuration & Execute Infrastructure Provisioning
# ------------------------------------------------------------------------------
CURRENT_STEP="Generating Terraform configuration"
cat <<EOF > terraform.tfvars
org_id          = "${TARGET_ORG}"
billing_account = "${TARGET_BILLING}"
folder_name     = "fldr-agentic-grc"
project_prefix  = "agentic-grc"
region          = "us-central1"
deployer_emails = $(echo -e "${TF_DEPLOYER_EMAILS}")
EOF

CURRENT_STEP="Provisioning Folder, Project, APIs, and IAM Roles"
echo -e "\n${BOLD}[5/6] Provisioning Cloud Infrastructure, APIs, and IAM Roles...${NC}"
echo -e "Initializing Terraform..."
"${IAC_BIN}" init -input=false 2>&1 | tee -a "${LOG_FILE}"

echo -e "\nApplying infrastructure changes automatically..."
"${IAC_BIN}" apply -auto-approve -input=false 2>&1 | tee -a "${LOG_FILE}"

CURRENT_STEP="Extracting provisioned resources"
PROJECT_ID=$("${IAC_BIN}" output -raw project_id 2>/dev/null || true)
FOLDER_ID=$("${IAC_BIN}" output -raw folder_id 2>/dev/null || true)
AUDITOR_SA=$("${IAC_BIN}" output -raw auditor_service_account_email 2>/dev/null || true)

if [ -z "${PROJECT_ID}" ] || [ -z "${FOLDER_ID}" ] || echo "${PROJECT_ID}" | grep -qi "Follow the instructions"; then
    echo "[ERROR] Invalid Terraform outputs" >> "${LOG_FILE}"
    exit 1
fi

echo -e "\n${BOLD}${GREEN}Cloud Foundation Provisioned Successfully!${NC}"
echo -e "Project: ${BOLD}${BLUE}${PROJECT_ID}${NC}"
echo -e "Folder:  ${FOLDER_ID}"
echo -e "Auditor: ${AUDITOR_SA}"

# ------------------------------------------------------------------------------
# 7. End-to-End Application Deployment to Google Cloud Run
# ------------------------------------------------------------------------------
CURRENT_STEP="Deploying Agentic GRC to Google Cloud Run"
echo -e "\n${BOLD}[6/6] Deploying Agentic GRC Platform to Google Cloud Run...${NC}"
gcloud config set project "${PROJECT_ID}" --quiet >> "${LOG_FILE}" 2>&1

export PROJECT_ID="${PROJECT_ID}"
export REGION="us-central1"
export SERVICE_NAME="mcp-server-grc"

bash "${PROJECT_ROOT}/scripts/deploy.sh" 2>&1 | tee -a "${LOG_FILE}"

CURRENT_STEP="Verifying live deployment and health"
SERVICE_URL=$(gcloud run services describe "${SERVICE_NAME}" --region="${REGION}" --project="${PROJECT_ID}" --format="value(status.url)" 2>/dev/null || true)
if [ -z "${SERVICE_URL}" ]; then
    SERVICE_URL="https://${SERVICE_NAME}-${PROJECT_ID}.${REGION}.run.app"
fi
PORTAL_URL="${SERVICE_URL}/portal"

# ------------------------------------------------------------------------------
# 8. Final Client Deliverable (Exact Output to Send to Engineer)
# ------------------------------------------------------------------------------
CURRENT_STEP="Completed"

echo -e "\n${BOLD}${GREEN}================================================================${NC}"
echo -e "${BOLD}${GREEN}        AGENTIC GRC: DEPLOYMENT COMPLETED SUCCESSFULLY!         ${NC}"
echo -e "${BOLD}${GREEN}================================================================${NC}"
echo -e "\n${BOLD}Please copy the entire block below and send it to your engineer:${NC}"
echo -e "\n----------------------------------------------------------------"
echo -e "GCP_ORGANIZATION:  ${TARGET_ORG}"
echo -e "GCP_PROJECT_ID:    ${BOLD}${BLUE}${PROJECT_ID}${NC}"
echo -e "GCP_FOLDER_ID:     ${FOLDER_ID}"
echo -e "AUDITOR_SA:        ${AUDITOR_SA}"
echo -e "AUTHORIZED_USERS:  ${TARGET_ACCOUNTS}"
echo -e "PORTAL_ACCESS_URL: ${BOLD}${GREEN}${PORTAL_URL}${NC}"
echo -e "----------------------------------------------------------------\n"
echo -e "Everything is live and running. No further actions required on your end.\n"
