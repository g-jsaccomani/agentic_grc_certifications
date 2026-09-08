# Strategic Roadmap — Agentic GRC Platform
## Continuous Compliance, Multi-Framework Automation & Multi-Cloud Governance

> **Platform**: Gemini Enterprise Agent Platform (GEAP) & Google Cloud Security  
> **Status**: Active Product & Engineering Roadmap  
> **Scope Boundary**: This platform performs continuous audit, automated evidence collection, and remediation recommendations; it does not directly modify client code or mutate infrastructure.  
> **Language**: English

---

## 1. Evolution Phases & Strategic Milestones

| Milestone / Initiative | Primary Focus | Key Deliverables | Status |
| :--- | :--- | :--- | :--- |
| **Foundation Complete** | **ISO 27001:2022 (GCP)** | All 93 controls, MCP server, 4 autonomous phases, SHA-256 Evidence Graph, C-Level Executive Dossier, and Stage 2 External Audit Report (PDF/JSON). | Completed |
| **Interactivity & Governance** | **ISO Questionnaires & Evidence** | Structured audit questionnaires, drag-and-drop evidence upload with SHA-256 anchoring, Gemini 2.5 AI consistency validation, and real-time score recalculation. | In Progress |
| **Hybrid Telemetry** | **Multi-Cloud Connectors (AWS & Azure)** | Ingestion of AWS and Azure telemetry via OIDC Workload Identity Federation (Zero-Key), unified control abstraction (KMS, Storage, IAM, Network). | In Progress |
| **Enterprise Cloud & B2B Frameworks** | **OCI & SOC 2 / PCI-DSS** | Oracle Cloud Infrastructure (OCI) connector, certification onboarding wizard (Pre-deploy / Pre-access), SOC 2 Type II and PCI-DSS v4.0 catalogs. | Backlog |
| **Global 360 Compliance** | **NIST CSF & Privacy (GDPR/LGPD)** | NIST CSF 2.0, Cloud DLP privacy data mapping, cross-correlation engine (*Collect Once, Comply Many*), and continuous multi-cloud auditing. | Future Vision |

---

## 2. Strategic Evolution Pillars

```
                   +-------------------------------------------------------------+
                   |             AGENTIC GRC UNIFIED PLATFORM                    |
                   +------------------------------+------------------------------+
                                                  |
                     +----------------------------+----------------------------+
                     |                            |                            |
                     v                            v                            v
            +-----------------+          +-----------------+          +-----------------+
            | PILLAR 1        |          | PILLAR 2        |          | PILLAR 3        |
            | Questionnaires &|          | Multi-Cloud     |          | Multi-Framework |
            | ISO Evidence    |          | Connectors      |          | Expansion       |
            | (HITL + Metrics)|          | (AWS/Azure/OCI) |          | (SOC2/PCI/NIST) |
            +-----------------+          +-----------------+          +-----------------+
```

---

### Pillar 1: ISO Audit Questionnaires & Evidence Attachments

Addresses organizational controls (A.5), people controls (A.6), and governance clauses (4 to 10) requiring human attestation and documentary verification:

- **Structured Normative Questions**:
  - Interactive evaluation matrix for all 93 ISO 27001 controls with formal acceptance criteria.
- **Evidence Upload with SHA-256 Integrity**:
  - Direct drag-and-drop ingestion of policy documents (PDF), meeting minutes, reports, and architecture diagrams.
  - Deterministic cryptographic hashing (SHA-256) calculated at upload time and anchored directly to the Evidence Graph.
- **Multimodal Consistency Analysis via Gemini 2.5**:
  - AI-driven validation checking alignment between written explanations and uploaded documentary evidence.
  - Formal classifications: *Consistent*, *Partial*, *Inconsistent*, *No Evidence*.
- **Immediate Cascading Recalculation**:
  - Instant scorecard updates for global compliance percentage.
  - Real-time refresh of the C-Level Executive Dossier.
  - Automatic injection of evidence receipts into the Stage 2 External Technical Audit Report (Print-ready A4 PDF / JSON / Markdown).

---

### Pillar 2: Multi-Cloud Connectors & Telemetry (AWS, Azure, OCI)

Unifies security posture management and continuous compliance for multi-cloud enterprise architectures:

- **OIDC Identity Federation (Zero-Key Principle)**:
  - Eliminates static credentials using Google Cloud Workload Identity Federation to assume temporary, scoped roles in AWS IAM, Microsoft Entra ID, and OCI IAM.
- **Native Cloud Service Connectors**:
  - **AWS**: Security Hub, AWS Config, IAM Access Analyzer, CloudTrail, KMS, S3.
  - **Microsoft Azure**: Microsoft Defender for Cloud, Azure Policy, Entra ID, Key Vault, Network Security Groups (NSGs), Blob Storage.
  - **Oracle Cloud (OCI)**: Cloud Guard, Security Zones, OCI Vault, VCN Security Lists, Object Storage.
- **Agnostic Control Abstraction Layer**:
  - Normalizes multi-cloud resources to ISO 27001 Annex A controls:
    - *Cryptography (A.8.24)*: Google Cloud KMS = AWS KMS = Azure Key Vault = OCI Vault.
    - *Network Security (A.8.20)*: GCP Compute Firewalls = AWS Security Groups = Azure NSGs = OCI Security Lists.
    - *Data Leakage Prevention (A.8.12)*: GCS = AWS S3 = Azure Blob Storage = OCI Object Storage.
- **Portal Unified & Provider-Specific Views**:
  - Toggle between single-cloud perimeters (`GCP`, `AWS`, `Azure`, `OCI`) and the **Global Consolidated Compliance Posture**.

---

### Pillar 3: Multi-Framework Expansion & Cross-Mapping

Transforms the audit engine into an enterprise multi-normative platform with evidentiary reuse (*Collect Once, Comply Many*):

- **Target Regulatory Frameworks**:
  - **SOC 2 Type II**: Trust Services Criteria (CC1 to CC9), Availability, and Confidentiality.
  - **PCI-DSS v4.0**: Cardholder Data Environment (CDE), tokenization, firewall boundaries, and encryption of cardholder data.
  - **NIST CSF 2.0 & SP 800-53 Rev. 5**: Govern, Identify, Protect, Detect, Respond, and Recover categories.
  - **Privacy Regulations (GDPR / LGPD)**: PII discovery via Cloud DLP and automated Records of Processing Activities (ROPA).
- **Framework Selection Architecture**:
  - **Pre-Deployment**: Declarative activation via Terraform configuration (`terraform.tfvars`) or Cloud Run environment variables (`ACTIVE_FRAMEWORKS`).
  - **Runtime & Pre-Access**: Workspace switcher in the portal header and self-service compliance onboarding wizard.
- **Cross-Framework Evidence Reusability**:
  - A single technical telemetry collector (e.g., KMS automatic key rotation) simultaneously satisfies ISO 27001 (A.8.24), SOC 2 (CC6.1), PCI-DSS (3.5.1), and NIST CSF (PR.DS-01), delivering up to 80% token savings through Gemini Context Caching.

---

## 3. Implementation Percentage by Pillar

| Initiative / Pillar | Estimated Completion | Status & Scope Gap Analysis (Real vs. Missing) |
| :--- | :---: | :--- |
| **Foundation (ISO 27001 / GCP)** | **90%** | Live Cloud KMS, Cloud Storage, IAM, and Cloud Run security inspections are fully implemented; live Firewall and Compute Engine deep inspection remain pending. |
| **Pillar 1 (Questionnaires & Evidence)** | **90%** | Interactive 93-control questionnaire, drag-and-drop evidence uploads, SHA-256 graph anchoring, and AI consistency analysis are operational; formal report Methodology and Auditor Responsibility sections remain pending. |
| **Pillar 2 (Multi-Cloud Connectors)** | **5%** | OIDC federation architecture and control abstraction schemas are specified, but zero real connectors for AWS, Azure, or OCI are implemented. |
| **Pillar 3 (Multi-Framework Expansion)** | **15%** | A pilot SOC 2 catalog covering 5 controls is implemented; no catalogs currently exist for PCI-DSS, NIST CSF 2.0, or GDPR/LGPD. |

---

## 4. Prioritization Matrix

```
                  HIGH IMPACT
                       ^
                       |   [Pillar 1] ISO Questionnaires & Evidence
                       |   [Pillar 2] Multi-Cloud Connectors (AWS/Azure)
                       |   
                       |   [Pillar 3] SOC 2 Type II & PCI-DSS
                       |   
                       |   [Pillar 3] NIST CSF 2.0 & OCI Connector
                       |   [Pillar 3] GDPR / LGPD Privacy Automation
                       +------------------------------------------>
                      LOW                             HIGH
                                  COMPLEXITY
```

---

## 5. Engineering Guidelines & Definition of Done (DoD)

Before any roadmap feature is released to production:

1. **Zero Static Credentials**: All cloud integrations must strictly employ OIDC Workload Identity Federation.
2. **Active Model Armor Guardrails**: Every new agent prompt and completion must pass through injection filtering, PII redaction, and anti-hallucination validation.
3. **Cryptographic Proof Chain**: All collected or uploaded evidence must be hashed with SHA-256 and anchored to the epistemic Evidence Graph.
4. **Automated Report Propagation**: New findings must immediately update both the C-Level Executive Dossier and the Stage 2 External Technical Audit Report.
5. **Continuous Quality Gate**: Minimum of 90% test coverage with automated unit, integration, and guardrail tests passing in CI/CD (`pytest tests/`).
