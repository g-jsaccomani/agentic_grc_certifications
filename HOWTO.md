# How-To Guide: Deploying and Running the Agentic GRC Platform

This guide details the complete deployment lifecycle for the Agentic GRC platform. It is designed for a two-phase workflow:

1. **Phase 1 (Client First Steps)**: The client applies a Terraform template in their GCP environment to provision the dedicated folder, host project, required APIs, auditor service account, organization-level IAM permissions, and deployer permissions.
2. **Phase 2 (Implementation & Deployment)**: The implementation engineer authenticates with GCP credentials and executes the automated deployment journey (`make journey`) to build and deploy the platform on Cloud Run.

---

## 1. Project Location and Paths

All commands and development tasks must be executed from the root of the `agentic_grc_certifications` repository:

- **Local Workstation Path**:
  ```bash
  cd "/Users/jsaccomani/Documents/Jetsky/My Projects/agentic_grc_certifications"
  ```
- **Git Clone (Fresh Workstation Setup)**:
  ```bash
  git clone git@github.com:g-jsaccomani/agentic_grc_certifications.git
  cd agentic_grc_certifications
  ```
- **Terraform First Steps Directory**:
  ```bash
  cd "/Users/jsaccomani/Documents/Jetsky/My Projects/agentic_grc_certifications/terraform/first_steps"
  ```

---

## 2. Phase 1: Client First Steps (Terraform Bootstrap)

The client provisions the baseline GCP organizational structure and access controls using the Terraform files located in `terraform/first_steps/`.

### What This Terraform Automatically Provisions

1. **Folder**: Creates `fldr-agentic-grc` under the client's GCP Organization.
2. **Project**: Creates `agentic-grc-<id>` inside the folder.
3. **Billing**: Links the client's active billing account to the new project.
4. **Cloud APIs**: Enables 16 required Google Cloud APIs:
   - `modelarmor.googleapis.com` (Model Armor Safety Gate)
   - `run.googleapis.com` (Cloud Run Serverless Compute)
   - `cloudasset.googleapis.com` (Cloud Asset Inventory)
   - `securitycenter.googleapis.com` (Security Command Center)
   - `accesscontextmanager.googleapis.com` (VPC Service Controls)
   - `cloudkms.googleapis.com` (Cloud Key Management Service)
   - `bigquery.googleapis.com` (Audit Log Sinks)
   - `aiplatform.googleapis.com` (Vertex AI Platform)
   - `discoveryengine.googleapis.com` (Gemini Enterprise Discovery Engine)
   - `artifactregistry.googleapis.com` (Container Registry)
   - `cloudbuild.googleapis.com` (Build Automation)
   - `iam.googleapis.com`
   - `cloudresourcemanager.googleapis.com`
   - `serviceusage.googleapis.com`
   - `logging.googleapis.com`
   - `monitoring.googleapis.com`
5. **Auditor Identity**: Creates Service Account `sa-agentic-grc-auditor@<PROJECT_ID>.iam.gserviceaccount.com`.
6. **Organization-Level IAM Bindings**: Binds read-only inspection roles to the auditor service account at the organization level:
   - `roles/cloudasset.viewer`: Real-time inspection of cloud resources across all projects.
   - `roles/browser`: Organizational hierarchy navigation.
   - `roles/iam.securityReviewer`: IAM policy review across the organization.
   - `roles/securitycenter.findingsViewer`: Organization-wide security posture findings.
   - `roles/accesscontextmanager.policyReader`: VPC Service Controls inspection.
7. **Deployer Permissions**: Grants the implementation engineer deployment permissions on the host project (`roles/run.admin`, `roles/iam.serviceAccountUser`, `roles/storage.admin`, `roles/artifactregistry.admin`, `roles/cloudbuild.builds.editor`).

### Client Execution (Choose Option A, B, or C)

#### Option A: Zero-Git One-Command Flow (Recommended for Non-Technical Clients)

Send these 3 simple steps to the client:

1. Open Google Cloud Shell: [https://shell.cloud.google.com](https://shell.cloud.google.com)
2. Paste this single command into the terminal and press Enter:
   ```bash
   curl -sSL https://raw.githubusercontent.com/g-jsaccomani/agentic_grc_certifications/main/terraform/first_steps/bootstrap.sh | bash
   ```
3. The script automatically detects the Organization ID, links billing, enables the APIs, and provisions the security identity. When finished, copy the printed line:
   ```text
   PROJECT_ID: agentic-grc-xxxx
   ```
   and send it to the implementation engineer.

#### Option B: Direct 1-Click Cloud Shell Link

If the client prefers a direct browser link:
- Click: [Open in Cloud Shell](https://shell.cloud.google.com/?cloudshell_git_repo=https://github.com/g-jsaccomani/agentic_grc_certifications.git&cloudshell_working_dir=terraform/first_steps)
- When the terminal opens, type `./bootstrap.sh` and press Enter.

#### Option C: Manual Terraform Execution (For Technical Administrators)

```bash
cd terraform/first_steps
cp terraform.tfvars.example terraform.tfvars
terraform init
terraform apply
```

---

## 3. Phase 2: Engineer Authentication and Application Deployment

Once the client completes Phase 1, the implementation engineer executes the deployment journey.

### Step 3.1: Authenticate with GCP Credentials

Authenticate your local terminal to GCP:

```bash
gcloud auth login
gcloud auth application-default login
```

### Step 3.2: Navigate to the Repository

Navigate to the project root:

```bash
cd "/Users/jsaccomani/Documents/Jetsky/My Projects/agentic_grc_certifications"
```

### Step 3.3: Run the Automated Deployment Journey

Set the target project ID (from Phase 1 output) and run `make journey`:

```bash
export PROJECT_ID="<OUTPUT_PROJECT_ID>"
export REGION="us-central1"

make journey
```

**What `make journey` does automatically:**
1. Executes the 56-test suite verifying the multi-agent graph, Model Armor safety, and Zero-Copy connectors.
2. Builds and packages the container containing the MCP server and web portal.
3. Deploys the service to Google Cloud Run.
4. Runs an automated smoke test verifying the Continuous Intelligence audit engine against live APIs.
5. Prints the live HTTPS URL for the client portal.

### Step 3.4: Access the Live Client Portal

Open the printed URL in your browser:
```text
https://<SERVICE_NAME>-<HASH>.a.run.app/portal
```

*(To run the portal locally without Cloud Run, run `make run-portal` and visit `http://localhost:8080/portal`)*

---

## 4. Alternative: Single-Script Provisioning (`make provision-org`)

If you have direct Organization Administrator privileges on the target GCP organization, you can bypass the manual Terraform upload and provision the folder, project, and IAM bindings with a single command:

```bash
cd "/Users/jsaccomani/Documents/Jetsky/My Projects/agentic_grc_certifications"
make provision-org
```

Then proceed directly to Step 3.3 (`make journey`).

---

## 5. Connecting to Gemini Enterprise (Agent Studio)

To connect the deployed compliance agent into Vertex AI / Gemini Enterprise:

1. In the Google Cloud Console, navigate to **Vertex AI** > **Agent Studio**.
2. Select or create an agent.
3. Click **Tools** > **Create Tool** > **Model Context Protocol (MCP)**.
4. In the **Server URL** field, enter your deployed Cloud Run URL pointing to the `/mcp` endpoint:
   ```text
   https://<YOUR_CLOUD_RUN_URL>/mcp
   ```
5. Agent Studio will automatically discover and register the audit skills via `/.well-known/agent.json`:
   - `audit_cloud_security` (A.5.23, A.8.20, A.8.24)
   - `scan_iac_configuration` (A.8.9)
   - `correlate_threat_intelligence` (A.5.7)
   - `audit_climate_resilience` (Amd 1:2024 Clauses 4.1 & 4.2)
   - `audit_data_leakage_prevention` (A.8.12)
   - `audit_monitoring_activities` (A.8.16)

---

## 6. Client Web Portal Features

The portal dashboard includes five primary operational tabs:

1. **Chatbot Auditor**: Natural language chat interface grounded in the live evidence graph and Model Armor guardrails.
2. **Sub-Agents**: View and invoke specialized sub-agents (`AnnexASubAgent`, `GCPTelemetrySubAgent`, `OrgPoliciesSubAgent`, `HorizonScannerSubAgent`).
3. **Upload & Connect**:
   - Upload Terraform (`.tf`), Ansible (`.yml`), or policy files (`.json`, `.txt`) for instant local misconfiguration analysis.
   - Configure Zero-Copy connectors (Google Drive, SharePoint, Jira, Confluence) to audit documentation at the source.
4. **Audit Dashboard & HITL Gate**: Continuous compliance score, temporal drift velocity, and approval gate for remediation playbooks.
5. **Gemini Integration**: Intranet embed code and REST/MCP endpoints.

---

## 7. Developer & Maintenance Command Reference

| Command | Purpose |
| :--- | :--- |
| `make install` | Install Python dependencies into `.venv` using `uv`. |
| `make test` | Run the complete 56-test suite with coverage reporting. |
| `make run-portal` | Start the local web portal on `http://localhost:8080/portal`. |
| `make audit-poc` | Run a standalone proof-of-concept audit script. |
| `make provision-org` | Run the bash script to provision GCP folder, project, and org-level IAM roles. |
| `make journey` | Full end-to-end test, container build, and Cloud Run deployment. |
| `make clean` | Remove temporary cache and test artifacts. |

---

## 8. Verification and Troubleshooting

- **Inspect Cloud Run Service**:
  ```bash
  gcloud run services describe mcp-server-grc --project="<PROJECT_ID>" --region="us-central1"
  ```
- **Read Service Logs**:
  ```bash
  gcloud logging read "resource.type=cloud_run_revision AND resource.labels.service_name=mcp-server-grc" --project="<PROJECT_ID>" --limit=30
  ```
- **Verify Organization-Level Auditor Bindings**:
  ```bash
  gcloud organizations get-iam-policy 31564119954 --filter="bindings.members:sa-agentic-grc-auditor"
  ```
- **Verify Project Deployer Permissions**:
  ```bash
  gcloud projects get-iam-policy "<PROJECT_ID>" --filter="bindings.members:<DEPLOYER_ACCOUNT>"
  ```
