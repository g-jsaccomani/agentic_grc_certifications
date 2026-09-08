# Agentic GRC — Enterprise Documentation Hub

> **Practice**: Google Cloud Security • Continuous Compliance & Autonomous Governance  
> **Target Standard**: ISO/IEC 27001:2022 & ISO/IEC 27002:2022 (Annex A — All 93 Controls)  
> **Platform**: Gemini Enterprise Agent Platform (GEAP) & Google Cloud Run  
> **Language**: English

---

## 1. Documentation Organization

All documentation, architecture specifications, deployment guides, proof-of-concept runbooks, and build automation are organized into dedicated subdirectories:

| Directory | Module Name | Description | Target Audience |
| :--- | :--- | :--- | :--- |
| **[`blueprint/`](./blueprint/)** | **Architecture Blueprint** | Complete technical architecture, multi-agent orchestration specifications, Zero-Trust boundaries, SPIFFE identities, and data flows. | Enterprise Architects, Lead Engineers |
| **[`guardrails/`](./guardrails/)** | **Model Armor & Guardrails** | Ingress/egress perimeter defense, prompt injection prevention, PII redaction, anti-hallucination directives, and red-team test matrix. | Security Engineers, Compliance Officers |
| **[`poc/`](./poc/)** | **Proof of Concept (POC)** | Complete customer demonstration package: technical specification, 7-scene presentation runbook, setup guide, testing recipes, and runner scripts. | Solution Architects, Sales Engineers, Auditors |
| **[`operations/`](./operations/)** | **Operations & Deployment** | Two-phase enterprise deployment guide: Terraform identity bootstrap, Google Workspace OAuth 2.0, Cloud Run hosting, and monitoring. | DevOps Engineers, Platform Administrators |
| **[`roadmap/`](./roadmap/)** | **Strategic Roadmap** | Multi-framework expansion (SOC 2 Type II, PCI-DSS v4.0, NIST CSF), multi-cloud telemetry (AWS, Azure, OCI), and automated code remediation. | Product Managers, CISOs, Engineering Leads |
| **[`build/`](./build/)** | **Build & Automation** | Developer workflow shortcuts, Makefile targets, testing commands, and local virtual environment setup. | Software Engineers, QA Engineers |

---

## 2. Core Architecture Principles

1. **Deterministic Ground Truth**:
   Compliance states are evaluated by deterministic Python collectors querying live Google Cloud APIs, not by generative model assumption.
2. **Iron Triangle of Agentic Safety**:
   Every operation is bound by verifiable SPIFFE identities, Model Armor perimeter filtering, and an epistemic Directed Acyclic Graph (DAG) sealed with SHA-256 hashes.
3. **Continuous Compliance vs. Point-in-Time Audits**:
   Transforms periodic compliance into real-time posture awareness, automatically updating the 93 ISO 27001 controls and detecting configuration drift.
4. **Closed-Loop Remediation with Human-in-the-Loop (HITL)**:
   Idempotent cloud remediations are proposed by the system but strictly require authenticated human approval prior to mutation.

---

## 3. Quick Navigation

- **For Product Implementation & Deployment**: Follow the **[Product Implementation Guide](./poc/HOW_TO.md)**.
- **For Infrastructure Provisioning**: Follow the **[Operations Guide](./operations/README.md)**.
- **For Security & Red-Team Testing**: Review the **[Guardrails Specification](./guardrails/README.md)**.
- **For Product & Multi-Cloud Plans**: Check the **[Strategic Roadmap](./roadmap/README.md)**.
- **For Developer Commands**: Refer to the **[Build Automation Guide](./build/README.md)**.
