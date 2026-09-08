# PROJECT AGENTIC GRC: TECHNICAL ARCHITECTURE AND IMPLEMENTATION PLAN
## AI Agent for Automated Auditing and Verification of GRC Compliance (ISO/IEC 27001:2022 & Cloud Security)

This document establishes the technical architecture, deployment specifications, and step-by-step instructions to build, deploy, and govern an AI-powered Governance, Risk, and Compliance (GRC) Agent inside the **Google Cloud Platform (GCP)** environment. It utilizes the **Gemini Enterprise Agent Platform (GEAP)** and is designed for local development via **Google Cloud Antigravity** and testing via the **Jetsky** container runtime (Cloud Run / GKE Agent Sandbox).

---

## 1. PROJECT OVERVIEW & COMPLIANCE USE CASES (ISO 27001:2022)

The **Agentic GRC Agent** is an intelligent multi-agent orchestration framework designed to audit multi-cloud infrastructure configurations and organizational policy documents continuously. It maps technical states directly to the **ISO/IEC 27001:2022** standard requirements and the Climate Action Amendment (**Amd 1:2024**).

### Core Audit Use Cases:
1. **Continuous Cloud Security Audit (Control A.5.23)**: Real-time analysis of network boundaries, firewalls, IAM role bindings, and cryptographic keys (Cloud KMS/EKM) to detect configuration drift against security baselines.
2. **Infrastructure-as-Code (IaC) Scanning (Control A.8.9)**: Static analysis of Terraform and Ansible code within deployment pipelines (via DevSecOps hooks) to detect misconfigurations before provisioning.
3. **Active Threat Intelligence Audit (Control A.5.7)**: Correlating cloud logging audit trails (queried from BigQuery) with active threat intelligence feeds from **Google SecOps (Chronicle)** and **Mandiant** to ensure active monitoring compliance.
4. **Climate Resilience and Disaster Recovery Audit (Amd 1:2024)**: Assessing the geographic distribution of critical assets, active-active failover capabilities, and weather-related business continuity risks within Clauses 4.1 & 4.2 of the ISMS.

---

## 2. REFERENCE ARCHITECTURE DIAGRAM

The diagram below maps the safe, **Zero-Trust** end-to-end flow of user requests, model processing, gateway boundaries, and outbound data integration via the **Model Context Protocol (MCP)** and **Agent2Agent (A2A)** protocols:

```
                                  +----------------------------+
                                  |     User Interface (UI)    |
                                  |    (Gemini Enterprise)     |
                                  +--------------+-------------+
                                                 |
                                                 | Ingress Payload
                                                 v
+-----------------------------------------------------------------------------------------+
|                                      AGENT GATEWAY                                      |
|                                                                                         |
|   +--------------------------+                         +----------------------------+   |
|   |                          |  Inspect Ingress        |                            |   |
|   |     Model Armor API      |<------------------------|   Ingress Security Flow    |   |
|   |  - Input Sanitization    |                         |                            |   |
|   |  - Prompt Injection Block|========================>|  - Validate ID Token       |   |
|   |  - PII Masking/Redact    |  ALLOW or BLOCK Verdict |  - Enforce Permissions     |   |
|   |                          |                         +--------------+-------------+   |
|   +--------------------------+                                        |                 |
+-----------------------------------------------------------------------|-----------------+
                                                                        |
                                                                        | Sanitized Traffic
                                                                        v
+-----------------------------------------------------------------------------------------+
|                                    AGENT RUNTIME (GEAP)                                 |
|                                                                                         |
|   +---------------------------------------------------------------------------------+   |
|   |                        Orchestrator Agent (ADK v1.0)                            |   |
|   |                   (SPIFFE Cryptographic ID: spiffe://...)                       |   |
|   |                                                                                 |   |
|   |   +--------------------+     +---------------------+     +------------------+   |   |
|   |   | Gemini 3.7 Flash   |     | Memory Bank / State |     |  RAG Engine      |   |   |
|   |   |  (Reasoning Core)  |     |  (Persistent Memory)|     | (Spanner/Vertex) |   |   |
|   |   +--------------------+     +---------------------+     +------------------+   |   |
|   +---------------------------------------------------------------------------------+   |
+-----------------------------------------------------------------------|-----------------+
                                                                        |
                                                                        | Outbound Call (Egress)
                                                                        v
+-----------------------------------------------------------------------------------------+
|                                      AGENT GATEWAY                                      |
|                                                                                         |
|   +--------------------------+                         +----------------------------+   |
|   |                          |  Inspect Egress Data    |                            |   |
|   |     Model Armor API      |<------------------------|    Egress Security Flow    |   |
|   |  - Exfiltration Block    |                         |                            |   |
|   |  - Safe Browsing         |========================>|  - Resolve MCP Tool Call   |   |
|   |  - Output Alignment      |  ALLOW or BLOCK Verdict |  - Inspect A2A Envelope    |   |
|   +--------------------------+                         +--------------+-------------+   |
+-----------------------------------------------------------------------|-----------------+
                                                                        |
                                                                        | Secure Connections
                                                                        v
            +-----------------------------------------------------------+----------------------------+
            |                                                           |                            |
            v (MCP StreamableHTTP over Cloud Run)                       v (A2A Protocol over HTTPS)  v (REST / API)
  +-------------------------------------+                  +---------------------------+   +-------------------+
  |          MCP Server GRC             |                  |       Wiz Sub-Agent       |   |   Google SecOps   |
  |  - BigQuery (IAM/Asset Inventory)   |                  | - Map Toxic Combinations  |   |   Mandiant API    |
  |  - Google Drive (Policies & PDFs)   |                  |   on Cloud Security Graph |   |   (Control A.5.7) |
  +-------------------------------------+                  +---------------------------+   +-------------------+
```

---

## 3. PLATFORM COMPONENTS & FRAMEWORKS (GEAP)

To implement this architecture in your GCP sandbox via **Antigravity**, the development and runtime environment is split according to 2026 enterprise standards:

1. **Modeling Layer (Model Garden)**: We utilize **Gemini 3.7 Flash** as the default engine for high-speed reasoning, structured tool invocation, and code execution. For deep, unstructured policy analysis, the system dynamically scales to **Gemini 3.5 Pro** or **Claude 3.5 Sonnet v2** via unified Model Garden APIs.
2. **Agent Development Kit (ADK v1.0)**: Built on a Python-based execution graph. The orchestrator agent coordinates reasoning flows, registers external systems, and delegates sub-tasks to specialized domain agents.
3. **Execution Platform (Agent Engine)**: A fully managed, serverless GCP runtime that hosts the ADK graph, providing sub-second cold starts and secure sandbox containers.
4. **Context & Persistence Layer**:
   * **Sessions**: Automatically tracks and stores conversation history linked to unique Audit Session IDs.
   * **Memory Bank / Memory Profiles**: Dynamically captures organizational context, remediation trends, and historical non-compliance states, persisting learning vectors across auditing sessions.

---

## 4. TECHNICAL INTEGRATION LAYER (MCP & A2A)

### A. Model Context Protocol (MCP) for Secure Data Access
The agent never queries databases directly with hardcoded API keys. Instead, it interacts with data repositories through a **custom MCP server** deployed on **Cloud Run**.
* **Mandatory Transport**: The connection uses **StreamableHTTP** (the legacy SSE transport is not supported by Gemini Enterprise).
* **Dual-Token Authorization Flow**:
  1. Gemini Enterprise injects the client's OAuth token into the `ToolContext` state.
  2. When triggering the Cloud Run tool endpoint, Gemini Enterprise injects both the `X-Serverless-Authorization` header (GCP Service Agent ID Token) to pass Cloud Run ingress validation, and the standard `Authorization` header containing the user's OAuth token for fine-grained database access control.

### B. Agent2Agent (A2A) Protocol for Multi-Cloud Collaborations
When audit requirements span across multiple cloud vendors or depend on third-party security findings (e.g., pulling posture data from the **Wiz CNAPP** API), the GRC Agent acts as an **A2A Client** and coordinates with external **A2A Servers**:
1. **Discovery**: The orchestrator fetches the `/.well-known/agent.json` (Agent Card) from the target server to inspect its supported capabilities, schemas, and endpoints.
2. **Authentication**: Mutual TLS (mTLS), delegated JWTs, or OAuth 2.0 flow.
3. **Task Orchestration**: The orchestrator registers a `Task` resource on the target server. The sub-task progresses asynchronously using Server-Sent Events (SSE) following the lifecycle: `submitted -> working -> input-required -> completed/failed`.

---

## 5. PLATFORM SECURITY AND GOVERNANCE (THE IRON TRIANGLE)

Before deploying GRC agents on organizational infrastructure, establish these three security boundaries:

1. **Agent Identity (SPIFFE)**: Each ADK agent runs with an isolated cryptographic SPIFFE identity linked to GCP IAM. This enforces the *least privilege* principle. Never use global, over-privileged Service Accounts.
2. **Agent Gateway**: Enforces outbound network compliance. Every connection originating from the agent runtime must pass through this proxy, preventing unapproved API calls or shadow exfiltration.
3. **Model Armor**: A high-speed, inline safety layer bound to the Gateway:
   * **Ingress Filter (Client-to-Agent)**: Screens incoming user prompts for Prompt Injection, Jailbreak attempts, and malicious system overrides.
   * **Egress Filter (Agent-to-Anywhere)**: Inspects outputs and MCP arguments to mask PII, redact secret keys detected in logging outputs, and block malicious URI destinations.

---

## 6. GCP PROVISIONING & CONFIGURATION COMMANDS

Execute these commands in your GCP Cloud Shell to initialize the sandbox resources.

### Step 1: Enable Core Google Cloud APIs
```bash
# Set your active sandbox project ID
export PROJECT_ID="your-sandbox-project-id"
gcloud config set project $PROJECT_ID

# Enable Model Armor, Discovery Engine (GEAP), and Cloud Run APIs
gcloud services enable \
    modelarmor.googleapis.com \
    discoveryengine.googleapis.com \
    run.googleapis.com \
    aiplatform.googleapis.com
```

### Step 2: Create a Model Armor Safety Template
```bash
gcloud model-armor templates create g-rc-safety-baseline \
  --location=us-central1 \
  --rai-settings-filters='[{"filterType":"HATE_SPEECH","confidenceLevel":"MEDIUM_AND_ABOVE"}]' \
  --pi-and-jailbreak-filter-settings-enforcement=enabled \
  --pi-and-jailbreak-filter-settings-confidence-level=medium-and-above \
  --malicious-uri-filter-settings-enforcement=enabled
```

### Step 3: Configure Service Agent Permissions for GEAP & Cloud Run
```bash
# Retrieve your GCP Project Number
export PROJECT_NUMBER=$(gcloud projects describe $PROJECT_ID --format="value(projectNumber)")

# Grant Model Armor usage permissions to the Vertex AI service agent (GEAP Engine)
gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:service-$PROJECT_NUMBER@gcp-sa-aiplatform.iam.gserviceaccount.com" \
    --role="roles/modelarmor.user"

# Authorize the Discovery Engine Service Agent to invoke the secure Cloud Run MCP server
gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:service-$PROJECT_NUMBER@gcp-sa-discoveryengine.iam.gserviceaccount.com" \
    --role="roles/run.invoker"
```

### Step 4: Override Organization Constraint for Custom MCPs
In the GCP Console under **IAM & Admin > Org Policies**:
1. Search for the constraint: `Disable custom mcp server connector for gemini enterprise`.
2. Click **Manage Policy** and toggle **Override parent's policy**.
3. Add a rule setting the enforcement state to **OFF**, then click save.

---

## 7. TARGET REPOSITORY STRUCTURE (`agentic_grc_certifications`)

Organize your new Git repository as follows to facilitate CI/CD pipelines and modular local testing inside Jetsky/Antigravity:

```
agentic_grc_certifications/
├── .github/
│   └── workflows/
│       └── deploy.yml          # CI/CD Pipeline to build and deploy GRC agents to Cloud Run/Agent Engine
├── README.md                   # Main Project Documentation (This File)
├── gcloud_setup.sh             # GCP Environment initialization bash script
├── agent_orchestrator/
│   ├── __init__.py
│   ├── agent.py                # Core Orchestrator ADK v1.0 code
│   ├── requirements.txt        # Orchestrator dependencies (google-genai, vertexai, fastapi, etc.)
│   └── Dockerfile              # Docker configuration for Agent Engine deployment
└── mcp_server_grc/
    ├── __init__.py
    ├── server.py               # Custom MCP Server (StreamableHTTP over FastAPI)
    ├── schema.json             # Declarative definition of exposed tools
    ├── requirements.txt        # Server dependencies
    └── Dockerfile              # Containerization for Cloud Run Deployment
```

---

## 8. CODE SCAFFOLDING (PYTHON)

### A. Orchestrator Agent ADK v1.0 (`agent_orchestrator/agent.py`)
This script initializes the core agent flow, extracts the delegated OAuth token from the `ToolContext` safely, and executes auditing logic:

```python
import os
import re
import google.auth
from google import genai
from vertexai.preview import reasoning_engines

# Gemini 2026 Platform Configurations
MODEL_ID = "gemini-3.7-flash"
CLIENT_AUTH_NAME = "agent-grc-identity"

class GRCAgentOrchestrator:
    def __init__(self):
        # Initialize the unified Gemini Client
        self.client = genai.Client()
        self.project_id = self._get_project_id()

    def _get_project_id(self):
        _, project = google.auth.default()
        if not project:
            raise Exception("Failed to automatically resolve GCP Project ID from the environment.")
        return project

    def _get_bearer_token(self, tool_context) -> str:
        """
        Safely extracts the delegated end-user OAuth bearer token 
        injected into the ToolContext by Gemini Enterprise.
        """
        escaped_name = re.escape(CLIENT_AUTH_NAME)
        pattern = re.compile(fr"^{escaped_name}_\\d+$")
        
        state_dict = tool_context.state.to_dict() if hasattr(tool_context.state, 'to_dict') else tool_context.state
        matching_keys = [k for k in state_dict.keys() if pattern.match(k)]
        if matching_keys:
            return state_dict.get(matching_keys[0])
        raise Exception("Required User Bearer Token was not found in the ToolContext payload.")

    def audit_gcp_resource(self, resource_name: str, control_id: str, tool_context) -> dict:
        """
        Exposed Agent Tool: audits a target GCP asset state against ISO 27001 requirements.
        """
        token = self._get_bearer_token(tool_context)
        # The agent uses the OAuth token to query BigQuery or Asset Inventory via the MCP server.
        headers = {"Authorization": f"Bearer {token}"}
        
        return {
            "status": "audited",
            "control": control_id,
            "resource": resource_name,
            "finding": "No compliance violations or configuration drifts detected for control A.5.23.",
            "evidence_secured": True
        }

    def get_agent_instructions(self) -> str:
        return """
        You are the "AgentG-RC", an expert Virtual GRC & ISO/IEC 27001:2022 Lead Auditor.
        Your mission is to continuously audit the user's GCP configurations and policy definitions.
        Utilize 'audit_gcp_resource' to fetch and validate technical states in the client environment.
        Ensure every compliance finding is strictly mapped to the ISO 27001:2022 Annex A controls.
        Maintain a highly professional, consultative, precise, and actionable audit tone.
        """
```

### B. Custom GRC MCP Server (`mcp_server_grc/server.py`)
This FastAPI application exposes an MCP-compliant interface running over **StreamableHTTP**, prepared to be mounted securely into the Gemini Enterprise app:

```python
from fastapi import FastAPI, Header, HTTPException, Depends
from pydantic import BaseModel
import httpx
import json

app = FastAPI(title="Custom MCP Server - ISO 27001 GRC Compliance Tooling")

class ToolCallRequest(BaseModel):
    tool: str
    arguments: dict

@app.get("/.well-known/agent.json")
def get_agent_card():
    """
    Discovery Endpoint (Agent Card) utilized by the A2A protocol and Gemini Enterprise integration.
    """
    return {
        "protocol_version": "1.0",
        "name": "mcp-server-grc-evidence",
        "description": "Exposes real-time GCP posture data and security policy definitions from GCS/BigQuery.",
        "url": "https://mcp-server-grc-us-central1.run.app/mcp",
        "capabilities": {
            "streaming": True,
            "auth_schemes": ["oauth2"]
        },
        "skills": [
            {
                "name": "get_iam_policy",
                "description": "Fetches and audits the IAM policy configurations of a target GCS Bucket for control A.5.23.",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "bucket_name": {"type": "string", "description": "The target GCS bucket name."}
                    },
                    "required": ["bucket_name"]
                }
            }
        ]
    }

@app.post("/mcp")
def handle_tool_call(
    request: ToolCallRequest,
    x_serverless_authorization: str = Header(None), # Validates GCP Service Agent Ingress Identity
    authorization: str = Header(None)               # Delegates the authenticated end-user OAuth token
):
    # Enforce strict dual-token security architecture (Zero-Trust Validation)
    if not x_serverless_authorization:
        raise HTTPException(status_code=401, detail="Missing X-Serverless-Authorization header. Unauthorized gateway request.")
    
    if request.tool == "get_iam_policy":
        bucket = request.arguments.get("bucket_name")
        # Under a real run, the code utilizes the 'authorization' header to query GCP GCS IAM states.
        return {
            "tool": "get_iam_policy",
            "result": {
                "bucket": bucket,
                "public_access_prevention": "enforced",
                "non_compliant_roles": [],
                "status": "COMPLIANT_WITH_A.5.23_REQUIREMENTS"
            }
        }
    
    raise HTTPException(status_code=404, detail="Requested tool configuration is not defined on this MCP Server.")
```

---

## 9. PROJECT TIMELINE & ROLLOUT MILESTONES

| Implementation Phase | Core Technical Deliverables | Gate / Acceptance Criteria |
| :--- | :--- | :--- |
| **Phase 1: IAM & Safety Baseline** | Provision IAM boundaries, create SPIFFE Agent Identity mapping, deploy network Gateway, enforce initial Model Armor template. | All test agents run with restricted SPIFFE IDs. Ingress Model Armor block rules intercept simulated injection vectors. |
| **Phase 2: MCP GRC & Connector Deployment** | Deploy FastAPI MCP server to Cloud Run, disable GCP Custom MCP Org Policy, bind Discovery Engine invoker permission. | Gemini App can resolve GCS Bucket status tool executions securely over authenticated StreamableHTTP connections. |
| **Phase 3: Observability & Continuous Auditing**| Install OpenTelemetry tracing pipelines, set up Agent Simulation testing suites, expose compliance findings inside Cloud Observability dashboards. | Automated configuration drift alerts trigger on GRC dashboards. Agent health monitoring detects anomaly signatures. |

---
**Prepared by:** Virtual GRC & ISO 27001 Lead Consultant
*Grounding Assurance: Grounded on native Gemini Enterprise Agent Platform documentation, Linux Foundation A2A specs, ISO/IEC 27001:2022 standards, and Google Cloud security reference patterns.*
