"""Annex A Specialist Sub-Agent with Real Gemini Function Calling & Grounding.

Dedicated to rigorous technical and administrative auditing against
ISO/IEC 27001:2022 Annex A controls (A.5, A.6, A.7, A.8), including:
- A.5.23: Cloud Security
- A.8.9: Configuration Management
- A.8.12: Data Leakage Prevention (DLP)
- A.8.16: Monitoring Activities
- A.8.24: Use of Cryptography
- A.8.28: Secure Coding / Development

Operates as a true LLMSubAgent: executes Gemini function calling via Vertex AI
with tools/*.py as the deterministic source of truth and strict grounding checks.
"""

from typing import Any, Callable, Dict, List, Optional
from agent_orchestrator.llm_subagent import LLMSubAgent
from mcp_server_grc.tools.cloud_security import audit_cloud_security
from mcp_server_grc.tools.data_leakage_prevention import audit_data_leakage_prevention
from mcp_server_grc.tools.monitoring import audit_monitoring_activities
from mcp_server_grc.tools.threat_intel import correlate_threat_intelligence
from mcp_server_grc.cloud_inspector import inspect_cloud_kms_key
from mcp_server_grc.tools.iac_scanner import scan_iac_configuration


ANNEX_A_SYSTEM_PROMPT = """
Você é o Auditor Especialista em Annex A (ISO/IEC 27001:2022).
Regra absoluta: você NUNCA declara um recurso como conforme ou não conforme
por conta própria. Você SEMPRE chama a tool correspondente e reporta
exatamente o 'status' e as 'violations' que ela retornar.
Se a tool retornar UNDETERMINED, você reporta UNDETERMINED — nunca infere
conformidade na ausência de evidência.
"""


class AnnexASubAgent:
    """Specialized ADK Sub-Agent for ISO 27001 Annex A verification with Gemini LLM Core."""

    def __init__(
        self,
        spiffe_id: str = "spiffe://grc.jetsky.gcp/ns/production/sa/subagent-annex-a",
        client: Optional[Any] = None,
        model_id: Optional[str] = None,
    ):
        self.spiffe_id = spiffe_id
        self.role = "ISO/IEC 27001:2022 Annex A Specialist"

        # Register Annex A deterministic tool suite
        self.tools: Dict[str, Callable[..., Dict[str, Any]]] = {
            "audit_cloud_security": audit_cloud_security,
            "audit_data_leakage_prevention": audit_data_leakage_prevention,
            "audit_monitoring_activities": audit_monitoring_activities,
            "scan_iac_configuration": scan_iac_configuration,
            "audit_cryptography_a824": self._eval_cryptography_a824,
            "audit_secure_development_a828": self._eval_secure_development_a828,
            "inspect_cloud_kms": inspect_cloud_kms_key,
        }

        # Underlying LLM subagent engine
        self.llm = LLMSubAgent(
            name="annex_a_agent",
            system_instruction=ANNEX_A_SYSTEM_PROMPT,
            tools=self.tools,
            model_id=model_id,
            client=client,
        )

    def run(self, user_task: str, max_turns: int = 4, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Runs the LLM function-calling loop for Annex A audit tasks."""
        return self.llm.run(user_task, max_turns=max_turns, context=context)

    async def arun(self, user_task: str, max_turns: int = 4, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Async version of LLM function-calling loop."""
        return await self.llm.arun(user_task, max_turns=max_turns, context=context)

    def audit_cryptography_a824(
        self,
        key_id: str,
        config: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Audits Control A.8.24 (Use of Cryptography).

        Public wrapper maintaining backward-compatibility with ContinuousIntelligenceEngine.
        """
        return self._eval_cryptography_a824(key_id=key_id, config=config)

    def _eval_cryptography_a824(
        self,
        key_id: str,
        config: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Internal deterministic evaluator for Control A.8.24."""
        if not isinstance(config, dict) or not config:
            return {
                "status": "UNDETERMINED",
                "control": "ISO/IEC 27001:2022 A.8.24",
                "resource_id": key_id,
                "metrics": {},
                "violations": ["Insufficient KMS telemetry: key configuration empty or not provided."],
                "remediation": "Provide KMS key rotation and protection level telemetry.",
            }

        violations: List[str] = []
        rotation_period = config.get("rotation_period_seconds", 7776000)
        protection_level = config.get("protection_level", "SOFTWARE")
        algorithm = config.get("algorithm", "GOOGLE_SYMMETRIC_ENCRYPTION")

        if rotation_period > 7776000:
            violations.append(
                f"KMS Key '{key_id}' rotation period ({rotation_period}s) exceeds 90 days policy requirement."
            )

        if config.get("require_hsm", False) and protection_level != "HSM":
            violations.append(
                f"KMS Key '{key_id}' uses protection level '{protection_level}' instead of mandated 'HSM'."
            )

        is_compliant = len(violations) == 0
        return {
            "status": "COMPLIANT" if is_compliant else "NON_COMPLIANT",
            "control": "ISO/IEC 27001:2022 A.8.24",
            "resource_id": key_id,
            "metrics": {
                "protection_level": protection_level,
                "rotation_period_seconds": rotation_period,
                "algorithm": algorithm,
            },
            "violations": violations,
            "remediation": (
                "Cryptography baseline is compliant with Control A.8.24."
                if is_compliant
                else "Adjust key rotation schedule and enforce HSM protection level."
            ),
        }

    def audit_secure_development_a828(
        self,
        repo_id: str,
        dev_policy: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Audits Control A.8.28 (Secure Coding).

        Public wrapper maintaining backward-compatibility with ContinuousIntelligenceEngine.
        """
        return self._eval_secure_development_a828(repo_id=repo_id, dev_policy=dev_policy)

    def _eval_secure_development_a828(
        self,
        repo_id: str,
        dev_policy: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Internal deterministic evaluator for Control A.8.28."""
        if not isinstance(dev_policy, dict) or not dev_policy:
            return {
                "status": "UNDETERMINED",
                "control": "ISO/IEC 27001:2022 A.8.28",
                "resource_id": repo_id,
                "metrics": {},
                "violations": ["Insufficient SDLC telemetry: repository dev_policy empty or not provided."],
                "remediation": "Provide repository dev_policy specifying SAST, branch protection, and signed commit settings.",
            }

        violations: List[str] = []
        sast_enabled = dev_policy.get("sast_enabled", False)
        branch_protection = dev_policy.get("branch_protection_enforced", False)
        signed_commits = dev_policy.get("signed_commits_required", False)

        if not sast_enabled:
            violations.append(
                f"Repository '{repo_id}' does not have automated Static Application Security Testing (SAST) in CI/CD."
            )

        if not branch_protection:
            violations.append(
                f"Repository '{repo_id}' lacks branch protection rules requiring code reviews prior to merge."
            )

        if not signed_commits:
            violations.append(
                f"Repository '{repo_id}' does not mandate GPG/SSH cryptographically signed commits."
            )

        is_compliant = len(violations) == 0
        return {
            "status": "COMPLIANT" if is_compliant else "NON_COMPLIANT",
            "control": "ISO/IEC 27001:2022 A.8.28",
            "resource_id": repo_id,
            "metrics": {
                "sast_enabled": sast_enabled,
                "branch_protection_enforced": branch_protection,
                "signed_commits_required": signed_commits,
            },
            "violations": violations,
            "remediation": (
                "Secure development practices conform to Control A.8.28."
                if is_compliant
                else "Enforce automated CI/CD SAST pipelines, branch protection, and commit signing."
            ),
        }
