#!/usr/bin/env bash
# ==============================================================================
# AGENTIC GRC: TIME-BOXED READ-ONLY CLIENT ONBOARDING SCRIPT
# Provisions temporary read-only IAM bindings (roles/viewer, roles/securityReviewer)
# with an automated expiration condition, and registers client workspace.
# MANDATE: Zero write permissions on client resources.
# ==============================================================================

set -euo pipefail

BOLD="\033[1m"
GREEN="\033[0;32m"
YELLOW="\033[1;33m"
BLUE="\033[0;34m"
RED="\033[0;31m"
NC="\033[0m"

CLIENT_NAME="New Client Workspace"
PROJECTS_ARG=""
ORG_ID_ARG=""
EXPIRY_DAYS="30"
AUDITOR_EMAIL=""
DRIVE_FOLDER_ARG=""
OUTPUT_FILE="grc_onboarding_config.txt"

while [[ $# -gt 0 ]]; do
    case "$1" in
        --client=*)
            CLIENT_NAME="${1#*=}"
            shift
            ;;
        --client)
            CLIENT_NAME="$2"
            shift 2
            ;;
        --consultant=*|--email=*)
            AUDITOR_EMAIL="${1#*=}"
            shift
            ;;
        --consultant|--email)
            AUDITOR_EMAIL="$2"
            shift 2
            ;;
        --projects=*)
            PROJECTS_ARG="${1#*=}"
            shift
            ;;
        --projects)
            PROJECTS_ARG="$2"
            shift 2
            ;;
        --org=*)
            ORG_ID_ARG="${1#*=}"
            shift
            ;;
        --org)
            ORG_ID_ARG="$2"
            shift 2
            ;;
        --days=*)
            EXPIRY_DAYS="${1#*=}"
            shift
            ;;
        --days)
            EXPIRY_DAYS="$2"
            shift 2
            ;;
        --drive-folder=*)
            DRIVE_FOLDER_ARG="${1#*=}"
            shift
            ;;
        --drive-folder)
            DRIVE_FOLDER_ARG="$2"
            shift 2
            ;;
        --output=*)
            OUTPUT_FILE="${1#*=}"
            shift
            ;;
        --output)
            OUTPUT_FILE="$2"
            shift 2
            ;;
        *)
            shift
            ;;
    esac
done

echo -e "${BOLD}${BLUE}================================================================${NC}"
echo -e "${BOLD}${BLUE}     AGENTIC GRC: AUTOMATED CLIENT WORKSPACE ONBOARDING         ${NC}"
echo -e "${BOLD}${BLUE}================================================================${NC}"
echo -e "Client Name:         ${BOLD}${GREEN}${CLIENT_NAME}${NC}"
echo -e "Access Expiration:   ${EXPIRY_DAYS} days"
echo -e "Access Type:         ${BOLD}READ-ONLY ONLY (roles/viewer, roles/securityReviewer)${NC}"
echo -e "Security Mandate:    ${YELLOW}No service account used during live inspection has write permissions.${NC}\n"

# Resolve auditor email if not passed
if [ -z "${AUDITOR_EMAIL}" ]; then
    AUDITOR_EMAIL=$(gcloud config get-value account 2>/dev/null || echo "auditor@client.corp")
fi

# Resolve projects list
PROJECTS=()
if [ -n "${PROJECTS_ARG}" ]; then
    IFS=',' read -ra ADDR <<< "${PROJECTS_ARG}"
    for p in "${ADDR[@]}"; do
        trimmed=$(echo "$p" | sed -e 's/^[[:space:]]*//' -e 's/[[:space:]]*$//')
        if [ -n "$trimmed" ]; then PROJECTS+=("$trimmed"); fi
    done
else
    # Detect current project or list accessible projects
    CURR_PROJ=$(gcloud config get-value project 2>/dev/null || true)
    if [ -n "${CURR_PROJ}" ] && [ "${CURR_PROJ}" != "(unset)" ]; then
        PROJECTS+=("${CURR_PROJ}")
    else
        PROJECTS+=("client-prod-scope")
    fi
fi

# Detect organization
if [ -z "${ORG_ID_ARG}" ]; then
    ORG_ID_ARG=$(gcloud organizations list --format="value(ID)" 2>/dev/null | head -n 1 || true)
    if [ -z "${ORG_ID_ARG}" ]; then
        ORG_ID_ARG=$(gcloud organizations list --format="value(name)" 2>/dev/null | head -n 1 | awk -F'/' '{print $NF}' || echo "")
    fi
fi

# Detect organization display name
ORG_NAME=$(gcloud organizations list --format="value(DISPLAY_NAME)" 2>/dev/null | head -n 1 || true)
if [ -z "${ORG_NAME}" ]; then
    ORG_NAME="${CLIENT_NAME}"
fi

# Compute expiry timestamp using python3
EXPIRY_ISO=$(python3 -c "import datetime; print((datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=int('${EXPIRY_DAYS}'))).strftime('%Y-%m-%dT%H:%M:%SZ'))")

# Determine member prefix
if [[ "${AUDITOR_EMAIL}" == *"gserviceaccount.com"* ]]; then
    MEMBER="serviceAccount:${AUDITOR_EMAIL}"
else
    MEMBER="user:${AUDITOR_EMAIL}"
fi

echo -e "[1/4] Configuring Read-Only Auditor Permissions (Least Privilege)..."
CONDITION_EXPR="request.time < timestamp(\"${EXPIRY_ISO}\")"

# Organization-level binding if available
if [ -n "${ORG_ID_ARG}" ]; then
    echo -e "  - Applying Organization-Level Read-Only roles to ${BOLD}${ORG_ID_ARG}${NC}..."
    for r in "roles/viewer" "roles/iam.securityReviewer" "roles/resourcemanager.organizationViewer"; do
        gcloud organizations add-iam-policy-binding "${ORG_ID_ARG}" \
            --member="${MEMBER}" \
            --role="${r}" \
            --condition=None \
            --quiet >/dev/null 2>&1 || true
    done
fi

for proj in "${PROJECTS[@]}"; do
    echo -e "  - Binding read-only auditor permissions to project: ${BOLD}${proj}${NC}"
    if command -v gcloud >/dev/null 2>&1 && gcloud projects describe "${proj}" >/dev/null 2>&1; then
        gcloud projects add-iam-policy-binding "${proj}" \
            --member="${MEMBER}" \
            --role="roles/viewer" \
            --condition="expression=${CONDITION_EXPR},title=temp_grc_readonly,description=Time-boxed read-only compliance access" \
            --quiet >/dev/null 2>&1 || true
        gcloud projects add-iam-policy-binding "${proj}" \
            --member="${MEMBER}" \
            --role="roles/securityReviewer" \
            --condition="expression=${CONDITION_EXPR},title=temp_grc_readonly,description=Time-boxed read-only compliance access" \
            --quiet >/dev/null 2>&1 || true
    fi
done

echo -e "\n[2/4] Registering Client Workspace in Onboarding Registry..."
python3 - <<PYEOF
import json
import os
import re
import datetime

client_name = """${CLIENT_NAME}"""
client_id = re.sub(r'[^a-z0-9]+', '-', client_name.lower()).strip('-') or "new-client"
words = client_name.split()
avatar = ("".join(w[0] for w in words[:2])).upper() if words else "CL"

raw_projects = """${PROJECTS_ARG}""".strip()
if raw_projects:
    projects = [p.strip() for p in raw_projects.split(",") if p.strip()]
else:
    projects = ["${PROJECTS[0]}"]

now_iso = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

record = {
    "client_id": client_id,
    "name": client_name,
    "avatar": avatar,
    "projects": projects,
    "org_id": "${ORG_ID_ARG}",
    "org_name": f"${ORG_NAME}",
    "contact_email": "${AUDITOR_EMAIL}",
    "drive_folder_id": "${DRIVE_FOLDER_ARG}" if "${DRIVE_FOLDER_ARG}" else None,
    "created_at": now_iso,
    "read_only_access_expires_at": "${EXPIRY_ISO}",
    "read_only_access_days_remaining": int("${EXPIRY_DAYS}"),
    "status": "active"
}

file_path = "data/clients.json"
os.makedirs(os.path.dirname(file_path), exist_ok=True)
clients = []
if os.path.exists(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            clients = json.load(f)
    except Exception:
        clients = []

found = False
for idx, c in enumerate(clients):
    if c.get("client_id") == client_id:
        clients[idx] = record
        found = True
        break
if not found:
    clients.append(record)

with open(file_path, "w", encoding="utf-8") as f:
    json.dump(clients, f, indent=2)

print(f"  ✓ Client '{client_name}' registered with ID '{client_id}' in {file_path}")
PYEOF

PROJECTS_JOINED=$(IFS=,; echo "${PROJECTS[*]}")
NOW_ISO="$(date -u +"%Y-%m-%dT%H:%M:%SZ")"

echo -e "\n[3/4] Generating Client Configuration File (${OUTPUT_FILE})..."
cat <<EOF > "${OUTPUT_FILE}"
# =====================================================================
# AGENTIC GRC - CLIENT WORKSPACE ONBOARDING CONFIGURATION
# Generated automatically by client bootstrap script
# =====================================================================
cloud_provider=gcp
client_name=${CLIENT_NAME}
org_id=${ORG_ID_ARG}
org_name=${ORG_NAME}
projects=${PROJECTS_JOINED}
access_days=${EXPIRY_DAYS}
auditor_identity=${AUDITOR_EMAIL}
drive_folder=${DRIVE_FOLDER_ARG}
generated_at=${NOW_ISO}
EOF

echo -e "  ✓ Environment configuration exported to ${BOLD}${OUTPUT_FILE}${NC}"

echo -e "\n[4/4] Generating Onboarding Summary..."
echo -e "${BOLD}${GREEN}================================================================${NC}"
echo -e "${BOLD}${GREEN}        CLIENT WORKSPACE BOOTSTRAP SUCCESSFUL!                  ${NC}"
echo -e "${BOLD}${GREEN}================================================================${NC}"
echo -e "Client Name:         ${BOLD}${CLIENT_NAME}${NC}"
echo -e "Organization:        ${ORG_NAME} (${ORG_ID_ARG:-N/A})"
echo -e "Projects in Scope:   ${#PROJECTS[@]} projects (${PROJECTS[*]})"
echo -e "Read-Only Expiry:    ${EXPIRY_ISO} (${EXPIRY_DAYS} days remaining)"
echo -e "Active Operator:     ${AUDITOR_EMAIL}"
echo -e "Permissions:         READ-ONLY (roles/viewer, roles/securityReviewer)"
echo -e "Config Output:       ${BOLD}${OUTPUT_FILE}${NC}"
echo -e "----------------------------------------------------------------"
echo -e "${BOLD}${YELLOW}>>> INSTRUÇÃO FINAL PARA O CLIENTE: <<<${NC}"
echo -e "${BOLD}Salve o arquivo de saída gerado (${OUTPUT_FILE})"
echo -e "e envie-o de volta ao consultor.${NC}"
echo -e "================================================================\n"
