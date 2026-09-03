# Project Agentic GRC: AI Agent for Automated GRC & ISO 27001 Compliance Auditing

[![CI/CD](https://github.com/g-jsaccomani/agentic_grc_certifications/actions/workflows/deploy.yml/badge.svg)](https://github.com/g-jsaccomani/agentic_grc_certifications/actions)
[![Python 3.12](https://img.shields.io/badge/python-3.12-blue.svg)](https://www.python.org/downloads/)
[![Standard](https://img.shields.io/badge/Standard-ISO%2FIEC%2027001%3A2022-green.svg)](https://www.iso.org/standard/27001)
[![Amendment](https://img.shields.io/badge/Climate%20Action-Amd%201%3A2024-emerald.svg)](https://www.iso.org/)

An intelligent multi-agent orchestration framework designed for continuous auditing, automated evidence collection, and verification of multi-cloud infrastructure configurations and organizational policy documents. Directly maps technical states to **ISO/IEC 27001:2022** requirements and the **Amd 1:2024 Climate Action Amendment**.

Built for the **Google Cloud Platform (GCP)** utilizing the **Gemini Enterprise Agent Platform (GEAP)**, **Vertex AI Reasoning Engines**, **Cloud Run StreamableHTTP MCP**, and **Model Armor** safety guardrails.

---

## 1. Core Compliance Use Cases (ISO/IEC 27001:2022)

1. **Continuous Cloud Security Audit (Control A.5.23)**:
   - Evaluates storage buckets (Public Access Prevention, Uniform Bucket-Level Access, CMEK encryption).
   - Validates Cloud KMS key rotation periods (<= 90 days baseline) and protection levels (HSM vs. SOFTWARE).
   - Audits Cloud Firewalls and VPC perimeters for unauthenticated 0.0.0.0/0 ingress on sensitive ports (SSH 22, RDP 3389, databases).
   - Flags primitive IAM roles (`roles/owner`, `roles/editor`) granted to individual users.

2. **Infrastructure-as-Code (IaC) Scanning (Control A.8.9)**:
   - Static analysis of Terraform (`.tf`) and Ansible (`.yml`) code within CI/CD pipelines.
   - Detects misconfigurations, public ACLs, open CIDRs, and hardcoded credentials before deployment.

3. **Active Threat Intelligence Audit (Control A.5.7)**:
   - Audits Cloud Logging trails routed to BigQuery.
   - Correlates telemetry against active threat intelligence feeds from **Google SecOps (Chronicle)** and **Mandiant** to verify active monitoring compliance.

4. **Climate Resilience and Disaster Recovery Audit (Amd 1:2024)**:
   - Evaluates Clauses 4.1 & 4.2 context requirements.
   - Audits multi-region geographic distribution, storage redundancy (dual-region/multi-region), automated failover, and extreme weather continuity resilience.

---

## 2. Architecture & The Iron Triangle

```
User (Gemini Enterprise)
           │
           ▼
┌─────────────────────────────────────────────────────────┐
│                      AGENT GATEWAY                      │
│  ┌───────────────────────────────────────────────────┐  │
│  │ Model Armor (Ingress)                             │  │
│  │ - Prompt Injection / Jailbreak Blocker            │  │
│  │ - PII Redaction / Masking                         │  │
│  │ - User ID Token Validation                        │  │
│  └───────────────────────────────────────────────────┘  │
└──────────────────────────┬──────────────────────────────┘
                           │ Sanitized Prompt
                           ▼
┌─────────────────────────────────────────────────────────┐
│                  AGENT RUNTIME (GEAP)                   │
│  - SPIFFE Identity: spiffe://grc.jetsky.gcp/ns/...      │
│  - Reasoning Core: Gemini 3.7 Flash                     │
│  - Memory Bank / State: Persistent Audit Sessions       │
└──────────────────────────┬──────────────────────────────┘
                           │ Tool Execution Call
                           ▼
┌─────────────────────────────────────────────────────────┐
│                      AGENT GATEWAY                      │
│  ┌───────────────────────────────────────────────────┐  │
│  │ Model Armor (Egress)                              │  │
│  │ - Secret / Key Leakage Redaction                  │  │
│  │ - Exfiltration / Malicious URI Blocker            │  │
│  └───────────────────────────────────────────────────┘  │
└──────────────┬───────────────────────────┬──────────────┘
               │ (StreamableHTTP)          │ (A2A Protocol)
               ▼                           ▼
┌──────────────────────────────┐  ┌───────────────────────────┐
│        MCP Server GRC        │  │     Wiz Sub-Agent (A2A)   │
│  - Cloud Security (A.5.23)   │  │  - Cloud Security Graph   │
│  - IaC Scanner (A.8.9)       │  │  - Toxic Combinations     │
│  - Threat Intel (A.5.7)      │  └───────────────────────────┘
│  - Climate Action (Amd 1:24) │
└──────────────────────────────┘
```

### The Iron Triangle Security Model
- **Agent Identity (SPIFFE)**: Cryptographic identity (`spiffe://grc.jetsky.gcp/ns/production/sa/grc-orchestrator`) bound to GCP IAM least privilege.
- **Agent Gateway**: Restricts egress traffic exclusively to authorized API endpoints.
- **Model Armor**: Inline safety filter inspecting both ingress (prompt injection, PII) and egress (secret leakage, exfiltration).

### Dual-Token Zero-Trust Transport
MCP requests over StreamableHTTP require dual tokens:
1. `X-Serverless-Authorization`: GCP Service Agent ID Token for Cloud Run ingress verification.
2. `Authorization`: Authenticated end-user OAuth Bearer token for fine-grained database/resource access.

---

## 3. Repository Structure

```
agentic_grc_certifications/
├── .github/
│   └── workflows/
│       └── deploy.yml          # CI/CD pipeline for Cloud Run & Agent Engine
├── agent_orchestrator/
│   ├── __init__.py
│   ├── agent.py                # Core Orchestrator ADK v1.0 (Gemini 3.7 Flash)
│   ├── gateway.py              # Model Armor Ingress/Egress & SPIFFE Gateway
│   ├── a2a_client.py           # Agent2Agent Discovery & Task Lifecycle Client
│   ├── requirements.txt        # Orchestrator dependencies
│   └── Dockerfile              # Container for Agent Engine
├── mcp_server_grc/
│   ├── __init__.py
│   ├── server.py               # StreamableHTTP MCP Server (FastAPI)
│   ├── schema.json             # Declarative tools JSON schema
│   ├── tools/
│   │   ├── __init__.py
│   │   ├── cloud_security.py   # Control A.5.23 auditor
│   │   ├── iac_scanner.py      # Control A.8.9 IaC analyzer (Terraform/Ansible)
│   │   ├── threat_intel.py     # Control A.5.7 threat correlation
│   │   └── climate_resilience.py # Amd 1:2024 resilience auditor
│   ├── requirements.txt        # Server dependencies
│   └── Dockerfile              # Container for Cloud Run
├── tests/
│   ├── test_mcp_server.py      # MCP endpoints & dual-token tests
│   ├── test_cloud_security.py  # Control A.5.23 test suite
│   ├── test_iac_scanner.py     # Control A.8.9 test suite
│   ├── test_threat_intel.py    # Control A.5.7 test suite
│   ├── test_climate_resilience.py # Amd 1:2024 test suite
│   └── test_gateway_and_agent.py  # Model Armor, SPIFFE, and Orchestrator tests
├── gcloud_setup.sh             # GCP environment provisioning script
├── Makefile                    # Developer shortcuts
└── requirements.txt            # Root project dependencies
```

---

## 4. Quick Start & Local Execution

### Prerequisites
- Python 3.12+
- `uv` (recommended) or `pip`
- Google Cloud SDK (`gcloud`)

### Setup Environment
```bash
# Clone or enter repository directory
cd "agentic_grc_certifications"

# Create virtual environment and install dependencies
uv venv
uv pip install -r requirements.txt --python .venv/bin/python
```

### Run Full Test Suite
```bash
# Run tests with coverage
.venv/bin/python -m pytest tests/ -v
```

### Start Local MCP Server
```bash
# Start StreamableHTTP server locally on port 8080
make run-mcp
# or:
.venv/bin/python -m uvicorn mcp_server_grc.server:app --host 0.0.0.0 --port 8080 --reload
```

---

## 5. Google Cloud Deployment

```bash
# 1. Initialize GCP APIs, Model Armor template, and IAM permissions
export PROJECT_ID="your-project-id"
export REGION="us-central1"
./gcloud_setup.sh

# 2. Deploy MCP Server to Cloud Run
gcloud run deploy mcp-server-grc \
  --source=./mcp_server_grc \
  --region=$REGION \
  --platform=managed \
  --no-allow-unauthenticated
```
