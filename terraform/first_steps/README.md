# First Steps: GCP Bootstrap via Terraform

This configuration provisions the initial Google Cloud Platform (GCP) resources required for the Agentic GRC platform:
- Dedicated Folder: `fldr-agentic-grc` under the organization.
- Host Project: `agentic-grc-xxxx` inside the folder.
- Billing Account association.
- 16 required Cloud APIs (Cloud Run, Model Armor, Cloud Asset, SCC, KMS, BigQuery, Vertex AI, Discovery Engine, etc.).
- Auditor Service Account (`sa-agentic-grc-auditor`) with organization-wide read privileges.
- Deployer permissions on the project for the implementation engineer.

---

## Instructions for Non-Technical Clients (Zero-Git / One-Command)

If the client has never used Git or downloaded repositories in GCP, send them the following template:

```text
To prepare your Google Cloud environment, please follow these 3 steps:

1. Open Google Cloud Shell in your browser:
   https://shell.cloud.google.com

2. In the terminal window that appears at the bottom of the screen, paste this single command and press Enter:
   curl -sSL https://raw.githubusercontent.com/g-jsaccomani/agentic_grc_certifications/main/terraform/first_steps/bootstrap.sh | bash

3. The script will automatically detect your Organization ID and Billing Account, create the folder and project, and configure the security auditor permissions.
   When finished, it will display:
   PROJECT_ID: agentic-grc-xxxx

   Please copy that line and send it back to us. We will take care of the rest of the deployment!
```

---

## Alternative: Direct Cloud Shell Link (1-Click)

Clicking this link opens Cloud Shell, automatically clones the repository, and navigates directly into this directory:

[Open in Google Cloud Shell](https://shell.cloud.google.com/?cloudshell_git_repo=https://github.com/g-jsaccomani/agentic_grc_certifications.git&cloudshell_working_dir=terraform/first_steps)

Once the terminal loads, run:
```bash
./bootstrap.sh
```

---

## Alternative: Manual Terraform Execution (For Technical Administrators)

```bash
cd terraform/first_steps
cp terraform.tfvars.example terraform.tfvars
# Adjust variables if needed
terraform init
terraform apply
```

---

## Post-Provisioning Step for the Implementation Engineer

Once the client sends back the `PROJECT_ID`:

```bash
# 1. Authenticate locally
gcloud auth login
gcloud auth application-default login

# 2. Navigate to the repository
cd "/Users/jsaccomani/Documents/Jetsky/My Projects/agentic_grc_certifications"

# 3. Export variables and deploy
export PROJECT_ID="<OUTPUT_PROJECT_ID>"
export REGION="us-central1"
make journey
```
