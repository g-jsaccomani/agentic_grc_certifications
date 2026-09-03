"""Unit tests for Continuous Intelligence, Evidence Graph, Memory Bank, and Remediation Engine."""

import pytest
from agent_orchestrator.evidence_graph import (
    EvidenceGraph,
    EvidenceVerificationTier,
)
from agent_orchestrator.memory_bank import MemoryBank
from agent_orchestrator.remediation_engine import (
    RemediationEngine,
    RemediationExecutionMode,
)
from agent_orchestrator.continuous_intelligence import ContinuousIntelligenceEngine


def test_evidence_graph_hashing_and_queries():
    graph = EvidenceGraph()
    raw = {"bucket_name": "prod-data", "pap": "enforced"}
    node = graph.add_evidence(
        resource_id="prod-data",
        resource_type="gcs_bucket",
        control_id="ISO/IEC 27001:2022 A.5.23",
        raw_payload=raw,
        verification_tier=EvidenceVerificationTier.VERIFIED,
    )
    assert node.evidence_hash is not None
    assert len(node.evidence_hash) == 64  # SHA256 length

    link = graph.link_compliance_state(
        source_node_id=node.node_id,
        control_id="ISO/IEC 27001:2022 A.5.23",
        status="COMPLIANT",
        justification="PAP enforced",
    )
    assert link.status == "COMPLIANT"

    query_res = graph.query_by_control("ISO/IEC 27001:2022 A.5.23")
    assert len(query_res) == 1
    assert query_res[0]["evidence_node"]["resource_id"] == "prod-data"

    summary = graph.get_summary()
    assert summary["total_evidence_nodes"] == 1
    assert summary["compliant_links"] == 1
    assert summary["verification_tiers"]["VERIFIED"] == 1


def test_memory_bank_drift_and_hotspots():
    mb = MemoryBank(organization_name="Fintech-Corp")

    # Cycle 1: initial score 50%
    mb.record_audit_cycle(
        cycle_id="c1",
        score=50.0,
        rating="NEEDS_IMPROVEMENT",
        total_controls=4,
        non_compliant_controls=["A.5.23", "A.8.12"],
    )
    trend1 = mb.calculate_drift_trend()
    assert trend1["trend"] == "BASELINE_ESTABLISHED"

    # Cycle 2: score improves to 75%
    mb.record_audit_cycle(
        cycle_id="c2",
        score=75.0,
        rating="SATISFACTORY",
        total_controls=4,
        non_compliant_controls=["A.8.12"],
        remediated_controls=["A.5.23"],
    )
    trend2 = mb.calculate_drift_trend()
    assert trend2["trend"] == "IMPROVING"
    assert trend2["score_delta"] == 25.0
    assert "A.8.12" in trend2["recurring_hotspots"]


def test_remediation_engine_hitl_gate():
    engine = RemediationEngine(sandbox_mode=True)
    plan = engine.plan_remediation(
        control_id="ISO/IEC 27001:2022 A.5.23",
        resource_id="unprotected-bucket",
        violations=["Public Access Prevention is not enforced"],
    )
    assert plan.sandbox_validated is True
    assert plan.execution_status == RemediationExecutionMode.SANDBOX_DRY_RUN

    # Attempt to execute without approval token -> blocked
    blocked_plan = engine.execute_remediation(plan, human_approval_token=None)
    assert blocked_plan.execution_status == RemediationExecutionMode.BLOCKED_MISSING_APPROVAL

    # Execute with authenticated human approval token
    approved_plan = engine.execute_remediation(plan, human_approval_token="HITL-APPROVED-lead-auditor-123")
    assert approved_plan.execution_status == RemediationExecutionMode.PRODUCTION_APPLIED
    assert approved_plan.approval_token_used == "HITL-APPROVED-lead-auditor-123"


def test_continuous_intelligence_end_to_end_cycle():
    ci_engine = ContinuousIntelligenceEngine(organization_name="Global-Bank")

    cloud_assets = [
        # 1. Compliant GCS Bucket (A.5.23)
        {
            "target_control": "ISO/IEC 27001:2022 A.5.23",
            "resource_type": "gcs_bucket",
            "resource_id": "compliant-bucket",
            "config": {
                "public_access_prevention": "enforced",
                "uniform_bucket_level_access": True,
            },
            "verification_tier": "VERIFIED",
        },
        # 2. Non-Compliant GCS Bucket (A.5.23)
        {
            "target_control": "ISO/IEC 27001:2022 A.5.23",
            "resource_type": "gcs_bucket",
            "resource_id": "leaky-bucket",
            "config": {
                "public_access_prevention": "inherited",
                "uniform_bucket_level_access": False,
            },
            "verification_tier": "VERIFIED",
        },
        # 3. Non-Compliant VPC-SC Perimeter (A.8.12)
        {
            "target_control": "ISO/IEC 27001:2022 A.8.12",
            "resource_type": "vpc_sc_perimeter",
            "resource_id": "accessPolicies/123/servicePerimeters/dev_perimeter",
            "config": {
                "enforced": False,  # Dry run
                "restricted_services": ["compute.googleapis.com"],
            },
            "verification_tier": "TELEMETRY",
        },
        # 4. Compliant Monitoring (A.8.16)
        {
            "target_control": "ISO/IEC 27001:2022 A.8.16",
            "resource_type": "logging_pipeline",
            "resource_id": "prod-project-xyz",
            "config": {
                "sinks": [{"destination": "bigquery.googleapis.com/p/d"}],
                "data_access_logs_enabled": True,
                "retention_days": 365,
                "alert_policies": ["iam_change", "firewall_change", "kms_destruction"],
            },
            "verification_tier": "VERIFIED",
        },
    ]

    report = ci_engine.execute_proactive_audit_cycle(cycle_id="cycle-alpha", cloud_assets=cloud_assets)

    assert report["cycle_id"] == "cycle-alpha"
    assert report["organization_name"] == "Global-Bank"
    assert report["findings_count"] == 4
    assert report["scorecard"]["compliant_count"] == 2
    assert report["scorecard"]["non_compliant_count"] == 2
    assert report["scorecard"]["overall_score"] == 50.0

    # Verify remediation plans were generated for the 2 non-compliant assets
    assert len(report["remediation_plans"]) == 2
    assert any(p["resource_id"] == "leaky-bucket" for p in report["remediation_plans"])
    assert any("accessPolicies/123" in p["resource_id"] for p in report["remediation_plans"])

    # Verify Evidence Graph Summary
    assert report["evidence_graph_summary"]["total_evidence_nodes"] == 4
    assert report["evidence_graph_summary"]["compliant_links"] == 2
    assert report["evidence_graph_summary"]["non_compliant_links"] == 2
