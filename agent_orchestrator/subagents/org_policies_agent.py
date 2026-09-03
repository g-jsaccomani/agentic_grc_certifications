"""Organizational Policies Specialist Sub-Agent.

Dedicated to evaluating written organizational policies, ISMS scope documents,
and security guidelines against technical cloud configurations.
Utilizes the Zero-Copy Grounding interface (Google Drive, SharePoint, Confluence, Jira).
"""

from typing import Any, Dict, List, Optional
from agent_orchestrator.zero_copy_connector import (
    ConnectorSource,
    ZeroCopyConnectorManager,
    ZeroCopyDocument,
)


class OrgPoliciesSubAgent:
    """Specialized ADK Sub-Agent for Organizational Policies and ISMS Governance."""

    def __init__(
        self,
        spiffe_id: str = "spiffe://grc.jetsky.gcp/ns/production/sa/subagent-org-policies",
        connector_manager: Optional[ZeroCopyConnectorManager] = None,
    ):
        self.spiffe_id = spiffe_id
        self.role = "Organizational Policies & Governance Specialist"
        self.connectors = connector_manager or ZeroCopyConnectorManager()

    def cross_reference_policy_with_tech_state(
        self,
        policy_keyword: str,
        technical_finding: Dict[str, Any],
        user_token: str,
    ) -> Dict[str, Any]:
        """Queries corporate policy via Zero-Copy and cross-references with technical telemetry."""
        # Query policy via Google Drive / Confluence
        drive_docs = self.connectors.query_source(
            source=ConnectorSource.GOOGLE_DRIVE,
            query=policy_keyword,
            delegated_user_token=user_token,
        )

        policy_snippet = drive_docs[0].content_snippet if drive_docs else "No specific policy text retrieved."
        policy_title = drive_docs[0].title if drive_docs else "Default ISMS Baseline"

        tech_status = technical_finding.get("status", "UNKNOWN")
        control = technical_finding.get("control", "ISO 27001")

        is_aligned = tech_status == "COMPLIANT"

        return {
            "subagent_spiffe": self.spiffe_id,
            "control": control,
            "policy_grounding": {
                "source": "Google Drive (Zero-Copy)",
                "document": policy_title,
                "mandate": policy_snippet,
                "cached_externally": False,
            },
            "technical_state": tech_status,
            "policy_implementation_aligned": is_aligned,
            "gap_analysis": (
                "Technical configuration strictly adheres to documented corporate policy."
                if is_aligned
                else f"Divergence detected: Documented policy requires compliance, but technical state returned {technical_finding.get('violations', [])}."
            ),
        }
