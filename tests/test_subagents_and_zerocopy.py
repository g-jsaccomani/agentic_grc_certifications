"""Unit tests for Zero-Copy Connectors and Specialized Sub-Agents."""

import pytest
from agent_orchestrator.zero_copy_connector import (
    ConnectorSource,
    ZeroCopyConnectorManager,
)
from agent_orchestrator.subagents.annex_a_agent import AnnexASubAgent
from agent_orchestrator.subagents.gcp_telemetry_agent import GCPTelemetrySubAgent
from agent_orchestrator.subagents.org_policies_agent import OrgPoliciesSubAgent
from agent_orchestrator.subagents.horizon_scanner_agent import HorizonScannerSubAgent


def test_zero_copy_connectors_privacy_and_access():
    manager = ZeroCopyConnectorManager(idp_tenant_id="enterprise-tenant-1")

    # Attempt query without delegated token -> blocked (returns empty)
    docs_unauth = manager.query_source(
        source=ConnectorSource.GOOGLE_DRIVE,
        query="KMS",
        delegated_user_token=None,
    )
    assert len(docs_unauth) == 0

    # Query with delegated token -> real-time Zero-Copy access
    docs = manager.query_source(
        source=ConnectorSource.GOOGLE_DRIVE,
        query="KMS",
        delegated_user_token="valid-delegated-oauth-bearer",
    )
    assert len(docs) > 0
    doc = docs[0]
    assert doc.cached_externally is False  # Zero-Copy guarantee
    assert "POL-SEC-001" in doc.title
    assert "A.8.24" in doc.content_snippet


def test_annex_a_subagent_cryptography_and_dev():
    agent = AnnexASubAgent()

    # 1. Test A.8.24 Cryptography
    good_kms = {"rotation_period_seconds": 5184000, "protection_level": "HSM", "require_hsm": True}
    res_crypto_ok = agent.audit_cryptography_a824("key-prod", good_kms)
    assert res_crypto_ok["status"] == "COMPLIANT"

    bad_kms = {"rotation_period_seconds": 15552000, "protection_level": "SOFTWARE", "require_hsm": True}
    res_crypto_bad = agent.audit_cryptography_a824("key-legacy", bad_kms)
    assert res_crypto_bad["status"] == "NON_COMPLIANT"
    assert len(res_crypto_bad["violations"]) == 2

    # 2. Test A.8.28 Secure Development
    good_repo = {"sast_enabled": True, "branch_protection_enforced": True, "signed_commits_required": True}
    res_dev_ok = agent.audit_secure_development_a828("repo-core-engine", good_repo)
    assert res_dev_ok["status"] == "COMPLIANT"

    bad_repo = {"sast_enabled": False, "branch_protection_enforced": False, "signed_commits_required": False}
    res_dev_bad = agent.audit_secure_development_a828("repo-ad-hoc", bad_repo)
    assert res_dev_bad["status"] == "NON_COMPLIANT"
    assert len(res_dev_bad["violations"]) == 3


def test_gcp_telemetry_subagent_batch_scan():
    agent = GCPTelemetrySubAgent()
    assets = [
        {
            "type": "gcs_bucket",
            "name": "prod-assets-bucket",
            "config": {"public_access_prevention": "enforced", "uniform_bucket_level_access": True},
        },
        {
            "type": "vpc_sc_perimeter",
            "name": "accessPolicies/1/servicePerimeters/prod_perimeter",
            "config": {"enforced": True, "restricted_services": ["storage.googleapis.com", "bigquery.googleapis.com"]},
        },
    ]
    report = agent.scan_project_infrastructure("prod-project", assets)
    assert report["project_id"] == "prod-project"
    assert report["total_assets_scanned"] == 2
    assert all(f["status"] == "COMPLIANT" for f in report["findings"])


def test_org_policies_subagent_cross_referencing():
    agent = OrgPoliciesSubAgent()
    tech_finding = {
        "control": "ISO/IEC 27001:2022 A.5.23",
        "status": "COMPLIANT",
        "violations": [],
    }
    analysis = agent.cross_reference_policy_with_tech_state(
        policy_keyword="cloud security",
        technical_finding=tech_finding,
        user_token="valid-token",
    )
    assert analysis["policy_implementation_aligned"] is True
    assert "Google Drive (Zero-Copy)" in analysis["policy_grounding"]["source"]


def test_horizon_scanner_subagent():
    agent = HorizonScannerSubAgent()
    updates = agent.scan_regulatory_updates(framework="ISO/IEC 27001")
    assert len(updates) >= 2
    climate_update = updates[0]
    assert "Amd 1:2024" in climate_update["standard"]

    proposal = agent.generate_policy_amendment_proposal(
        regulatory_update=climate_update,
        internal_policy_text="Current policy...",
    )
    assert proposal["status"] == "DRAFT_AWAITING_HUMAN_APPROVAL"
    assert "Aditamento" in proposal["proposed_amendment_text"]
