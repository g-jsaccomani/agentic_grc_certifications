"""
Dedicated anti-fabrication guardrail suite.

This file exists because the same fabrication pattern has been introduced into
build_scan_results_for_phase() / run_phased_audit()'s Phase 3 handling THREE
times: hardcoding COMPLIANT results (with a fake "TELEMETRY" verification tier
and narrative evidence_text) for governance/people controls — A.5.1, A.5.5,
A.5.7, A.5.9, A.5.24, A.5.31 — that have NO corresponding real function in
cloud_inspector.py. Each time it was caught by tests and reverted, and each
time it came back.

Contains ONLY checks in this one class: "no synced/reported control result
may exist without a real, traceable, currently-implemented cloud_inspector.py
function behind it." Do not add unrelated test coverage here — put it in
test_questionnaire.py, test_portal.py, or test_client_isolation.py instead.

If you are an engineer (human or AI) about to add a new control result to
build_scan_results_for_phase() or to the Phase 3 block of run_phased_audit():
first add the real inspection function to cloud_inspector.py, wire it in with
error handling identical to the existing Phase 1/2 checks, and only then
extend the whitelist (KNOWN_AUTOMATED_CONTROLS) in this file. If you cannot
do that, the control stays unanswered and self-attested via the questionnaire
— that is not a bug, it is the honesty guarantee this file protects.
"""
import inspect
import re

import pytest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient

from mcp_server_grc.server import app
from mcp_server_grc.cloud_inspector import reset_session_call_budget
from mcp_server_grc import cloud_inspector as cloud_inspector_module
from mcp_server_grc import portal as portal_module

client = TestClient(app)
AUTH_HEADER = {"Authorization": "Bearer ya29.valid-auditor-access-token"}

# The exhaustive, explicit whitelist of controls that are allowed to be
# auto-answered, each mapped to the real cloud_inspector.py function that
# backs it. Extending this list requires adding the real function first.
KNOWN_AUTOMATED_CONTROLS = {
    "A.5.15": "inspect_project_iam_policy",
    "A.5.18": "inspect_project_iam_policy",
    "A.5.23": "inspect_cloud_storage_bucket",
    "A.8.20": "inspect_cloud_run_services",
    "A.8.24": "inspect_cloud_kms_key",
}

# Controls previously fabricated (Phase 3 governance/people controls) that
# must NEVER be auto-answered because no real check exists for them.
FABRICATED_CONTROL_IDS = ["A.5.1", "A.5.5", "A.5.7", "A.5.9", "A.5.24", "A.5.31"]


def test_every_known_automated_control_maps_to_a_real_cloud_inspector_function():
    """Structural check: every function named in KNOWN_AUTOMATED_CONTROLS must actually
    exist in cloud_inspector.py. If this fails, the whitelist itself has drifted from reality.
    """
    for control_id, func_name in KNOWN_AUTOMATED_CONTROLS.items():
        assert hasattr(cloud_inspector_module, func_name), (
            f"Control {control_id} claims to be backed by cloud_inspector.{func_name}, "
            f"but no such function exists."
        )


def test_fabricated_control_ids_have_no_real_cloud_inspector_function():
    """None of the previously-fabricated Phase 3 governance control IDs may appear in the
    automated whitelist, and cloud_inspector.py must not define a function for them.
    """
    for cid in FABRICATED_CONTROL_IDS:
        assert cid not in KNOWN_AUTOMATED_CONTROLS, (
            f"Control {cid} was added to the automated whitelist without a real check — "
            f"this is the exact fabrication regression this file exists to prevent."
        )


def test_build_scan_results_source_never_hardcodes_compliant_for_fabricated_controls():
    """Static/structural guardrail on build_scan_results_for_phase() source code itself.

    Even if a future change bypasses the dynamic mocking below (e.g. by fabricating results
    outside the phase loops this test mocks), a hardcoded 'control_id': 'A.5.1' (etc.) literal
    paired with a hardcoded COMPLIANT status inside this function's source is exactly the
    fabrication pattern that has regressed twice. Fail fast on the source text itself.
    """
    source = inspect.getsource(portal_module.build_scan_results_for_phase)
    for cid in FABRICATED_CONTROL_IDS:
        # A control id like "A.5.1" is a substring of "A.5.15"/"A.5.18", so require it not be
        # immediately followed by another digit (which would make it a *different* control id).
        pattern = re.compile(re.escape(cid) + r"(?!\d)")
        assert not pattern.search(source), (
            f"build_scan_results_for_phase() source references fabricated control {cid} — "
            f"this control has no real cloud_inspector.py function and must never be "
            f"hardcoded into scan results. See the module docstring of this test file."
        )


def test_run_phased_audit_source_never_hardcodes_compliant_for_fabricated_controls():
    """Same static guardrail as above, applied to the Phase 3 block inside run_phased_audit()
    (the /api/audit/run_phases endpoint), which is a separate code path from
    build_scan_results_for_phase() and fabricated the same controls independently.
    """
    source = inspect.getsource(portal_module.run_phased_audit)
    for cid in FABRICATED_CONTROL_IDS:
        pattern = re.compile(re.escape(cid) + r"(?!\d)")
        assert not pattern.search(source), (
            f"run_phased_audit() source references fabricated control {cid} in its Phase 3 "
            f"reporting — this control has no real cloud_inspector.py function and must never "
            f"be hardcoded into the phased audit response."
        )
    assert '"status": "NOT_AUTOMATABLE"' in source or "'status': 'NOT_AUTOMATABLE'" in source, (
        "run_phased_audit() must report Phase 3 governance/people controls as NOT_AUTOMATABLE, "
        "not as a completed automated evaluation."
    )


def test_build_scan_results_for_phase_never_returns_fabricated_controls_even_with_full_mocking():
    """Dynamic guardrail: call build_scan_results_for_phase() directly with every real
    cloud_inspector.py function mocked to return a fully COMPLIANT result, across all 4
    phases. Assert the returned control_id set is an exact subset of the whitelist, and
    specifically excludes every previously-fabricated control.
    """
    reset_session_call_budget()
    mock_iam = MagicMock(return_value={
        "status": "SUCCESS", "project_id": "test-proj", "total_bindings": 5,
        "compliance": {"status": "COMPLIANT", "violations": []},
    })
    mock_storage = MagicMock(return_value={
        "status": "FOUND", "compliance": {"status": "COMPLIANT", "violations": []},
    })
    mock_kms = MagicMock(return_value={
        "status": "FOUND", "compliance": {"status": "COMPLIANT", "violations": []},
    })
    mock_run = MagicMock(return_value={
        "status": "SUCCESS", "compliance": {"status": "COMPLIANT", "violations": []},
    })

    with patch("mcp_server_grc.cloud_inspector.inspect_project_iam_policy", mock_iam), \
         patch("mcp_server_grc.cloud_inspector.inspect_cloud_storage_bucket", mock_storage), \
         patch("mcp_server_grc.cloud_inspector.inspect_cloud_kms_key", mock_kms), \
         patch("mcp_server_grc.cloud_inspector.inspect_cloud_run_services", mock_run):
        results = portal_module.build_scan_results_for_phase(
            target_phase=None,
            projects=["test-proj"],
        )

    returned_ids = {r["control_id"] for r in results}
    assert returned_ids.issubset(set(KNOWN_AUTOMATED_CONTROLS.keys())), (
        f"build_scan_results_for_phase() returned control(s) outside the known-automated "
        f"whitelist: {returned_ids - set(KNOWN_AUTOMATED_CONTROLS.keys())}"
    )
    for cid in FABRICATED_CONTROL_IDS:
        assert cid not in returned_ids, (
            f"build_scan_results_for_phase() fabricated a result for {cid} with no real "
            f"cloud_inspector.py check behind it."
        )


def test_run_phases_endpoint_phase3_is_never_completed_with_synthetic_compliance():
    """End-to-end guardrail on the live /api/audit/run_phases endpoint: Phase 3 must always
    report NOT_AUTOMATABLE with no compliance_score, regardless of what Phase 1/2 cloud
    inspection returns, and no fabricated control may be synced into the questionnaire.
    """
    # Use a dedicated, isolated client rather than the default/shared demo client — this scan
    # writes questionnaire answers, FinOps usage, and evidence-graph links that must not perturb
    # the shared altostrat-ventures demo state other tests depend on.
    reset_session_call_budget()
    op_headers = {**AUTH_HEADER, "X-Operator-Id": "consultant-anti-fabrication-guardrail"}
    isolated_cid = "anti-fabrication-guardrail-client"
    client.post(
        "/api/clients/onboard",
        json={"name": "Guardrail Test Co", "client_id": isolated_cid, "projects": ["test-proj"], "days": 30, "is_shared": True},
        headers=op_headers,
    )
    client_headers = {**op_headers, "X-Client-Id": isolated_cid}
    try:
        mock_iam = MagicMock(return_value={
            "status": "SUCCESS", "project_id": "test-proj", "total_bindings": 5,
            "compliance": {"status": "COMPLIANT", "violations": []},
        })
        mock_storage = MagicMock(return_value={
            "status": "FOUND", "compliance": {"status": "COMPLIANT", "violations": []},
        })
        mock_kms = MagicMock(return_value={
            "status": "FOUND", "compliance": {"status": "COMPLIANT", "violations": []},
        })
        mock_run = MagicMock(return_value={
            "status": "SUCCESS", "compliance": {"status": "COMPLIANT", "violations": []},
        })

        with patch("mcp_server_grc.cloud_inspector.inspect_project_iam_policy", mock_iam), \
             patch("mcp_server_grc.cloud_inspector.inspect_cloud_storage_bucket", mock_storage), \
             patch("mcp_server_grc.cloud_inspector.inspect_cloud_kms_key", mock_kms), \
             patch("mcp_server_grc.cloud_inspector.inspect_cloud_run_services", mock_run):
            res = client.post(
                "/api/audit/run_phases",
                json={"projects": ["test-proj"]},
                headers=client_headers,
            )
        assert res.status_code == 200
        data = res.json()

        phase3 = next(p for p in data["phases"] if p["phase"].startswith("Phase 3"))
        assert phase3["status"] == "NOT_AUTOMATABLE"
        assert phase3.get("compliance_score") is None
        assert "controls_tested" not in phase3

        q_res = client.get("/api/questionnaire?framework=ISO27001:2022", headers=client_headers)
        answered_ids = {c["id"] for c in q_res.json()["controls"] if c.get("answer") is not None}
        for cid in FABRICATED_CONTROL_IDS:
            assert cid not in answered_ids, (
                f"Fabricated control {cid} was synced to the questionnaire despite having no "
                f"real cloud_inspector.py check."
            )
    finally:
        client.delete(f"/api/clients/{isolated_cid}", headers=op_headers)


def test_no_hardcoded_telemetry_tier_for_fabricated_controls_in_portal_source():
    """Regex guardrail: no line in portal.py may pair a fabricated control_id literal with
    the highest-trust 'TELEMETRY' verification_tier, which is exactly how the fabrication
    presented evidence for controls no real API ever checked.
    """
    source = inspect.getsource(portal_module)
    for cid in FABRICATED_CONTROL_IDS:
        pattern = re.compile(
            r'"control_id"\s*:\s*"' + re.escape(cid) + r'"[\s\S]{0,400}?"verification_tier"\s*:\s*"TELEMETRY"'
        )
        assert not pattern.search(source), (
            f"portal.py hardcodes verification_tier='TELEMETRY' for fabricated control {cid} "
            f"— this is the exact regression pattern this guardrail file exists to catch."
        )
