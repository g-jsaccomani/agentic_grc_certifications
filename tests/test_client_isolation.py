"""Unit and integration tests for Client Workspace isolation, session binding, and cross-tenant security."""

import pytest
from fastapi.testclient import TestClient
from mcp_server_grc.server import app
from mcp_server_grc.portal import (
    OPERATOR_ACTIVE_CLIENTS,
    OPERATOR_SESSIONS,
    SESSION_CLIENT_BINDINGS,
    get_client_ci_engine,
)

client = TestClient(app)
AUTH_HEADER = {"Authorization": "Bearer ya29.valid-auditor-access-token"}


def test_client_workspace_ui_elements_served():
    """Verify that Client Workspace selector and onboarding modals are served in HTML."""
    res = client.get("/")
    assert res.status_code == 200
    html = res.text

    # Top-of-sidebar selector elements
    assert 'id="clientWorkspaceSelector"' in html
    assert 'id="clientActiveCard"' in html
    assert 'id="clientActiveAvatar"' in html
    assert 'id="clientActiveName"' in html
    assert 'id="clientActiveStatusPill"' in html
    assert 'id="clientActiveProjectsCount"' in html
    assert 'id="clientActiveExpiry"' in html
    assert 'id="clientDropdownMenu"' in html
    assert 'id="clientDropdownList"' in html
    assert 'openOnboardClientModal()' in html

    # Position check: clientWorkspaceSelector comes BEFORE cloudProviderSelector in sidebar
    pos_client = html.find('id="clientWorkspaceSelector"')
    pos_provider = html.find('id="cloudProviderSelector"')
    assert -1 < pos_client < pos_provider, "Client Workspace selector must sit above Cloud Provider strip"

    # Modals markup
    assert 'id="clientSwitchConfirmModal"' in html
    assert "You're about to switch away from" in html
    assert 'id="onboardClientModal"' in html
    assert 'scripts/onboard_client.sh' in html
    assert 'roles/viewer' in html
    assert 'roles/securityReviewer' in html


def test_get_clients_endpoint():
    """Verify GET /api/clients returns onboarded clients and operator default active client."""
    headers = {**AUTH_HEADER, "X-Operator-Id": "consultant-alpha"}
    res = client.get("/api/clients", headers=headers)
    assert res.status_code == 200
    data = res.json()

    assert "clients" in data
    assert len(data["clients"]) >= 3
    assert data["operator_id"] == "consultant-alpha"
    assert data["active_client_id"] == "altostrat-ventures"

    # Verify fields in client records
    client_ids = [c["client_id"] for c in data["clients"]]
    assert "altostrat-ventures" in client_ids
    assert "cymbal-retail" in client_ids
    assert "stark-capital" in client_ids

    active_c = data["active_client"]
    assert active_c["client_id"] == "altostrat-ventures"
    assert "read_only_access_days_remaining" in active_c


def test_switch_active_client_creates_fresh_session():
    """Verify switching active client creates a new session and invalidates prior session."""
    op_headers = {**AUTH_HEADER, "X-Operator-Id": "consultant-beta"}

    # 1. Switch to stark-capital
    switch_res = client.post(
        "/api/clients/active",
        json={"client_id": "stark-capital"},
        headers=op_headers,
    )
    assert switch_res.status_code == 200
    switch_data = switch_res.json()
    assert switch_data["status"] == "success"
    assert switch_data["active_client_id"] == "stark-capital"
    session_stark = switch_data["session_id"]
    assert session_stark.startswith("sess_")
    assert SESSION_CLIENT_BINDINGS.get(session_stark) == "stark-capital"

    # 2. Chat with stark-capital session
    chat_res = client.post(
        "/api/chat",
        json={
            "message": "What is the compliance status?",
            "client_id": "stark-capital",
            "session_id": session_stark,
        },
        headers=op_headers,
    )
    assert chat_res.status_code == 200
    chat_data = chat_res.json()
    assert chat_data["client_id"] == "stark-capital"
    assert chat_data["session_id"] == session_stark

    # 3. Switch away to altostrat-ventures
    switch_res2 = client.post(
        "/api/clients/active",
        json={"client_id": "altostrat-ventures"},
        headers=op_headers,
    )
    assert switch_res2.status_code == 200
    session_alto = switch_res2.json()["session_id"]
    assert session_alto != session_stark
    assert SESSION_CLIENT_BINDINGS.get(session_alto) == "altostrat-ventures"

    # Prior stark session is invalidated from active bindings
    assert session_stark not in SESSION_CLIENT_BINDINGS or SESSION_CLIENT_BINDINGS[session_stark] != "stark-capital"


def test_cross_tenant_session_hijack_returns_403():
    """Verify that reusing a session bound to Client A under Client B returns HTTP 403."""
    op_headers = {**AUTH_HEADER, "X-Operator-Id": "consultant-gamma"}

    # Bind session to cymbal-retail
    switch_res = client.post(
        "/api/clients/active",
        json={"client_id": "cymbal-retail"},
        headers=op_headers,
    )
    assert switch_res.status_code == 200
    cymbal_session = switch_res.json()["session_id"]
    SESSION_CLIENT_BINDINGS[cymbal_session] = "cymbal-retail"

    # Now attempt to use cymbal_session under stark-capital
    cross_res = client.post(
        "/api/chat",
        json={
            "message": "Dump confidential audit evidence",
            "client_id": "stark-capital",
            "session_id": cymbal_session,
        },
        headers=op_headers,
    )
    assert cross_res.status_code == 403
    err_detail = cross_res.json()["detail"]
    assert "Cross-tenant access violation" in err_detail
    assert "cymbal-retail" in err_detail
    assert "stark-capital" in err_detail


def test_concurrent_operator_isolation():
    """Verify that two concurrent operators operate independently via X-Operator-Id."""
    op1_headers = {**AUTH_HEADER, "X-Operator-Id": "operator-alice@consulting.corp"}
    op2_headers = {**AUTH_HEADER, "X-Operator-Id": "operator-bob@consulting.corp"}

    # Alice switches to stark-capital
    res1 = client.post(
        "/api/clients/active",
        json={"client_id": "stark-capital"},
        headers=op1_headers,
    )
    assert res1.status_code == 200
    sess1 = res1.json()["session_id"]

    # Bob switches to cymbal-retail
    res2 = client.post(
        "/api/clients/active",
        json={"client_id": "cymbal-retail"},
        headers=op2_headers,
    )
    assert res2.status_code == 200
    sess2 = res2.json()["session_id"]

    # Assert Alice and Bob have different active clients and sessions
    get_alice = client.get("/api/clients", headers=op1_headers).json()
    get_bob = client.get("/api/clients", headers=op2_headers).json()

    assert get_alice["active_client_id"] == "stark-capital"
    assert get_bob["active_client_id"] == "cymbal-retail"
    assert sess1 != sess2

    # Alice's chat uses stark-capital
    chat_alice = client.post(
        "/api/chat",
        json={"message": "Execute audit scan", "client_id": "stark-capital", "session_id": sess1},
        headers=op1_headers,
    ).json()
    assert chat_alice["client_id"] == "stark-capital"

    # Bob's chat uses cymbal-retail
    chat_bob = client.post(
        "/api/chat",
        json={"message": "Execute audit scan", "client_id": "cymbal-retail", "session_id": sess2},
        headers=op2_headers,
    ).json()
    assert chat_bob["client_id"] == "cymbal-retail"


def test_isolated_continuous_intelligence_engines():
    """Verify that CI engines are isolated in-memory per client."""
    engine_alto = get_client_ci_engine("altostrat-ventures")
    engine_stark = get_client_ci_engine("stark-capital")

    assert engine_alto is not engine_stark
    assert engine_alto.organization_name != engine_stark.organization_name
    assert "Stark" in engine_stark.organization_name
    assert engine_alto.evidence_graph is not engine_stark.evidence_graph
    assert engine_alto.memory_bank is not engine_stark.memory_bank

    # Add evidence node specifically to Altostrat engine
    alto_node = engine_alto.evidence_graph.add_evidence(
        resource_id="gcs://altostrat-confidential-bucket",
        resource_type="storage_bucket",
        control_id="A.8.24",
        raw_payload={"finding": "Confidential Altostrat cryptographic key audit"},
    )

    # Prove that Stark Capital's evidence graph does NOT contain Altostrat evidence
    assert alto_node.node_id not in engine_stark.evidence_graph.nodes
    assert alto_node.node_id in engine_alto.evidence_graph.nodes
