# Proof of Concept (POC) Utility & Automation Scripts

> **Purpose**: Standalone scripts to verify, audit, test, and safely tear down the Google Cloud Security & Agentic GRC POC environment.  
> **Target Framework**: ISO/IEC 27001:2022  
> **Language**: English

---

## Script Catalog

| Script | Type | Purpose | How to Run |
| :--- | :--- | :--- | :--- |
| **[`verify_poc_environment.py`](./verify_poc_environment.py)** | Python | Audits 26 live Google Cloud assets across 4 lab projects (`fnlab-apps-8fa913`, `fnlab-ai-data-8fa913`, `fnlab-sec-mgmt-8fa913`, and `aispr-core-1cab11`). Confirms ~30% compliant / ~70% baseline non-compliant detection accuracy. | `python POC/scripts/verify_poc_environment.py` |
| **[`poc_live_audit.py`](./poc_live_audit.py)** | Python | Runs an end-to-end standalone audit session directly through the Cloud Inspector and Continuous Intelligence engine, printing detailed control findings. | `python POC/scripts/poc_live_audit.py` |
| **[`smoke_test.py`](./smoke_test.py)** | Python | Performs live HTTP health checks against the deployed Cloud Run service to verify that the audit portal and API endpoints are responsive. | `python POC/scripts/smoke_test.py --url <RUN_URL>` |
| **[`cleanup_poc_resources.sh`](./cleanup_poc_resources.sh)** | Bash | Safely destroys demo GCS buckets, removes firewall rules, destroys KMS key versions, and removes demo service accounts created for the POC. | `./POC/scripts/cleanup_poc_resources.sh [--dry-run]` |

---

## Execution Prerequisites

1. Active Google Cloud SDK authentication:
   ```bash
   gcloud auth application-default login
   ```
2. Python virtual environment activated with project dependencies:
   ```bash
   source .venv/bin/activate
   ```
