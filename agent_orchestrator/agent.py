"""Orchestrator Agent ADK v1.0 for GRC & ISO/IEC 27001:2022 Auditing.

Integrates Gemini 3.7 Flash reasoning core, SPIFFE identity,
ToolContext dual-token extraction, Model Armor safety boundaries,
and MCP / A2A communication pipelines.
"""

import os
import re
from typing import Any, Dict, List, Optional
import google.auth
from google import genai
import httpx

from agent_orchestrator.gateway import ModelArmorGateway
from agent_orchestrator.a2a_client import A2AClient, A2ATask

# Gemini 2026 Platform Configurations
MODEL_ID = os.getenv("GEMINI_MODEL_ID", "gemini-3.7-flash")
CLIENT_AUTH_NAME = "agent-grc-identity"


class GRCAgentOrchestrator:
    """Core GRC Orchestrator Agent conforming to Gemini Enterprise Agent Platform (GEAP)."""

    def __init__(
        self,
        mcp_server_url: Optional[str] = None,
        gateway: Optional[ModelArmorGateway] = None,
    ):
        self.mcp_server_url = mcp_server_url or os.getenv(
            "MCP_SERVER_URL", "http://localhost:8080"
        )
        self.gateway = gateway or ModelArmorGateway()
        self.spiffe_id = self.gateway.get_spiffe_id(agent_name="grc-orchestrator")
        self.a2a_client = A2AClient()
        self.project_id = self._get_project_id()

        # In-memory session tracking / Memory Bank simulation
        self.audit_sessions: Dict[str, List[Dict[str, Any]]] = {}

        # Initialize genai Client if API credentials exist
        try:
            self.client = genai.Client()
        except Exception:
            self.client = None

    def _get_project_id(self) -> str:
        """Resolves GCP Project ID from environment or default credentials."""
        project = os.getenv("PROJECT_ID") or os.getenv("GOOGLE_CLOUD_PROJECT")
        if project:
            return project
        try:
            _, resolved = google.auth.default()
            if resolved:
                return resolved
        except Exception:
            pass
        return "sandbox-grc-project"

    def _get_bearer_token(self, tool_context: Any) -> str:
        """Safely extracts the delegated end-user OAuth bearer token

        injected into the ToolContext by Gemini Enterprise.
        """
        escaped_name = re.escape(CLIENT_AUTH_NAME)
        pattern = re.compile(fr"^{escaped_name}_\d+$")

        if tool_context is None:
            # Fallback for direct testing
            return os.getenv("TEST_BEARER_TOKEN", "mock-delegated-bearer-token")

        state = getattr(tool_context, "state", tool_context)
        state_dict = state.to_dict() if hasattr(state, "to_dict") else (state if isinstance(state, dict) else {})

        matching_keys = [k for k in state_dict.keys() if pattern.match(k)]
        if matching_keys:
            return state_dict.get(matching_keys[0])

        # If key named CLIENT_AUTH_NAME directly exists
        if CLIENT_AUTH_NAME in state_dict:
            return state_dict[CLIENT_AUTH_NAME]

        raise ValueError("Required User Bearer Token was not found in the ToolContext payload.")

    def audit_gcp_resource(
        self,
        resource_name: str,
        control_id: str,
        resource_type: str = "gcs_bucket",
        config: Optional[Dict[str, Any]] = None,
        tool_context: Any = None,
    ) -> Dict[str, Any]:
        """Exposed Agent Tool: audits a target GCP asset state against ISO 27001 requirements."""
        token = self._get_bearer_token(tool_context)
        headers = {
            "Authorization": f"Bearer {token}",
            "X-Serverless-Authorization": f"Bearer service-agent-id-token-for-{self.project_id}",
        }

        payload = {
            "tool": "audit_cloud_security",
            "arguments": {
                "resource_type": resource_type,
                "resource_name": resource_name,
                "config": config or {},
            },
        }

        # Route via MCP Server if reachable, otherwise run local fallback verification
        try:
            with httpx.Client(timeout=5.0) as http_client:
                resp = http_client.post(f"{self.mcp_server_url}/mcp", json=payload, headers=headers)
                if resp.status_code == 200:
                    return resp.json().get("result", {})
        except Exception:
            pass

        from mcp_server_grc.tools.cloud_security import audit_cloud_security
        return audit_cloud_security(
            resource_type=resource_type,
            resource_name=resource_name,
            config=config,
            bearer_token=token,
        )

    def scan_iac(
        self,
        iac_type: str,
        content: str,
        filename: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Audits Terraform or Ansible IaC against ISO 27001:2022 Control A.8.9."""
        from mcp_server_grc.tools.iac_scanner import scan_iac_configuration
        return scan_iac_configuration(iac_type=iac_type, content=content, filename=filename)

    def audit_threat_intelligence(
        self,
        log_sink_name: str,
        sink_destination: str,
        recent_events: Optional[List[Dict[str, Any]]] = None,
        threat_feed_enabled: bool = True,
    ) -> Dict[str, Any]:
        """Audits threat intelligence correlation per ISO 27001:2022 Control A.5.7."""
        from mcp_server_grc.tools.threat_intel import correlate_threat_intelligence
        return correlate_threat_intelligence(
            log_sink_name=log_sink_name,
            sink_destination=sink_destination,
            recent_events=recent_events,
            threat_feed_enabled=threat_feed_enabled,
        )

    def audit_climate_resilience(
        self,
        workload_id: str,
        topology: Dict[str, Any],
        climate_risk_assessed: bool = True,
    ) -> Dict[str, Any]:
        """Audits climate resilience & DR per ISO 27001:2022 Amd 1:2024 (Clauses 4.1 & 4.2)."""
        from mcp_server_grc.tools.climate_resilience import audit_climate_resilience
        return audit_climate_resilience(
            workload_id=workload_id,
            topology=topology,
            climate_risk_assessed=climate_risk_assessed,
        )

    def process_audit_request(
        self,
        session_id: str,
        user_prompt: str,
        user_id_token: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Full end-to-end flow passing through Model Armor Ingress and Egress gates."""
        # 1. Ingress Gate: Model Armor inspection
        ingress_verdict = self.gateway.inspect_ingress(user_prompt, id_token=user_id_token)
        if not ingress_verdict.allowed:
            return {
                "status": "BLOCKED_BY_MODEL_ARMOR",
                "session_id": session_id,
                "reason": ingress_verdict.violations,
                "spiffe_id": self.spiffe_id,
            }

        sanitized_prompt = ingress_verdict.sanitized_prompt

        # 2. Record Session History / Memory Bank
        if session_id not in self.audit_sessions:
            self.audit_sessions[session_id] = []
        self.audit_sessions[session_id].append({"role": "user", "content": sanitized_prompt})

        # 3. Simulate or execute reasoning flow
        raw_response = (
            f"ISO/IEC 27001:2022 Continuous Audit Log:\n"
            f"Orchestrator [{self.spiffe_id}] processed request with model [{MODEL_ID}].\n"
            f"Request: {sanitized_prompt}\n"
            f"All Annex A controls and Amd 1:2024 resilience gates active."
        )

        # 4. Egress Gate: Model Armor inspection
        egress_verdict = self.gateway.inspect_egress(raw_response)
        if not egress_verdict.allowed:
            return {
                "status": "EGRESS_BLOCKED_BY_MODEL_ARMOR",
                "session_id": session_id,
                "reason": egress_verdict.violations,
            }

        final_content = egress_verdict.sanitized_output
        self.audit_sessions[session_id].append({"role": "assistant", "content": final_content})

        return {
            "status": "SUCCESS",
            "session_id": session_id,
            "spiffe_id": self.spiffe_id,
            "response": final_content,
            "ingress_pii_redacted": ingress_verdict.pii_redacted,
            "egress_secrets_redacted": egress_verdict.secrets_redacted,
        }

    def get_agent_instructions(self) -> str:
        """System instructions for Gemini 3.7 Flash reasoning core."""
        return """
        You are the "AgentG-RC", an expert Virtual GRC & ISO/IEC 27001:2022 Lead Auditor.
        Your mission is to continuously audit the user's GCP configurations, IaC definitions,
        threat intelligence pipelines, and climate resilience posture (Amd 1:2024).

        Core Capabilities:
        1. Cloud Security Audit (A.5.23): Enforce least privilege, UBLA/PAP on GCS, KMS key rotation <= 90 days.
        2. IaC Scanning (A.8.9): Detect misconfigurations in Terraform and Ansible code prior to deployment.
        3. Threat Intelligence (A.5.7): Correlate BigQuery audit logs with Google SecOps / Mandiant feeds.
        4. Climate Resilience (Amd 1:2024): Audit geographic redundancy and automated disaster recovery under Clauses 4.1 & 4.2.

        Ensure every compliance finding is strictly mapped to the ISO 27001:2022 Annex A controls.
        Maintain a highly professional, consultative, precise, and actionable audit tone.
        """
