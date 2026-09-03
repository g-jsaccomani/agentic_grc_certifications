#!/usr/bin/env bash
# ==============================================================================
# AGENTIC GRC: ONE-CLICK CLIENT BOOTSTRAP SCRIPT
# Handles missing Terraform/OpenTofu, prompts for install, and auto-provisions
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

# Ensure user local bin is in PATH
BIN_DIR="${HOME}/.local/bin"
mkdir -p "${BIN_DIR}"
export PATH="${BIN_DIR}:${PATH}"

# Detect System Architecture
OS=$(uname -s | tr '[:upper:]' '[:lower:]')
ARCH=$(uname -m)
case "${ARCH}" in
    x86_64) ARCH="amd64" ;;
    aarch64|arm64) ARCH="arm64" ;;
    *) ARCH="amd64" ;;
esac

# 1. Verify Google Cloud Authentication
echo -e "\n${BOLD}[1/6] Checking Google Cloud Authentication...${NC}"
CURRENT_ACCOUNT=$(gcloud config get-value account 2>/dev/null || true)
if [ -z "${CURRENT_ACCOUNT}" ]; then
    echo -e "${YELLOW}No active account found. Running gcloud auth login...${NC}"
    gcloud auth login --quiet
    CURRENT_ACCOUNT=$(gcloud config get-value account)
fi
echo -e "Authenticated as: ${BOLD}${GREEN}${CURRENT_ACCOUNT}${NC}"

# 2. Check for Functional Infrastructure-as-Code Engine (Terraform or OpenTofu)
echo -e "\n${BOLD}[2/6] Verifying Infrastructure-as-Code (IaC) Engine...${NC}"
IAC_BIN=""

# Test if an actual working terraform binary exists
if command -v terraform >/dev/null 2>&1; then
    if terraform version >/dev/null 2>&1; then
        IAC_BIN="terraform"
    fi
fi

# Test if an actual working OpenTofu binary exists
if [ -z "${IAC_BIN}" ] && command -v tofu >/dev/null 2>&1; then
    if tofu version >/dev/null 2>&1; then
        IAC_BIN="tofu"
    fi
fi

# If neither is found or functional, present choices to the client
if [ -z "${IAC_BIN}" ]; then
    echo -e "${YELLOW}Notice: Neither Terraform nor OpenTofu is currently installed in this environment.${NC}"
    echo -e "Please select which tool you would like to install:\n"
    echo -e "  ${BOLD}[1] Terraform${NC}  (Official HashiCorp binary - Recommended)"
    echo -e "  ${BOLD}[2] OpenTofu${NC}   (Open-source Linux Foundation engine)\n"

    SELECTION="1"
    # Read user input safely even if running through 'curl ... | bash' pipe
    if [ -t 0 ]; then
        read -r -p "Enter your choice [1 or 2] (default: 1): " USER_INPUT || true
        if [ -n "${USER_INPUT:-}" ]; then
            SELECTION="${USER_INPUT}"
        fi
    elif [ -e /dev/tty ]; then
        read -r -p "Enter your choice [1 or 2] (default: 1): " USER_INPUT < /dev/tty || true
        if [ -n "${USER_INPUT:-}" ]; then
            SELECTION="${USER_INPUT}"
        fi
    else
        echo -e "Non-interactive terminal detected. Auto-selecting Option 1 (Terraform)."
    fi

    if [ "${SELECTION}" == "2" ]; then
        echo -e "\n${BOLD}Installing OpenTofu (v1.8.2)...${NC}"
        TOFU_URL="https://github.com/opentofu/opentofu/releases/download/v1.8.2/tofu_1.8.2_${OS}_${ARCH}.tar.gz"
        curl -sSL -o /tmp/tofu.tar.gz "${TOFU_URL}"
        tar -xzf /tmp/tofu.tar.gz -C "${BIN_DIR}" tofu
        chmod +x "${BIN_DIR}/tofu"
        rm -f /tmp/tofu.tar.gz
        IAC_BIN="${BIN_DIR}/tofu"
        echo -e "${GREEN}OpenTofu successfully installed to ${IAC_BIN}!${NC}"
    else
        echo -e "\n${BOLD}Installing HashiCorp Terraform (v1.9.5)...${NC}"
        TF_URL="https://releases.hashicorp.com/terraform/1.9.5/terraform_1.9.5_${OS}_${ARCH}.zip"
        curl -sSL -o /tmp/terraform.zip "${TF_URL}"
        if command -v unzip >/dev/null 2>&1; then
            unzip -q -o /tmp/terraform.zip -d "${BIN_DIR}"
        else
            python3 -c "import zipfile; zipfile.ZipFile('/tmp/terraform.zip').extractall('${BIN_DIR}')"
        fi
        chmod +x "${BIN_DIR}/terraform"
        rm -f /tmp/terraform.zip
        IAC_BIN="${BIN_DIR}/terraform"
        echo -e "${GREEN}Terraform successfully installed to ${IAC_BIN}!${NC}"
    fi
fi

echo -e "Using IaC Engine: ${BOLD}${GREEN}$(${IAC_BIN} version | head -n 1)${NC}"

# 3. Detect or Confirm Organization ID
echo -e "\n${BOLD}[3/6] Identifying GCP Organization...${NC}"
DEFAULT_ORG="31564119954"
DETECTED_ORG=$(gcloud organizations list --format="value(name)" 2>/dev/null | head -n 1 | awk -F'/' '{print $NF}' || true)

if [ -n "${DETECTED_ORG}" ]; then
    TARGET_ORG="${DETECTED_ORG}"
    echo -e "Detected Organization ID: ${BOLD}${GREEN}${TARGET_ORG}${NC}"
else
    TARGET_ORG="${DEFAULT_ORG}"
    echo -e "Using Default Organization ID: ${BOLD}${TARGET_ORG}${NC}"
fi

# 4. Detect or Confirm Billing Account
echo -e "\n${BOLD}[4/6] Identifying Billing Account...${NC}"
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

# 5. Generate Configuration File
echo -e "\n${BOLD}[5/6] Generating Configuration File (terraform.tfvars)...${NC}"
cat <<EOF > terraform.tfvars
org_id          = "${TARGET_ORG}"
billing_account = "${TARGET_BILLING}"
folder_name     = "fldr-agentic-grc"
project_prefix  = "agentic-grc"
region          = "us-central1"
deployer_email  = "${DEPLOYER_EMAIL}"
EOF
echo -e "${GREEN}Configuration file generated.${NC}"

# 6. Execute Provisioning
echo -e "\n${BOLD}[6/6] Provisioning Folder, Project, APIs, and IAM Roles...${NC}"
echo -e "Running initialization (${IAC_BIN} init)..."
${IAC_BIN} init -input=false

echo -e "\nApplying infrastructure changes automatically..."
${IAC_BIN} apply -auto-approve -input=false

# 7. Extract Outputs and Display in Large, Plain Text
PROJECT_ID=$(${IAC_BIN} output -raw project_id 2>/dev/null || true)
FOLDER_ID=$(${IAC_BIN} output -raw folder_id 2>/dev/null || true)
AUDITOR_SA=$(${IAC_BIN} output -raw auditor_service_account_email 2>/dev/null || true)

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
