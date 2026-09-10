# Agentic Compliance Readiness Accelerator (GEAP)

[![CI/CD](https://github.com/g-jsaccomani/agentic_grc_certifications/actions/workflows/deploy.yml/badge.svg)](https://github.com/g-jsaccomani/agentic_grc_certifications/actions)
[![Python 3.12](https://img.shields.io/badge/python-3.12-blue.svg)](https://www.python.org/downloads/)
[![Standard](https://img.shields.io/badge/Standard-ISO%2FIEC%2027001%3A2022-green.svg)](https://www.iso.org/standard/27001)
[![Amendment](https://img.shields.io/badge/Climate%20Action-Amd%201%3A2024-emerald.svg)](https://www.iso.org/)
[![Tests](https://img.shields.io/badge/Tests-223%20Passed-brightgreen.svg)](tests/)
[![Coverage](https://img.shields.io/badge/Coverage-92%25-success.svg)](tests/)
[![FinOps](https://img.shields.io/badge/FinOps-Token%20%26%20Cost%20Tracking-81c995.svg)](mcp_server_grc/finops.py)
[![Cloud Run](https://img.shields.io/badge/Cloud%20Run-Live%20Portal-4285F4.svg)](https://mcp-server-grc-938078169010.us-central1.run.app/portal)

An enterprise-grade, autonomous multi-agent orchestration framework designed for continuous security posture assessment, automated evidence collection, policy validation, and proactive compliance readiness. Built natively for the **Gemini Enterprise Agent Platform (GEAP)**—integrating deeply with Google Cloud Platform (GCP) security infrastructure, Zero-Trust network boundaries, and StreamableHTTP Model Context Protocol (MCP) servers.

Directly maps live cloud telemetry and organizational policies to **ISO/IEC 27001:2022** (all 93 controls), the **Amd 1:2024 Climate Action Amendment**, and emerging AI governance baselines.

> [!IMPORTANT]
> **Legal & Compliance Disclaimer**:  
> **Google Cloud does not conduct formal audits or issue compliance certifications.**  
> The Agentic Compliance Readiness Accelerator is an advisory, assessment, and evidence readiness framework. It automates technical evidence collection, analyzes security configurations, and identifies posture gaps to assist organizations in preparing for independent, accredited third-party certification audits.

> **Live Production Portal**: Access the web-based interactive readiness console at [https://mcp-server-grc-938078169010.us-central1.run.app/portal](https://mcp-server-grc-938078169010.us-central1.run.app/portal)
> 
> **Documentation Hub**: See [documentation/](documentation/) for complete technical specifications, architecture blueprints, and operations runbooks.
>
> **Deployment Guide**: See [documentation/operations/README.md](documentation/operations/README.md) for step-by-step instructions on provisioning the GCP Organization folder, project, and deploying the service with `make journey`.
>
> **Multi-Framework Roadmap**: See [documentation/roadmap/README.md](documentation/roadmap/README.md) for upcoming support for SOC 2 Type II, PCI-DSS v4.0, NIST CSF 2.0, LGPD/GDPR, and pre-deploy/pre-access selection mechanisms.

---

## 1. Key Architectural Pillars (GEAP)

### I. Complementary Operating Environments
1. **Interactive Web Portal (`/portal`)**:
   - Google Cloud-style web dashboard for CISOs, security directors, and compliance readiness teams.
   - Real-time **Compliance & Security Advisor** with streaming dossiers and specialized subagent delegation.
   - Autonomous **4-Phase Readiness Pipeline** (Asset Discovery, Deep Technical Review, Zero-Copy Governance, Formal Opinion & Sealing).
   - Interactive **ISO 27001 Matrix** covering all 93 controls across Organizational (A.5), People (A.6), Physical (A.7), and Technological (A.8) themes.
   - **Dual Reporting Suite**: Instant toggle between **Executive Dossier (C-Level)** and **Technical Assessment Dossier (ISO 27001 Stage 2 Readiness)** with official print-ready PDF, structured JSON, and Markdown export.
2. **Agent Development Kit - ADK v1.0 (Code-First)**:
   - Python ADK for deep enterprise customization and programmable compliance readiness pipelines.
   - Orchestrates a modular execution graph composed of specialized, autonomous subagents.

### II. Secure Grounding with "Zero Copy" (Data)
Connects directly to enterprise repositories (**Google Drive, Microsoft SharePoint Online, Jira, Confluence, ServiceNow, Salesforce**):
- **Zero-Copy Architecture**: Enterprise policies, IaC files, risk matrices, and configuration logs are never duplicated or indexed into external search databases. The agent queries data in real-time at the source.
- **Identity & ACL Preservation**: Enforces corporate Identity Provider (IDP) access controls—queries require delegated user OAuth bearer tokens.
- **Total Privacy**: Prompts, compliance telemetry, and internal policies remain strictly confined within the customer's private cloud perimeter; customer data is **never** used to train Google base models.

### III. Persistent Assessment Memory & Evidence Graph (Scale)
- **Agent Platform AI Sessions**: Sustains multi-day and multi-week readiness workflows across certification review lifecycles.
- **Persistent Memory Bank**: Retains unresolved assessment findings from past sessions, tracking proven controls and open remediation items.
- **Temporal Drift Analysis**: Computes compliance velocity (`IMPROVING`, `STABLE`, `DEGRADING`) and flags recurring non-compliance hotspots.
- **Directed Evidence Graph**: Tracks cryptographic evidence nodes with SHA-256 hashes and epistemic tiers.

### IV. GCP Organization Scope & Multi-Project Selector
- Operates at the **GCP Organization Level** (`org_id: 108928374619`).
- Features a **retractable dropdown selector** in the UI sidebar allowing reviewers and assessors to dynamically toggle which organization projects are in active scope:
  - Discovers projects across GCP folders (`Core-Workloads`, `Data-Platform`, `Operations/FinOps`, `Security-Perimeter`).
  - Single-click inclusion/exclusion, search filtering, and quick actions ("Select All", "Prod Only").

### V. FinOps & AI Token Cost Management
- Real-time token consumption telemetry (Prompt Tokens, Context Caching, Output Tokens).
- Real-time cost computation in **USD ($)** and **BRL (R$)** using official Google Cloud Vertex AI / Gemini rates.
- **Gemini Context Caching Savings**: Calculates financial ROI from zero-copy evidence caching (achieving up to ~73% cache hit ratio and drastic token savings).
- Granular breakdown per agent/subagent and assessment phase.

### VI. Governance & Agent Self-Defense (Govern)
- **Agent Cryptographic Identity (SPIFFE)**: Each subagent runs with a verifiable SPIFFE ID (`spiffe://grc.jetsky.gcp/ns/production/sa/...`) bound to GCP IAM least privilege.
- **Agent Gateway & Model Armor**: Ingress inspection blocks prompt injections and redacts PII; Egress inspection redacts secrets, keys, and enforces a strict domain allowlist to prevent data exfiltration.
- **Human-in-the-Loop (HITL) Gate**: All remediation plans are validated in an isolated sandbox (`SANDBOX_DRY_RUN`). Applying changes to production requires an authenticated human approval token (`HITL-APPROVED-...`).

### VII. Dual Reporting Suite & Assessment Deliverables
- **Executive Dossier (C-Level)**: High-level executive scorecard, quantitative domain breakdown, FinOps ROI, and strategic compliance posture for executive leadership and boards.
- **Technical Assessment Dossier (ISO/IEC 27001:2022 Stage 2 Readiness)**:
  - Full Statement of Applicability (SoA v2022.4) with normative clause mappings.
  - Verifiable technical evidence blocks with real Google Cloud CLI (`gcloud`) outputs and policy inspection (Cloud KMS HSM FIPS 140-2, VPC-SC, Cloud DLP, Cloud Armor, IAM Least Privilege, Binary Authorization).
  - Corrective & Preventive Action (CAPA) register with automated remediation tracking and HITL approval tokens.
  - Merkle Root Hash and SHA-256 cryptographic sealing conforming to RFC 3161 digital evidence trail standards.
  - Triple-format exports: Official A4 print-ready PDF, structured machine-readable JSON (compatible with Archer, ServiceNow, Vanta, Drata), and Markdown.

### VIII. Global Localization & Multilingual Architecture (i18n)
- **Default International Language**: The platform defaults to **English (`en`)** across all UI controls, reports, prompts, and assessment models.
- **Multi-Language Support**: Users can toggle between **English (`en`)**, **Portuguese (`pt`)**, and **Spanish (`es`)** via the top navigation bar with `localStorage` persistence.
- **Full UI & AI Reasoning Localization**:
  - Dynamically localizes sidebar navigation, action buttons, prompt chips, and document viewer toolbars.
  - Propagates target `locale` to Vertex AI Gemini and specialized subagents, formulating technical findings, evidence dossiers, and executive opinions in the selected language.

---

## 2. ISO/IEC 27001:2022 Controls Mapping (93 Controls)

The platform implements the complete 2022 taxonomy across 4 themes:

| Theme | Controls | Scope & Highlights | Lead Subagent |
| :--- | :--- | :--- | :--- |
| **A.5 Organizational Controls** | 37 controls | Information security policies, governance, roles, segregation of duties, supplier relationships (A.5.23), incident management (A.5.24-28). | `AnnexASubAgent` / `OrgPoliciesSubAgent` |
| **A.6 People Controls** | 8 controls | Background screening (A.6.1), contractual terms, security awareness and education (A.6.3), offboarding processes (A.6.5). | `AnnexASubAgent` (HR Specialist) |
| **A.7 Physical Controls** | 14 controls | Physical security perimeters (A.7.1), entry controls, office security, environmental threat protection (A.7.5). | `AnnexASubAgent` (Physical Sec) |
| **A.8 Technological Controls** | 34 controls | IAM and MFA (A.8.5), cryptography and Cloud KMS (A.8.24), secure development lifecycle (A.8.25/28), DLP and VPC-SC (A.8.12), logging and monitoring (A.8.16). | `GCPTelemetrySubAgent` / `AnnexASubAgent` |
| **Amd 1:2024** | Climate Action | Multi-region resilience, geographical redundancy, Disaster Recovery, and business continuity plans. | `climate_resilience.py` |

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
│  - Reasoning Engine: Gemini 2.5 Pro (Lead Advisor) / Gemini 2.5 Flash (Subagents)          │
│  - FinOps Engine: Real-time token metering, Vertex AI pricing, Context Caching ROI       │
│  - Persistent Memory: Memory Bank (Drift Velocity, AI Sessions, Historical Evidence)      │
│  - Evidence Graph: Directed Graph with SHA-256 Hashed Nodes & Epistemic Verification      │
│  - Remediation Engine: Sandbox Dry-Run Validation + Zero-Trust HITL Approval Gate         │
│                                                                                           │
│   ┌───────────────────────────────────────────────────────────────────────────────────┐   │
│   │                        Specialized Subagents Execution Graph                      │   │
│   │   [Annex A Specialist]   [GCP Telemetry Agent]   [Org Policies]   [Horizon]       │   │
│   │   [A.5 Org Subagent]     [A.6 People Subagent]   [A.7 Physical]   [A.8 Tech]      │   │
│   └───────────────────────────────────────────────────────────────────────────────────┘   │
└───────────────────────┬─────────────────────────────────────────────┬─────────────────────┘
                        │ Real-Time Queries (Zero-Copy)               │ Tool Invocations
                        ▼                                             ▼
┌───────────────────────────────────────────────┐ ┌─────────────────────────────────────────┐
│        Zero-Copy Enterprise Connectors        │ │      Agent Gateway & Model Armor        │
│ - Google Drive       - SharePoint Online      │ │ (Egress Secret Redaction & URL Filter)  │
│ - Jira               - Confluence             │ └───────────────────┬─────────────────────┘
│ - ServiceNow         - Salesforce             │                     │ StreamableHTTP
│ - GitHub Repositories                         │                     ▼
└───────────────────────────────────────────────┘ ┌─────────────────────────────────────────┐
                                                  │             MCP Server GRC              │
                                                  │  - Web Portal (/portal) & API Endpoints │
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
│   ├── agent.py                        # Core Orchestrator ADK v1.0
│   ├── continuous_intelligence.py      # Proactive Assessment & Implementation Engine
│   ├── evidence_graph.py               # Evidence Graph with SHA-256 Hashing & Tiers
│   ├── memory_bank.py                  # Persistent Memory Bank & Temporal Drift Analysis
│   ├── remediation_engine.py           # Sandbox Remediation Engine with HITL Gate
│   ├── zero_copy_connector.py          # Zero-Copy Enterprise Connectors (Drive, Jira, etc.)
│   ├── gateway.py                      # Model Armor Ingress/Egress & SPIFFE Gateway
│   ├── a2a_client.py                   # Agent2Agent (A2A) Discovery Client
│   └── subagents/
│       ├── __init__.py
│       ├── annex_a_agent.py            # ISO 27001 Annex A Specialist
│       ├── gcp_telemetry_agent.py      # GCP Infrastructure & Telemetry Specialist
│       ├── org_policies_agent.py       # Corporate Policy & Governance Specialist
│       └── horizon_scanner_agent.py    # Horizon Scanning (Deep Research) Specialist
├── mcp_server_grc/
│   ├── __init__.py
│   ├── server.py                       # StreamableHTTP MCP Server (FastAPI)
│   ├── portal.py                       # Web Portal API Routes, Scopes & Assessment Engine
│   ├── portal_html.py                  # Single-Page Application Portal (Google Cloud-style)
│   ├── catalog.py                      # 93 ISO 27001 Controls & Organization Projects
│   ├── questionnaire.py                # Questionnaire Engine, Evidence Linking & Auto-Sync
│   ├── questionnaire_catalog.py        # 93-Control Questionnaire & Inspection Guidance
│   ├── finops.py                       # FinOps Engine: Token & Cost Telemetry (USD/BRL)
│   ├── schema.json                     # Declarative MCP Tools Schema
│   └── tools/
│       ├── __init__.py
│       ├── cloud_security.py           # Control A.5.23 Assessor
│       ├── iac_scanner.py              # Control A.8.9 IaC Analyzer (Terraform/Ansible)
│       ├── data_leakage_prevention.py  # Control A.8.12 DLP & VPC-SC Assessor
│       ├── monitoring.py               # Control A.8.16 Logging & Monitoring Assessor
│       ├── threat_intel.py             # Control A.5.7 Threat Intelligence Correlator
│       └── climate_resilience.py       # Amd 1:2024 Climate Resilience Assessor
├── terraform/
│   └── first_steps/                    # Terraform Bootstrap for Client GCP Environment
├── tests/                              # 223 Automated Tests (Unit, Integration & Guardrails)
├── documentation/                      # Central Enterprise Documentation Hub
│   ├── blueprint/                      # Technical Architecture Blueprint
│   ├── guardrails/                     # Model Armor & Guardrails Specification
│   ├── poc/                            # Proof of Concept Runbook, Specs & Scripts
│   ├── operations/                     # Deployment & Operations Manual
│   ├── roadmap/                        # Strategic Evolution & Multi-Framework Roadmap
│   └── build/                          # Makefile & Developer Workflow Automation
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

### Run Full Test Suite (223 Tests, 100% Passing)
```bash
uv run pytest
```

### Run Web Portal & MCP Server Locally
```bash
export ALLOW_DEV_AUTH_BYPASS="true"
.venv/bin/python -m uvicorn mcp_server_grc.server:app --host 0.0.0.0 --port 8080 --reload
```
Access the interactive console at `http://localhost:8080/portal`.

---

## 6. Strategic Roadmap

Detailed architecture and strategic pillars are maintained in [ROADMAP.md](ROADMAP.md):

- **In Progress**: **Interactive ISO Assessment Questionnaires & Evidence Attachment** — structured interview workflows, evidence upload with SHA-256 anchoring, AI evaluation, and real-time report/metric updates.
- **In Progress**: **Multi-Cloud Connectors (AWS & Azure)** — zero-key telemetry ingestion via OIDC federation and unified control abstraction (KMS, Storage, IAM, Network).
- **Next Cycle**: **CodeMender** — autonomous vulnerability remediation in code repositories (ISO Control A.8.28) with ephemeral container sandbox validation.
- **Planned / Future Vision**: **Multi-Framework Expansion & OCI** — Oracle Cloud (OCI), SOC 2 Type II, PCI-DSS v4.0, NIST CSF 2.0, LGPD/GDPR, and unified cross-mapping engine ("Collect Once, Comply Many").

---

## 7. License & Standards

- **Standards Reference**: [ISO/IEC 27001:2022](https://www.iso.org/standard/27001) & [ISO/IEC 27001:2022/Amd 1:2024](https://www.iso.org/)
- **License**: Apache 2.0
