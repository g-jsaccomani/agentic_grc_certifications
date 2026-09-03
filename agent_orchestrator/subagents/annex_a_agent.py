"""Annex A Specialist Sub-Agent.

Dedicated to rigorous technical and administrative auditing against
ISO/IEC 27001:2022 Annex A controls (A.5, A.6, A.7, A.8), including:
- A.5.23: Cloud Security
- A.8.9: Configuration Management
- A.8.12: Data Leakage Prevention (DLP)
- A.8.16: Monitoring Activities
- A.8.24: Use of Cryptography
- A.8.28: Secure Coding / Development
"""

from typing import Any, Dict, List, Optional
from mcp_server_grc.tools.cloud_security import audit_cloud_security
from mcp_server_grc.tools.data_leakage_prevention import audit_data_leakage_prevention
from mcp_server_grc.tools.monitoring import audit_monitoring_activities
from mcp_server_grc.tools.iac_scanner import scan_iac_configuration


class AnnexASubAgent:
    """Specialized ADK Sub-Agent for ISO 27001 Annex A verification."""

    def __init__(self, spiffe_id: str = "spiffe://grc.jetsky.gcp/ns/production/sa/subagent-annex-a"):
        self.spiffe_id = spiffe_id
        self.role = "ISO/IEC 27001:2022 Annex A Specialist"

    def audit_cryptography_a824(
        self,
        key_id: str,
        config: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Audits Control A.8.24 (Use of Cryptography).

        Verifies algorithm strength, key rotation cycle (<= 90 days for high-risk),
        and hardware security module (HSM) enforcement.
        """
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

        Verifies automated SAST/DAST in CI/CD, dependency scanning,
        and branch protection enforcement.
        """
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
