# First Steps: GCP Bootstrap via Terraform

This Terraform configuration provisions the initial Google Cloud Platform (GCP) resources required before deploying the Agentic GRC platform:

1. **Dedicated Folder**: Creates `fldr-agentic-grc` under your GCP Organization.
2. **Dedicated Project**: Creates `agentic-grc-<id>` inside the folder.
3. **Billing Association**: Links your active billing account.
4. **API Enablement**: Enables Cloud Run, Model Armor, Cloud Asset Inventory, Security Command Center, KMS, BigQuery, Vertex AI, and Discovery Engine.
5. **Auditor Service Account**: Creates `sa-agentic-grc-auditor` and grants organization-level read privileges (`roles/cloudasset.viewer`, `roles/browser`, `roles/iam.securityReviewer`, `roles/securitycenter.findingsViewer`, `roles/accesscontextmanager.policyReader`).
6. **Deployer Permissions**: Grants the engineer deployer roles on the project to build and deploy Cloud Run.

---

## Client Execution Instructions (via Cloud Shell or Local Terminal)

### Option A: Running from GCP Cloud Shell (Easiest for Client)

1. Open [Google Cloud Shell](https://shell.cloud.google.com).
2. Upload this `first_steps` directory or clone the repository:
   ```bash
   git clone https://github.com/g-jsaccomani/agentic_grc_certifications.git
   cd agentic_grc_certifications/terraform/first_steps
   ```
3. Copy the example variables:
   ```bash
   cp terraform.tfvars.example terraform.tfvars
   ```
4. Edit `terraform.tfvars` if needed (adjust `org_id`, `billing_account`, or `deployer_email`).
5. Initialize and apply:
   ```bash
   terraform init
   terraform apply
   ```
6. Send the resulting output (`project_id`) back to the implementation engineer.

---

### Option B: Running from Local Workstation

```bash
cd terraform/first_steps
cp terraform.tfvars.example terraform.tfvars
terraform init
terraform plan
terraform apply
```

---

## Post-Provisioning Step for the Implementation Engineer

Once the client runs `terraform apply`:
1. The client shares the generated `project_id`.
2. The engineer authenticates:
   ```bash
   gcloud auth login
   gcloud auth application-default login
   ```
3. The engineer navigates to the project and runs `make journey`:
   ```bash
   cd "/Users/jsaccomani/Documents/Jetsky/My Projects/agentic_grc_certifications"
   export PROJECT_ID="<OUTPUT_PROJECT_ID>"
   export REGION="us-central1"
   make journey
   ```
