# How-To Guide: Deploying and Running the Agentic GRC Platform

This guide provides step-by-step instructions for provisioning the Google Cloud Platform (GCP) organization hierarchy, deploying the autonomous compliance agent to Cloud Run, and connecting it to Gemini Enterprise.

---

## 1. Prerequisites

Before starting, verify that your environment has:
- Google Cloud SDK (`gcloud`) installed and authenticated:
  ```bash
  gcloud auth login
  gcloud auth application-default login
  ```
- An active GCP user account with the following roles:
  - Organization Administrator (`roles/resourcemanager.organizationAdmin`) or Folder Creator (`roles/resourcemanager.folderCreator`) + Project Creator (`roles/resourcemanager.projectCreator`) on the target Organization.
  - Organization IAM Administrator (`roles/iam.admin`) to grant organization-wide read roles.
  - Billing Account User (`roles/billing.user`) on an active billing account.
- Python 3.12+ and `make` installed locally.

---

## 2. Automated Deployment (Recommended)

### Step 2.1: Provision the Organization Folder, Project, and IAM Roles

Run the provisioning script using `make`:

```bash
make provision-org
```

**What this command does automatically:**
1. Creates a dedicated folder named `fldr-agentic-grc` under your GCP Organization (`31564119954`).
2. Creates a dedicated project named `agentic-grc-<suffix>` inside that folder.
3. Links your active Billing Account (`0180FF-1553BD-6B74BE`) to the new project.
4. Enables all required APIs:
   - `modelarmor.googleapis.com` (Model Armor Safety Gate)
   - `run.googleapis.com` (Cloud Run Serverless Compute)
   - `cloudasset.googleapis.com` (Cloud Asset Inventory)
   - `securitycenter.googleapis.com` (Security Command Center)
   - `accesscontextmanager.googleapis.com` (VPC Service Controls)
   - `cloudkms.googleapis.com` (Key Management Service)
   - `bigquery.googleapis.com` (Audit Log Sinks)
   - `aiplatform.googleapis.com` (Vertex AI Platform)
   - `discoveryengine.googleapis.com` (Gemini Enterprise Discovery Engine)
5. Creates a dedicated Service Account: `sa-agentic-grc-auditor@<PROJECT_ID>.iam.gserviceaccount.com`.
6. Binds organization-level read privileges to the Service Account on the organization:
   - `roles/cloudasset.viewer`: Real-time inspection of all GCP assets across all projects.
   - `roles/browser`: Hierarchy traversal across all folders and projects.
   - `roles/iam.securityReviewer`: Organization-wide IAM policy and permissions review.
   - `roles/securitycenter.findingsViewer`: Organization-wide Security Command Center findings.
   - `roles/accesscontextmanager.policyReader`: VPC Service Controls perimeter review.
7. Deploys the Model Armor security baseline template (`g-rc-safety-baseline`).

---

### Step 2.2: Deploy the Agent and Client Web Portal

Set the environment variables with the project ID output from Step 2.1 and execute the journey:

```bash
export PROJECT_ID="<OUTPUT_PROJECT_ID>"
export REGION="us-central1"

make journey
```

**What this command does automatically:**
1. Executes the quality and security test suite (56 unit and integration tests).
2. Deploys the combined StreamableHTTP MCP server and Client Web Portal container to Cloud Run.
3. Performs an end-to-end smoke test validating the continuous audit engine.
4. Prints the live HTTPS URL for the client portal.

---

### Step 2.3: Access the Client Portal

Open the printed URL in your browser:
```text
https://<SERVICE_NAME>-<HASH>.a.run.app/portal
```

*(For local testing without deploying to GCP, run `make run-portal` and visit `http://localhost:8080/portal`)*

---

## 3. Connecting to Gemini Enterprise (Agent Studio)

To enable chatbot interactions directly inside Google Cloud Vertex AI / Gemini Enterprise:

1. Open the Google Cloud Console and navigate to **Vertex AI** > **Agent Studio**.
2. Select or create an Agent.
3. In the left navigation, click **Tools** > **Create Tool**.
4. Choose **Model Context Protocol (MCP)**.
5. In the **Server URL** field, paste your deployed Cloud Run URL pointing to the `/mcp` endpoint:
   ```text
   https://<YOUR_CLOUD_RUN_URL>/mcp
   ```
6. Agent Studio will query the Discovery Endpoint (`/.well-known/agent.json`) and automatically register all compliance skills:
   - `audit_cloud_security`
   - `scan_iac_configuration`
   - `correlate_threat_intelligence`
   - `audit_climate_resilience`
   - `audit_data_leakage_prevention`
   - `audit_monitoring_activities`

---

## 4. Using the Client Web Portal

The deployed web portal provides an intuitive dashboard divided into five tabs:

### Tab 1: Chatbot Auditor
- Send natural language prompts (e.g., *"Execute proactive audit"*, *"Audit KMS cryptography A.8.24"*, *"Horizon scanning regulatory update"*).
- The agent orchestrates subagents, queries the live evidence graph, evaluates compliance, and returns structured findings.

### Tab 2: Sub-Agents
- View the real-time operational status and cryptographic SPIFFE identity of each specialized sub-agent:
  - `AnnexASubAgent` (ISO 27001 Annex A controls)
  - `GCPTelemetrySubAgent` (Asset inventory and telemetry)
  - `OrgPoliciesSubAgent` (Policy cross-referencing)
  - `HorizonScannerSubAgent` (Regulatory updates and climate resilience)
  - `CodeMender` (Planned backlog)
- Trigger individual sub-agents on demand.

### Tab 3: Upload & Connect
- **Compliance Artifact Upload**: Drag and drop Terraform files (`.tf`), Ansible playbooks (`.yml`), or organizational policy files (`.json`, `.txt`). The scanner evaluates misconfigurations immediately.
- **Zero-Copy Storage Link**: Connect Google Drive, SharePoint, Jira, or Confluence by supplying the folder ID or repository URL. Files are analyzed at the source without copying data externally.

### Tab 4: Audit Dashboard & HITL Gate
- View the overall compliance scorecard and temporal drift velocity.
- Review and approve pending Human-in-the-Loop (HITL) remediation playbooks or policy amendments.

### Tab 5: Gemini Integration
- View setup instructions and embed code for internal client intranets.

---

## 5. Local Development and Testing Commands

| Command | Purpose |
| :--- | :--- |
| `make install` | Install Python dependencies into `.venv` using `uv`. |
| `make test` | Run the complete 56-test suite with coverage reporting. |
| `make run-portal` | Start the local web portal on `http://localhost:8080/portal`. |
| `make audit-poc` | Run a standalone proof-of-concept audit script. |
| `make provision-org` | Provision GCP folder, project, and org-level IAM roles. |
| `make journey` | Full end-to-end test, container build, and Cloud Run deployment. |
| `make clean` | Remove temporary cache and test artifacts. |

---

## 6. Verification and Troubleshooting

- **Check Cloud Run service status**:
  ```bash
  gcloud run services describe mcp-server-grc --project="<PROJECT_ID>" --region="us-central1"
  ```
- **Check Cloud Run logs**:
  ```bash
  gcloud logging read "resource.type=cloud_run_revision AND resource.labels.service_name=mcp-server-grc" --project="<PROJECT_ID>" --limit=20
  ```
- **Verify Organization IAM Bindings**:
  ```bash
  gcloud organizations get-iam-policy 31564119954 --filter="bindings.members:sa-agentic-grc-auditor"
  ```
