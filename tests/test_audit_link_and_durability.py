"""Tests for questionnaire link generation, guest scoping, verification workflow, and Firestore durability."""

import json
import os
import time
import datetime
from unittest.mock import patch
import pytest
from fastapi.testclient import TestClient

from mcp_server_grc.server import app
from mcp_server_grc.auth import require_questionnaire_authorized_user
from mcp_server_grc.firestore_storage import (
    save_questionnaire_token,
    get_questionnaire_token,
    save_client_to_store,
    load_onboarded_clients_from_store,
    save_questionnaire_answer_to_store,
    load_questionnaire_answers_from_store,
    save_evidence_node_to_store,
    load_evidence_nodes_from_store,
)
from agent_orchestrator.evidence_graph import EvidenceVerificationTier
from mcp_server_grc.questionnaire import QUESTIONNAIRE_ANSWERS

client = TestClient(app)
AUTH_HEADER = {"Authorization": "Bearer ya29.lead-auditor-valid-token"}


import copy

@pytest.fixture(autouse=True)
def enable_dev_auth(monkeypatch):
    monkeypatch.setenv("ALLOW_DEV_AUTH_BYPASS", "true")
    orig_answers = copy.deepcopy(QUESTIONNAIRE_ANSWERS)
    from mcp_server_grc.portal import get_client_ci_engine
    engine = get_client_ci_engine("altostrat-ventures")
    orig_links = list(engine.evidence_graph.links)
    orig_nodes = dict(engine.evidence_graph.nodes)
    yield
    QUESTIONNAIRE_ANSWERS.clear()
    QUESTIONNAIRE_ANSWERS.update(orig_answers)
    engine.evidence_graph.links = orig_links
    engine.evidence_graph.nodes = orig_nodes


def test_client_questionnaire_link_generation_and_access():
    """Generates scoped link for client and validates isolated HTML and API access."""
    res = client.post(
        "/api/clients/altostrat-ventures/questionnaire_link",
        json={"expires_in_days": 5, "recipient_email": "ciso@altostrat.corp"},
        headers=AUTH_HEADER,
    )
    assert res.status_code == 200, res.text
    data = res.json()
    assert data["status"] == "success"
    assert data["client_id"] == "altostrat-ventures"
    token = data["token"]
    assert token.startswith("qlink_")
    assert "/portal/client_questionnaire?token=" in data["link"]

    # Access minimal isolated HTML page with token
    html_res = client.get(f"/portal/client_questionnaire?token={token}")
    assert html_res.status_code == 200
    assert "Portal de Auto-Declaração & Evidências" in html_res.text
    assert "altostrat-ventures" in html_res.text
    # Ensure no admin/chat navigation leaked into minimal page
    assert 'id="chatInputHero"' not in html_res.text
    assert 'id="clientDropdownMenu"' not in html_res.text

    # Access API questionnaire with token
    api_res = client.get(f"/api/questionnaire?framework=ISO27001:2022", headers={"X-Questionnaire-Token": token})
    assert api_res.status_code == 200
    quest_data = api_res.json()
    assert quest_data["total_controls"] == 93
    # Check that can_verify_scan is populated correctly
    a515 = next((c for c in quest_data["controls"] if c["id"] == "A.5.15"), None)
    assert a515 is not None
    assert a515["can_verify_scan"] is True
    a61 = next((c for c in quest_data["controls"] if c["id"] == "A.6.1"), None)
    assert a61 is not None
    assert a61["can_verify_scan"] is False


def test_guest_token_cannot_access_operator_routes():
    """Validates that a guest client questionnaire token cannot access operator chat or audit routes."""
    res = client.post(
        "/api/clients/altostrat-ventures/questionnaire_link",
        json={"expires_in_days": 3},
        headers=AUTH_HEADER,
    )
    token = res.json()["token"]
    guest_header = {"X-Questionnaire-Token": token}

    # Attempt chat
    chat_res = client.post(
        "/api/chat",
        json={"message": "Assess GCP compliance", "history": []},
        headers=guest_header,
    )
    assert chat_res.status_code == 401

    # Attempt phased audit
    audit_res = client.post("/api/audit/run_phases", headers=guest_header)
    assert audit_res.status_code == 401


def test_expired_questionnaire_link_rejected():
    """Validates that expired tokens are immediately rejected with HTTP 401."""
    past_date = (datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=2)).isoformat()
    token_rec = {
        "token": "qlink_expired_test_token_12345",
        "client_id": "altostrat-ventures",
        "expires_at": past_date,
        "status": "active",
        "recipient_email": "guest@test.corp",
    }
    save_questionnaire_token(token_rec)

    # HTML page
    html_res = client.get("/portal/client_questionnaire?token=qlink_expired_test_token_12345")
    assert html_res.status_code == 401
    assert "Expirado" in html_res.text

    # API call
    api_res = client.get("/api/questionnaire", headers={"X-Questionnaire-Token": "qlink_expired_test_token_12345"})
    assert api_res.status_code == 401


def test_guest_answer_marked_self_attested():
    """Validates that answers submitted via guest questionnaire link are tagged as SELF_ATTESTED."""
    res = client.post(
        "/api/clients/altostrat-ventures/questionnaire_link",
        json={"expires_in_days": 1},
        headers=AUTH_HEADER,
    )
    token = res.json()["token"]

    ans_res = client.post(
        "/api/questionnaire/A.5.1/answer",
        json={
            "control_id": "A.5.1",
            "framework": "ISO27001:2022",
            "status": "COMPLIANT",
            "justification": "Política aprovada formalmente pela diretoria em reunião anual.",
            "evidence_uri": "https://drive.google.com/open?id=test-pol",
        },
        headers={"X-Questionnaire-Token": token},
    )
    assert ans_res.status_code == 200
    ans_data = ans_res.json()
    assert ans_data["verification_tier"] == EvidenceVerificationTier.SELF_ATTESTED.value
    assert ans_data["status"] == "COMPLIANT"


def test_verify_scan_rejects_unsupported_controls():
    """Validates that verify_scan returns HTTP 400 for controls without live cloud_inspector capability."""
    res = client.post(
        "/api/questionnaire/A.6.1/verify_scan",
        headers=AUTH_HEADER,
    )
    assert res.status_code == 400
    assert "does not have a live automated inspection mapping" in res.json()["detail"]


def test_verify_scan_and_confirmation_workflow():
    """Validates that verify_scan sets status to VERIFICAR and requires human confirmation to finalize."""
    from mcp_server_grc import cloud_inspector

    with patch.object(cloud_inspector, "inspect_project_iam_policy", return_value={
        "status": "COMPLIANT",
        "violations": [],
        "overprivileged_bindings_count": 0,
        "scanned_members_count": 12,
    }):
        # Trigger scan
        scan_res = client.post(
            "/api/questionnaire/A.5.15/verify_scan",
            headers=AUTH_HEADER,
        )
        assert scan_res.status_code == 200
        scan_data = scan_res.json()
        assert scan_data["status"] == "VERIFICAR"
        assert "VERIFICAR" in scan_data["justification"]
        assert scan_data["verification_tier"] == EvidenceVerificationTier.TELEMETRY.value

        # Attempt to confirm with invalid decision
        bad_confirm = client.post(
            "/api/questionnaire/A.5.15/confirm_verification",
            json={"decision": "MAYBE"},
            headers=AUTH_HEADER,
        )
        assert bad_confirm.status_code == 400

        # Confirm compliance explicitly
        confirm_res = client.post(
            "/api/questionnaire/A.5.15/confirm_verification",
            json={"decision": "COMPLIANT", "justification": "Auditor reviewed live IAM bindings and verified least privilege."},
            headers=AUTH_HEADER,
        )
        assert confirm_res.status_code == 200
        confirmed_data = confirm_res.json()
        assert confirmed_data["status"] == "COMPLIANT"
        assert "Confirmed as COMPLIANT" in confirmed_data["justification"]

        # Attempting to confirm again when no longer in VERIFICAR status should fail
        repeat_res = client.post(
            "/api/questionnaire/A.5.15/confirm_verification",
            json={"decision": "COMPLIANT"},
            headers=AUTH_HEADER,
        )
        assert repeat_res.status_code == 400
        assert "not 'VERIFICAR'" in repeat_res.json()["detail"]


def test_scorecard_category_breakdown():
    """Validates that calculate_scorecard_data computes honest real category breakdown for A.5, A.6, A.7, A.8."""
    res = client.get("/api/scorecard", headers=AUTH_HEADER)
    assert res.status_code == 200
    data = res.json()

    assert "category_breakdown" in data
    breakdown = data["category_breakdown"]
    for cat in ("A.5", "A.6", "A.7", "A.8"):
        assert cat in breakdown
        info = breakdown[cat]
        assert info["total"] > 0
        assert 0.0 <= info["percentage"] <= 100.0
        assert info["compliant"] + info["non_compliant"] <= info["total"]


def test_firestore_durability_and_local_fallback():
    """Validates Firestore persistence functions and safe fallback to local JSON stores."""
    # Test client storage
    test_client = {
        "client_id": "durability-test-client",
        "name": "Durability Test Inc",
        "status": "active",
        "projects": ["proj-123"],
    }
    save_client_to_store(test_client)
    loaded_clients = load_onboarded_clients_from_store()
    found = next((c for c in loaded_clients if c.get("client_id") == "durability-test-client"), None)
    assert found is not None
    assert found["name"] == "Durability Test Inc"

    # Test questionnaire answer storage
    ans_data = {
        "control_id": "A.5.23",
        "framework": "ISO27001:2022",
        "status": "COMPLIANT",
        "justification": "GCS buckets verified with Uniform Bucket Level Access enabled.",
    }
    save_questionnaire_answer_to_store("ISO27001:2022", "A.5.23", ans_data)
    loaded_answers = load_questionnaire_answers_from_store()
    assert ("ISO27001:2022", "A.5.23") in loaded_answers

    # Test evidence node storage
    node_data = {
        "node_id": "ev-test-node-1",
        "control_id": "A.5.23",
        "verification_tier": "telemetry",
        "evidence_hash": "abc123hash",
    }
    save_evidence_node_to_store(node_data)
    loaded_nodes = load_evidence_nodes_from_store()
    assert any(n.get("node_id") == "ev-test-node-1" for n in loaded_nodes)

    # Clean up test client
    from mcp_server_grc.firestore_storage import delete_client_from_store
    delete_client_from_store("durability-test-client")
