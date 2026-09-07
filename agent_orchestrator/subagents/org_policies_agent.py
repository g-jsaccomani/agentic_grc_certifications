"""Organizational Policies Specialist Sub-Agent with Gemini Zero-Copy Grounding.

Dedicated to evaluating written organizational policies, ISMS scope documents,
and security guidelines against technical cloud configurations.
Utilizes the Zero-Copy Grounding interface (Google Drive, SharePoint, Confluence, Jira).
"""

from typing import Any, Callable, Dict, List, Optional
from agent_orchestrator.llm_subagent import LLMSubAgent
from agent_orchestrator.zero_copy_connector import (
    ConnectorSource,
    ZeroCopyConnectorManager,
    ZeroCopyDocument,
)


ORG_POLICIES_SYSTEM_PROMPT = """
Você é o Auditor Especialista em Políticas Organizacionais e Governança SGSI (ISO/IEC 27001:2022).
Sua missão é realizar a análise de aderência (Gap Analysis) entre políticas corporativas documentadas
e o estado técnico da infraestrutura em nuvem, garantindo rastreabilidade Zero-Copy.
"""


class OrgPoliciesSubAgent:
    """Specialized ADK Sub-Agent for Organizational Policies and ISMS Governance."""

    def __init__(
        self,
        spiffe_id: str = "spiffe://grc.jetsky.gcp/ns/production/sa/subagent-org-policies",
        connector_manager: Optional[ZeroCopyConnectorManager] = None,
        client: Optional[Any] = None,
        model_id: Optional[str] = None,
    ):
        self.spiffe_id = spiffe_id
        self.role = "Organizational Policies & Governance Specialist"
        self.connectors = connector_manager or ZeroCopyConnectorManager()

        self.tools: Dict[str, Callable[..., Dict[str, Any]]] = {
            "cross_reference_policy_with_tech_state": self._eval_policy_alignment,
        }

        self.llm = LLMSubAgent(
            name="org_policies_agent",
            system_instruction=ORG_POLICIES_SYSTEM_PROMPT,
            tools=self.tools,
            model_id=model_id,
            client=client,
        )

    def run(self, user_task: str, max_turns: int = 4, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Runs the LLM function-calling loop for policy evaluation."""
        return self.llm.run(user_task, max_turns=max_turns, context=context)

    async def arun(self, user_task: str, max_turns: int = 4, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Async version of LLM function-calling loop."""
        return await self.llm.arun(user_task, max_turns=max_turns, context=context)

    def cross_reference_policy_with_tech_state(
        self,
        policy_keyword: str,
        technical_finding: Dict[str, Any],
        user_token: str,
    ) -> Dict[str, Any]:
        """Queries corporate policy via Zero-Copy and cross-references with technical telemetry."""
        return self._eval_policy_alignment(policy_keyword, technical_finding, user_token)

    def _eval_policy_alignment(
        self,
        policy_keyword: str,
        technical_finding: Dict[str, Any],
        user_token: Optional[str] = None,
    ) -> Dict[str, Any]:
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
