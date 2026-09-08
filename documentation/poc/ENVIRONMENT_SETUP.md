# Infrastructure & Environment Setup Guide
## Complete Deployment & Provisioning Manual for Google Cloud Security & Agentic GRC

> **Document Version**: 1.0.0  
> **Status**: Production Ready  
> **Target Audience**: DevOps Engineers, Cloud Platform Admins, Security Engineers  
> **Platform**: Google Cloud Platform (GCP) • Cloud Run • Terraform • Docker  
> **Repository**: `https://github.com/g-jsaccomani/agentic_grc_certifications.git`  
> **Language**: English

---

## 1. Overview & Architecture Workflow

The deployment of the Agentic GRC Auditor follows a strict **Two-Phase Architecture**:

1. **Phase 1: Infrastructure & Security Identity Bootstrap (Terraform)**:
   - Provisions a dedicated folder (`fldr-agentic-grc`) and host project in your GCP Organization.
   - Enables all 16 required Google Cloud APIs.
   - Configures the auditor service account (`sa-agentic-grc-auditor`) with read-only organization-level IAM permissions.
2. **Phase 2: Container Packaging & Cloud Run Deployment (`make journey`)**:
   - Executes the automated 184-test validation suite.
   - Builds the production container image via Google Cloud Build.
   - Deploys the service to Google Cloud Run with managed HTTPS, zero-trust headers, and autoscaling.

```mermaid
sequenceDiagram
    autonumber
    actor Admin as GCP Organization Admin
    actor Engineer as DevOps / Security Engineer
    participant TF as Terraform Bootstrap
    participant GCP as Google Cloud Platform
    participant Build as Cloud Build & Artifact Registry
    participant Run as Cloud Run (mcp-server-grc)

    Note over Admin,GCP: Phase 1: GCP Infrastructure & Identity Bootstrap
    Admin->>TF: terraform apply (or bootstrap.sh)
    TF->>GCP: Create Folder & Host Project (agentic-grc-xxxx)
    TF->>GCP: Enable 16 APIs (Model Armor, Asset Inventory, Cloud Run, Vertex AI)
    TF->>GCP: Create Service Account (sa-agentic-grc-auditor)
    TF->>GCP: Bind Org-Level Read Roles (cloudasset.viewer, iam.securityReviewer)
    TF-->>Admin: Outputs PROJECT_ID

    Note over Engineer,Run: Phase 2: Application Build & Cloud Run Deployment
    Engineer->>GCP: gcloud auth login & set PROJECT_ID
    Engineer->>Build: make journey (runs 184 tests & builds container)
    Build->>Run: Deploy container to Cloud Run (us-central1, min-instances=1)
    Run->>Run: Execute live smoke tests
    Run-->>Engineer: Live HTTPS Portal (https://<RUN_URL>/portal)
```

---

## 2. Tooling & System Prerequisites

Ensure your deployment workstation has the following tools installed and authenticated:

| Tool | Minimum Version | Verification Command | Description |
| :--- | :--- | :--- | :--- |
| **Git** | 2.30+ | `git --version` | Source code management. |
| **Python** | 3.11 or 3.12 | `python3 --version` | Runtime for MCP server and automated tests. |
| **Google Cloud SDK** | 460.0.0+ | `gcloud --version` | Authenticated with GCP Organization or Project privileges. |
| **Terraform** | >= 1.5.0 | `terraform -version` | Infrastructure as Code provisioning. |
| **uv** (Optional) | Latest | `uv --version` | Ultra-fast Python package manager (Makefile auto-detects). |
| **Docker** (Optional)| 24.0+ | `docker --version` | Local container execution (Cloud Build is default). |

---

## 3. Phase 1: GCP Infrastructure & Security Identity Bootstrap

### 3.1 Automated Cloud Shell Flow (Fastest)
Run this single command inside [Google Cloud Shell](https://shell.cloud.google.com):
```bash
curl -sSL https://raw.githubusercontent.com/g-jsaccomani/agentic_grc_certifications/main/terraform/first_steps/bootstrap.sh | bash
```
When execution completes, note the generated `PROJECT_ID`:
```text
======================================================================
PROJECT_ID: agentic-grc-cd06
======================================================================
```

### 3.2 Manual Terraform Bootstrap Execution
If running from your local workstation:
```bash
cd terraform/first_steps
cp terraform.tfvars.example terraform.tfvars
```

Edit `terraform.tfvars` with your organization and billing details:
```hcl
organization_id    = "123456789012"
billing_account_id = "012345-6789AB-CDEF01"
region             = "us-central1"
project_prefix     = "agentic-grc"
```

Initialize and apply:
```bash
terraform init
terraform apply -auto-approve
```

### 3.3 What is Automatically Created
1. **Dedicated GCP Folder**: `fldr-agentic-grc` isolating compliance operations.
2. **Dedicated GCP Project**: `agentic-grc-<id>` attached to your designated billing account.
3. **16 Required APIs**:
   - `modelarmor.googleapis.com` (Prompt-injection & safety defense)
   - `run.googleapis.com` (Cloud Run serverless hosting)
   - `cloudasset.googleapis.com` (Cloud Asset Inventory real-time query)
   - `securitycenter.googleapis.com` (Security Command Center findings)
   - `accesscontextmanager.googleapis.com` (VPC-SC perimeter audit)
   - `cloudkms.googleapis.com` (KMS key inspection & rotation)
   - `bigquery.googleapis.com` (Audit logging analytics)
   - `aiplatform.googleapis.com` (Vertex AI platform & Gemini 2.5)
   - `discoveryengine.googleapis.com` (Gemini Enterprise integration)
   - `artifactregistry.googleapis.com` (Container images)
   - `cloudbuild.googleapis.com` (Container build pipeline)
   - `iam.googleapis.com`, `cloudresourcemanager.googleapis.com`, `serviceusage.googleapis.com`, `logging.googleapis.com`, `monitoring.googleapis.com`
4. **Service Account**: `sa-agentic-grc-auditor@<PROJECT_ID>.iam.gserviceaccount.com`.
5. **Organization-Level Read-Only IAM Bindings**:
   - `roles/cloudasset.viewer`: Query any asset state across all projects.
   - `roles/browser`: Read organization and folder hierarchy.
   - `roles/iam.securityReviewer`: Audit IAM bindings without write access.
   - `roles/securitycenter.findingsViewer`: Read SCC security findings.
   - `roles/accesscontextmanager.policyReader`: Read VPC Service Controls perimeters.

---

## 4. Google Workspace OAuth 2.0 Client Setup

The portal integrates with Google Workspace Single Sign-On. To configure authentication:

1. In the Google Cloud Console, navigate to **APIs & Services** > **Credentials**.
2. Click **Create Credentials** > **OAuth Client ID**.
3. Select Application type: **Web application**.
4. Set **Name**: `Agentic GRC Portal`.
5. Under **Authorized JavaScript Origins**, add:
   - `http://localhost:8080` (Local testing)
   - `https://<YOUR_SERVICE_NAME>-<HASH>.a.run.app` (Cloud Run production URL)
6. Under **Authorized Redirect URIs**, add:
   - `http://localhost:8080/portal`
   - `https://<YOUR_SERVICE_NAME>-<HASH>.a.run.app/portal`
7. Click **Create**. Copy the generated `Client ID`.
8. Configure the client ID directly in the portal code:
   Edit the `GOOGLE_WORKSPACE_CONFIG.clientId` (and optionally `expectedDomain`) value directly in `mcp_server_grc/portal_html.py` (around line 9723) and redeploy:
   ```javascript
   const GOOGLE_WORKSPACE_CONFIG = {
       clientId: "<YOUR_CLIENT_ID>.apps.googleusercontent.com",
       expectedDomain: "client.corp",
       ...
   };
   ```
   After updating, redeploy using `bash scripts/deploy.sh` or `make journey`.

---

## 5. Granting Consultant/Partner Access for Final Configuration

When engaging external security consultants or technical partners to assist with deployment, verification, and final configuration, adhere strictly to the principle of least privilege using time-boxed, temporary IAM conditions.

### 5.1 Required Scoped Roles
Grant access only to the host project (`PROJECT_ID`) where the Cloud Run service and deployment artifacts reside. The consultant requires:
- `roles/run.admin`: Manage, deploy, and inspect Cloud Run services.
- `roles/iam.serviceAccountUser`: Impersonate the Cloud Run runtime service account during deployment.
- `roles/resourcemanager.projectIamAdmin` (or narrower `roles/iam.securityAdmin`): Configure service-to-service IAM bindings.
- `roles/serviceusage.serviceUsageAdmin`: Enable required GCP APIs if additional services are introduced.

### 5.2 Time-Boxed IAM Binding Grant Command
The client organization admin executes the following command, specifying an explicit expiry timestamp (e.g., 7 days from setup):

```bash
PROJECT_ID="<YOUR_HOST_PROJECT_ID>"
CONSULTANT_USER="user:consultant@partner.corp"
EXPIRY_TIMESTAMP="$(date -u -v+7d "+%Y-%m-%dT%H:%M:%SZ" 2>/dev/null || date -u -d "+7 days" "+%Y-%m-%dT%H:%M:%SZ")"

for ROLE in \
  "roles/run.admin" \
  "roles/iam.serviceAccountUser" \
  "roles/resourcemanager.projectIamAdmin" \
  "roles/serviceusage.serviceUsageAdmin"; do
  gcloud projects add-iam-policy-binding "${PROJECT_ID}" \
    --member="${CONSULTANT_USER}" \
    --role="${ROLE}" \
    --condition="expression=request.time < timestamp('${EXPIRY_TIMESTAMP}'),title=temporary_consultant_access,description=Expires at ${EXPIRY_TIMESTAMP}" \
    --quiet
done
```

### 5.3 Immediate Revocation Command (Post-Configuration)
Once deployment and handover are verified, the client revokes all temporary bindings immediately:

```bash
PROJECT_ID="<YOUR_HOST_PROJECT_ID>"
CONSULTANT_USER="user:consultant@partner.corp"

for ROLE in \
  "roles/run.admin" \
  "roles/iam.serviceAccountUser" \
  "roles/resourcemanager.projectIamAdmin" \
  "roles/serviceusage.serviceUsageAdmin"; do
  gcloud projects remove-iam-policy-binding "${PROJECT_ID}" \
    --member="${CONSULTANT_USER}" \
    --role="${ROLE}" \
    --all \
    --quiet
done
```

---

## 6. Phase 2: Application Build & Cloud Run Deployment

Deploy the platform container to Cloud Run using the automated build script:

### Step 6.1: Authenticate gcloud
```bash
gcloud auth login
gcloud auth application-default login
```

### Step 6.2: Set Environment Variables
```bash
export PROJECT_ID="<YOUR_PROJECT_ID_FROM_PHASE_1>"
export REGION="us-central1"
export SERVICE_NAME="mcp-server-grc"
```

### Step 6.3: Run Automated Deployment Journey
```bash
make journey
```

#### What `make journey` Executes:
1. Runs the complete test suite (184 unit, integration, and guardrail tests).
2. Submits the code to Google Cloud Build.
3. Builds and pushes the Docker container to Artifact Registry.
4. Deploys to Cloud Run with:
   - `--min-instances=1` (Prevents cold starts during demos).
   - `--memory=2Gi` and `--cpu=2`.
   - `--allow-unauthenticated` (Zero-trust identity handled at application layer).
5. Runs automated HTTP smoke tests against `/portal` and `/api/audit/summary`.
6. Prints the public live HTTPS URL.

---

## 7. Functional Lab Projects Setup (POC Target Scope)

For POC demonstrations, the system audits multi-project environments. You can connect existing corporate non-prod projects or provision the functional lab projects:

| Project ID | Role in POC | Assets Audited |
| :--- | :--- | :--- |
| `fnlab-apps-8fa913` | Application Workloads | GCS Buckets, Non-compliant SSH Firewall, Software KMS Keys |
| `fnlab-ai-data-8fa913` | AI & Analytics Data | GCS Analytics Buckets, Over-privileged IAM Owner roles |
| `fnlab-sec-mgmt-8fa913`| Security & Management | Compliant HSM KMS Keys, Internal Management Firewalls |
| `aispr-core-1cab11` | Core Infrastructure | Log storage buckets, Open RDP Firewall Rules |

To verify that the service account can inspect all target projects:
```bash
python scripts/verify_poc_environment.py
```

---

## 8. Local Development & Testing Workflow

To run and modify the platform locally:

### 8.1 Install Virtual Environment
```bash
make install
```
*(Creates `.venv` using `uv` or `python -m venv` and installs all dependencies).*

### 8.2 Run Test Suite
```bash
make test
```
*(Executes all 184 tests with coverage output).*

### 8.3 Launch Local Web Portal
```bash
make run-portal
```
Open your browser and navigate to:
```text
http://localhost:8080/portal
```

### 8.4 Launch Standalone MCP Server
To expose the Model Context Protocol (MCP) server on port 8080 for Gemini Enterprise Agent Studio:
```bash
make run-mcp
```

---

## 9. Maintenance & Operational Commands

| Command | Purpose |
| :--- | :--- |
| `make clean` | Clean temporary `.pytest_cache`, `__pycache__`, and build artifacts. |
| `make test` | Run full automated test suite. |
| `make run-portal` | Start local portal server on port 8080. |
| `make journey` | Full end-to-end test, container build, and Cloud Run deployment. |
| `python scripts/verify_poc_environment.py` | Verify live telemetry access across target GCP projects. |
| `./scripts/cleanup_poc_resources.sh --dry-run` | Preview cleanup of temporary POC resources. |
