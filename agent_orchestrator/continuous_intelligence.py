"""Continuous Intelligence & Proactive Compliance Engine for GEAP.

Acts as the persistent auditor and compliance implementer within a secure sandbox:
- Orchestrates, scales, and governs enterprise compliance assistants.
- Operates inside a secure sandbox with SPIFFE identity and Model Armor.
- Maps logical evidence into an Evidence Graph.
- Monitors security posture continuously and predicts compliance drift.
- Synthesizes and tests remediation playbooks with Zero-Trust human sign-off gates.
"""

import time
import uuid
from typing import Any, Dict, List, Optional

from agent_orchestrator.evidence_graph import EvidenceGraph, EvidenceVerificationTier
from agent_orchestrator.memory_bank import MemoryBank
from agent_orchestrator.remediation_engine import RemediationEngine
from agent_orchestrator.gateway import ModelArmorGateway
from agent_orchestrator.agent import GRCAgentOrchestrator


class ContinuousIntelligenceEngine:
    """GEAP-native proactive intelligence engine for continuous GRC auditing and implementation."""

    def __init__(
        self,
        organization_name: str = "Enterprise-Client",
        orchestrator: Optional[GRCAgentOrchestrator] = None,
        sandbox_runtime: str = "Jetsky-CloudRun-Sandbox",
    ):
        self.organization_name = organization_name
        self.sandbox_runtime = sandbox_runtime
        self.orchestrator = orchestrator or GRCAgentOrchestrator()
        self.evidence_graph = EvidenceGraph()
        self.memory_bank = MemoryBank(organization_name=organization_name)
        self.remediation_engine = RemediationEngine(sandbox_mode=True)
        self.gateway = self.orchestrator.gateway

    def execute_proactive_audit_cycle(
        self,
        cycle_id: Optional[str] = None,
        cloud_assets: Optional[List[Dict[str, Any]]] = None,
    ) -> Dict[str, Any]:
        """Executes a complete continuous audit cycle within the secure sandbox.

        Steps:
        1. Ingest cloud asset telemetry into EvidenceGraph.
        2. Execute ISO 27001:2022 control checks (A.5.23, A.8.9, A.8.12, A.8.16, Amd 1:2024).
        3. Map logical evidence links and hash verification.
        4. Calculate quantitative compliance score and rating.
        5. Record cycle in persistent MemoryBank and detect drift trends.
        6. Synthesize remediation plans inside sandbox.
        """
        cycle_id = cycle_id or f"cycle-{uuid.uuid4().hex[:8]}"
        cloud_assets = cloud_assets or []
        findings: List[Dict[str, Any]] = []
        remediation_plans: List[Dict[str, Any]] = []

        for asset in cloud_assets:
            ctrl = asset.get("target_control", "A.5.23")
            resource_type = asset.get("resource_type", "")
            resource_id = asset.get("resource_id", "unnamed-resource")
            config = asset.get("config", {})
            tier_str = asset.get("verification_tier", "VERIFIED")
            verification_tier = getattr(EvidenceVerificationTier, tier_str, EvidenceVerificationTier.VERIFIED)

            # 1. Add to Evidence Graph
            node = self.evidence_graph.add_evidence(
                resource_id=resource_id,
                resource_type=resource_type,
                control_id=ctrl,
                raw_payload=config,
                verification_tier=verification_tier,
            )

            # 2. Audit against target control
            finding: Dict[str, Any] = {}

            if "A.5.23" in ctrl:
                finding = self.orchestrator.audit_gcp_resource(
                    resource_name=resource_id,
                    control_id=ctrl,
                    resource_type=resource_type,
                    config=config,
                )
            elif "A.8.9" in ctrl:
                iac_type = config.get("iac_type", "terraform")
                content = config.get("content", "")
                finding = self.orchestrator.scan_iac(iac_type=iac_type, content=content, filename=resource_id)
            elif "A.8.12" in ctrl:
                finding = self.orchestrator.audit_data_leakage_prevention(
                    perimeter_name=resource_id,
                    perimeter_config=config,
                )
            elif "A.8.16" in ctrl:
                finding = self.orchestrator.audit_monitoring_activities(
                    project_id=resource_id,
                    monitoring_config=config,
                )
            elif "Amd 1:2024" in ctrl or "4.1" in ctrl:
                finding = self.orchestrator.audit_climate_resilience(
                    workload_id=resource_id,
                    topology=config,
                )
            else:
                finding = {"status": "UNKNOWN_CONTROL", "control": ctrl, "violations": []}

            findings.append(finding)

            # 3. Create Compliance Link in Evidence Graph
            violations = finding.get("violations", [])
            status = finding.get("status", "NON_COMPLIANT")
            self.evidence_graph.link_compliance_state(
                source_node_id=node.node_id,
                control_id=ctrl,
                status=status,
                justification=finding.get("remediation", finding.get("verdict", "")),
                violations=violations,
            )

            # 4. Synthesize Remediation Plan if non-compliant
            if status != "COMPLIANT" and violations:
                plan = self.remediation_engine.plan_remediation(
                    control_id=ctrl,
                    resource_id=resource_id,
                    violations=violations,
                )
                remediation_plans.append(plan.to_dict())

        # 5. Calculate Compliance Score
        score_report = self.orchestrator.calculate_compliance_score(findings)

        # 6. Record in Memory Bank
        non_compliant_ctrls = [f.get("control", "UNKNOWN") for f in findings if f.get("status") != "COMPLIANT"]
        self.memory_bank.record_audit_cycle(
            cycle_id=cycle_id,
            score=score_report["overall_score"],
            rating=score_report["rating"],
            total_controls=len(findings),
            non_compliant_controls=non_compliant_ctrls,
        )

        # 7. Analyze Drift Trends
        drift_trends = self.memory_bank.calculate_drift_trend()

        return {
            "cycle_id": cycle_id,
            "sandbox_runtime": self.sandbox_runtime,
            "spiffe_id": self.orchestrator.spiffe_id,
            "organization_name": self.organization_name,
            "scorecard": score_report,
            "drift_trajectory": drift_trends,
            "findings_count": len(findings),
            "findings": findings,
            "remediation_plans": remediation_plans,
            "evidence_graph_summary": self.evidence_graph.get_summary(),
        }
