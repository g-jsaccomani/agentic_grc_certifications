# Agentic GRC: Autonomous AI Compliance Auditor & Implementer (GEAP)

[![CI/CD](https://github.com/g-jsaccomani/agentic_grc_certifications/actions/workflows/deploy.yml/badge.svg)](https://github.com/g-jsaccomani/agentic_grc_certifications/actions)
[![Python 3.12](https://img.shields.io/badge/python-3.12-blue.svg)](https://www.python.org/downloads/)
[![Standard](https://img.shields.io/badge/Standard-ISO%2FIEC%2027001%3A2022-green.svg)](https://www.iso.org/standard/27001)
[![Amendment](https://img.shields.io/badge/Climate%20Action-Amd%201%3A2024-emerald.svg)](https://www.iso.org/)
[![Tests](https://img.shields.io/badge/Tests-51%20Passed-brightgreen.svg)](tests/)
[![Coverage](https://img.shields.io/badge/Coverage-93%25-success.svg)](tests/)

An enterprise-grade, autonomous multi-agent orchestration framework designed for continuous auditing, automated evidence collection, policy validation, and persistent compliance remediation. Built natively for the **Gemini Enterprise Agent Platform (GEAP)**—the evolution of Vertex AI—integrating deeply with Google Cloud Platform (GCP) security infrastructure, Zero-Trust network boundaries, and StreamableHTTP Model Context Protocol (MCP) servers.

Directly maps live cloud telemetry and organizational policies to **ISO/IEC 27001:2022**, the **Amd 1:2024 Climate Action Amendment**, and emerging AI governance baselines.

> **Deployment Guide**: See [HOWTO.md](file:///Users/jsaccomani/Documents/Jetsky/My%20Projects/agentic_grc_certifications/HOWTO.md) for step-by-step instructions on provisioning the GCP Organization folder, project, and deploying the agent with `make provision-org` and `make journey`.

---

## 1. Key Architectural Pillars (GEAP)

### I. Complementary Operating Environments
1. **Agent Studio (Low-Code)**:
   - Visual modeling interface designed for CISO and GRC leadership.
   - Defines logical decision trees, compliance thresholds, audit frequencies, and business rules without requiring code.
2. **Agent Development Kit - ADK v1.0 (Code-First)**:
   - Export logic from Agent Studio into Python ADK for deep enterprise customization.
   - Orchestrates a modular execution graph composed of specialized, autonomous sub-agents.

### II. Secure Grounding with "Zero Copy" (Data)
Connects directly to enterprise repositories (**Google Drive, Microsoft SharePoint Online, Jira, Confluence, ServiceNow, Salesforce**):
- **Zero-Copy Architecture**: Enterprise policies, IaC files, risk matrices, and audit logs are never duplicated or indexed into external search databases. The agent queries data in real-time at the source.
- **Identity & ACL Preservation**: Enforces corporate Identity Provider (IDP) access controls—queries require delegated user OAuth bearer tokens.
- **Total Privacy**: Prompts, compliance telemetry, and internal policies remain strictly confined within the customer's private cloud perimeter; customer data is **never** used to train Google base models.

### III. Persistent Audit Memory (Scale)
- **Agent Platform AI Sessions**: Sustains multi-day and multi-week audit workflows across certification lifecycles.
- **Persistent Memory Bank**: Remembers unresolved audit findings from past sessions, tracking which controls (e.g. A.8.24 Cryptography or A.8.28 Secure Development) are already proven by cryptographic evidence and which remain open.
- **Temporal Drift Analysis**: Computes compliance velocity (`IMPROVING`, `STABLE`, `DEGRADING`) and flags recurring non-compliance hotspots ($\ge 50\%$ cycle failure rate).

### IV. Specialized Sub-Agent Execution Graph (Optimize)
The orchestrator coordinates specialized sub-agents running in parallel:
- **`AnnexASubAgent`**: Dedicated to ISO/IEC 27001:2022 Annex A technical & organizational controls (A.5.23, A.8.9, A.8.12, A.8.16, A.8.24, A.8.28).
- **`GCPTelemetrySubAgent`**: Extracts live infrastructure posture from Cloud Asset Inventory, BigQuery audit sinks, and VPC-SC.
- **`OrgPoliciesSubAgent`**: Cross-references documented corporate policies (via Zero-Copy) against live technical configurations to flag implementation gaps.
- **`HorizonScannerSubAgent` (Deep Research)**: Monitors regulatory portals (ISO, NIST, EU AI Act) for emerging changes, cross-references internal policies, and drafts policy amendments for human approval.

### V. Governance & Agent Self-Defense (Govern)
- **Agent Cryptographic Identity (SPIFFE)**: Each sub-agent runs with a verifiable SPIFFE ID (`spiffe://grc.jetsky.gcp/ns/production/sa/...`) bound to GCP IAM least privilege.
- **Agent Gateway & Model Armor**: Ingress inspection blocks prompt injections and redacts PII; Egress inspection redacts secrets, keys, and enforces a strict domain allowlist to prevent data exfiltration.
- **Human-in-the-Loop (HITL) Gate**: All remediation plans are validated in an isolated sandbox (`SANDBOX_DRY_RUN`). Applying changes to production requires an authenticated human approval token (`HITL-APPROVED-...`).

---

## 2. ISO/IEC 27001:2022 Controls Mapping

| Control | Description | Technical Requirement & Verification Criteria | Enforcement Tool / Sub-Agent |
| :--- | :--- | :--- | :--- |
| **A.5.23** | Information Security for Cloud Services | GCS Public Access Prevention (PAP), Uniform Bucket-Level Access (UBLA), Cloud KMS key rotation $\le 90$ days, no primitive IAM roles (`roles/owner`). | `cloud_security.py` |
| **A.8.9** | Configuration Management | Static analysis of Terraform & Ansible IaC; blocks open CIDR `0.0.0.0/0` on sensitive ports, requires strict SSH host key checking, prevents plaintext credentials. | `iac_scanner.py` |
| **A.8.12** | Data Leakage Prevention (DLP) | VPC Service Controls (VPC-SC) perimeters enforced; restricted core services (`storage`, `bigquery`); blocks wildcard `*` egress rules. | `data_leakage_prevention.py` |
| **A.8.16** | Monitoring Activities | Centralized log ingestion of Admin & Data Access audit trails into BigQuery or Google SecOps (Chronicle); retention $\ge 365$ days; automated security alerts. | `monitoring.py` |
| **A.8.24** | Use of Cryptography | Cryptographic key lifecycle, rotation $\le 90$ days for sensitive data, Hardware Security Module (HSM) protection level enforcement. | `annex_a_agent.py` |
| **A.8.28** | Secure Coding & Development | Mandatory automated SAST/DAST in CI/CD pipelines, branch protection rules, cryptographically signed commits. | `annex_a_agent.py` |
| **A.5.7** | Threat Intelligence | Ingestion and real-time correlation of Cloud Logging trails with Google SecOps / Mandiant threat intelligence indicators (IoCs). | `threat_intel.py` |
| **Amd 1:2024** | Climate Action (Clauses 4.1 & 4.2) | Multi-region geographic distribution, storage cross-region redundancy, automated failover, and climate disaster recovery resilience. | `climate_resilience.py` |

---

## 3. Architecture & Security Flow

```
                     ┌─────────────────────────────────────────────────────────┐
                     │               User (Gemini Enterprise)                  │
                     └────────────────────────────┬────────────────────────────┘
                                                  │
                                                  ▼
┌───────────────────────────────────────────────────────────────────────────────────────────┐
│                                       AGENT GATEWAY                                       │
│  ┌─────────────────────────────────────────────────────────────────────────────────────┐  │
│  │ Model Armor (Ingress)                                                               │  │
│  │ - Prompt Injection & Jailbreak Defense    - PII Tokenization & Redaction            │  │
│  │ - End-User OAuth Token Extraction         - SPIFFE ID Issuance                      │  │
│  └─────────────────────────────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────┬─────────────────────────────────────────────┘
                                              │ Sanitized Request
                                              ▼
┌───────────────────────────────────────────────────────────────────────────────────────────┐
│                                   AGENT RUNTIME (GEAP)                                    │
│  - Reasoning Engine: Gemini 3.7 Flash / Gemini 3.5 Pro                                    │
│  - Persistent Memory: Memory Bank (Drift Velocity, AI Sessions, Historical Evidence)      │
│  - Evidence Graph: Directed Graph with SHA-256 Hashed Nodes & Epistemic Verification      │
│  - Remediation Engine: Sandbox Dry-Run Validation + Zero-Trust HITL Approval Gate         │
│                                                                                           │
│   ┌───────────────────────────────────────────────────────────────────────────────────┐   │
│   │                        Specialized Sub-Agents Execution Graph                     │   │
│   │   [Annex A Agent]    [GCP Telemetry Agent]    [Org Policies]    [Horizon Scanner] │   │
│   └───────────────────────────────────────────────────────────────────────────────────┘   │
└───────────────────────┬─────────────────────────────────────────────┬─────────────────────┘
                        │ Real-Time Queries (Zero-Copy)               │ Tool Invocations
                        ▼                                             ▼
┌───────────────────────────────────────────────┐ ┌─────────────────────────────────────────┐
│        Zero-Copy Enterprise Connectors        │ │      Agent Gateway & Model Armor        │
│ - Google Drive       - SharePoint Online      │ │ (Egress Secret Redaction & URL Filter)  │
│ - Jira               - Confluence             │ └───────────────────┬─────────────────────┘
│ - ServiceNow         - Salesforce             │                     │ StreamableHTTP
└───────────────────────────────────────────────┘                     ▼
                                                  ┌─────────────────────────────────────────┐
                                                  │             MCP Server GRC              │
                                                  │  - A.5.23 Cloud Sec    - A.8.9 IaC      │
                                                  │  - A.8.12 DLP (VPC-SC) - A.8.16 Logging │
                                                  │  - A.5.7 Threat Intel  - Amd 1:2024 DR  │
                                                  └─────────────────────────────────────────┘
```

---

## 4. Repository Structure

```
agentic_grc_certifications/
├── .github/
│   └── workflows/
│       └── deploy.yml                  # CI/CD pipeline for Cloud Run & Agent Engine
├── agent_orchestrator/
│   ├── __init__.py                     # Module exports
│   ├── agent.py                        # Core Orchestrator ADK v1.0 (Gemini 3.7 Flash)
│   ├── continuous_intelligence.py      # Proactive Audit & Implementation Engine
│   ├── evidence_graph.py               # Evidence Graph with SHA-256 Hashing & Tiers
│   ├── memory_bank.py                  # Persistent Memory Bank & Temporal Drift Analysis
│   ├── remediation_engine.py           # Sandbox Remediation Engine with HITL Gate
│   ├── zero_copy_connector.py          # Zero-Copy Enterprise Connectors (Drive, Jira, etc.)
│   ├── gateway.py                      # Model Armor Ingress/Egress & SPIFFE Gateway
│   ├── a2a_client.py                   # Agent2Agent (A2A) Discovery Client
│   ├── subagents/
│   │   ├── __init__.py
│   │   ├── annex_a_agent.py            # ISO 27001 Annex A Specialist (A.8.24, A.8.28)
│   │   ├── gcp_telemetry_agent.py      # GCP Infrastructure & Telemetry Specialist
│   │   ├── org_policies_agent.py       # Corporate Policy & Governance Specialist
│   │   └── horizon_scanner_agent.py    # Horizon Scanning (Deep Research) Specialist
│   ├── requirements.txt
│   └── Dockerfile
├── mcp_server_grc/
│   ├── __init__.py
│   ├── server.py                       # StreamableHTTP MCP Server (FastAPI)
│   ├── schema.json                     # Declarative MCP Tools Schema
│   ├── tools/
│   │   ├── __init__.py
│   │   ├── cloud_security.py           # Control A.5.23 Auditor
│   │   ├── iac_scanner.py              # Control A.8.9 IaC Analyzer (Terraform/Ansible)
│   │   ├── data_leakage_prevention.py  # Control A.8.12 DLP & VPC-SC Auditor
│   │   ├── monitoring.py               # Control A.8.16 Logging & Monitoring Auditor
│   │   ├── threat_intel.py             # Control A.5.7 Threat Intelligence Correlator
│   │   └── climate_resilience.py       # Amd 1:2024 Climate Resilience Auditor
│   ├── requirements.txt
│   └── Dockerfile
├── tests/
│   ├── test_mcp_server.py              # Dual-Token & MCP endpoint tests
│   ├── test_cloud_security.py          # Control A.5.23 test suite
│   ├── test_iac_scanner.py             # Control A.8.9 test suite
│   ├── test_data_leakage_prevention.py # Control A.8.12 test suite
│   ├── test_monitoring.py              # Control A.8.16 test suite
│   ├── test_threat_intel.py            # Control A.5.7 test suite
│   ├── test_climate_resilience.py      # Amd 1:2024 test suite
│   ├── test_gateway_and_agent.py       # Model Armor, SPIFFE, and Orchestrator tests
│   ├── test_continuous_intelligence.py # Evidence Graph, Memory Bank, Remediation tests
│   └── test_subagents_and_zerocopy.py  # Sub-agents & Zero-Copy connector tests
├── ROADMAP.md                          # Product roadmap (including CodeMender backlog)
├── gcloud_setup.sh                     # GCP environment bootstrapping script
├── Makefile                            # Developer workflow shortcuts
└── requirements.txt                    # Unified development dependencies
```

---

## 5. Quick Start & Local Execution

### Prerequisites
- Python 3.12+
- `uv` (recommended) or `pip`
- Google Cloud SDK (`gcloud`)

### Setup Environment
```bash
# Clone repository and enter directory
git clone https://github.com/g-jsaccomani/agentic_grc_certifications.git
cd agentic_grc_certifications

# Create virtual environment and install dependencies
uv venv
uv pip install -r requirements.txt --python .venv/bin/python
```

### Run Full Test Suite (51 Tests, 93% Coverage)
```bash
# Run pytest with code coverage report
.venv/bin/python -m pytest tests/ -v --cov=agent_orchestrator --cov=mcp_server_grc --cov-report=term-missing
```

### Run StreamableHTTP MCP Server Locally
```bash
# Start local MCP server on port 8080 with development bypass enabled
export ALLOW_DEV_AUTH_BYPASS="true"
.venv/bin/python -m uvicorn mcp_server_grc.server:app --host 0.0.0.0 --port 8080 --reload
```

---

## 6. Proactive Audit Cycle Example

```python
from agent_orchestrator import ContinuousIntelligenceEngine

# Initialize the proactive engine inside the secure GEAP sandbox
ci_engine = ContinuousIntelligenceEngine(organization_name="Fintech-Enterprises")

# Assets to audit in the continuous cycle
cloud_assets = [
    {
        "target_control": "ISO/IEC 27001:2022 A.5.23",
        "resource_type": "gcs_bucket",
        "resource_id": "corporate-financial-records",
        "config": {"public_access_prevention": "enforced", "uniform_bucket_level_access": True},
        "verification_tier": "VERIFIED",
    },
    {
        "target_control": "ISO/IEC 27001:2022 A.8.12",
        "resource_type": "vpc_sc_perimeter",
        "resource_id": "accessPolicies/123/servicePerimeters/prod_perimeter",
        "config": {"enforced": True, "restricted_services": ["storage.googleapis.com", "bigquery.googleapis.com"]},
        "verification_tier": "VERIFIED",
    }
]

# Execute end-to-end continuous audit cycle
report = ci_engine.execute_proactive_audit_cycle(cycle_id="audit-cycle-001", cloud_assets=cloud_assets)

print(f"Overall Compliance Score: {report['scorecard']['overall_score']}% ({report['scorecard']['rating']})")
print(f"Drift Trajectory: {report['drift_trajectory']['trend']}")
print(f"Evidence Nodes in Graph: {report['evidence_graph_summary']['total_evidence_nodes']}")
```

---

## 7. Roadmap & Future Capabilities

Detailed planning is maintained in [ROADMAP.md](ROADMAP.md).

- **CodeMender (Control A.8.28)**: Autonomous vulnerability remediation engine for client code repositories. Discovers CVEs, simulates patches in ephemeral container sandboxes, and proposes pull requests with mandatory developer approval before production merges.
- **Agent Studio Web Interface**: Visual flow designer for GRC decision rules.
- **Jira Cloud Service Desk Integration**: Automated compliance ticket opening and remediation SLA tracking.

---

## 8. License & Standards

- **Standard Reference**: [ISO/IEC 27001:2022](https://www.iso.org/standard/27001) & [ISO/IEC 27001:2022/Amd 1:2024](https://www.iso.org/)
- **License**: Apache 2.0
