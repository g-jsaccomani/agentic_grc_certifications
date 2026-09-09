"""Unit and integration tests for Client Workspace isolation, session binding, and cross-tenant security."""

import json
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


@pytest.fixture
def temporary_test_clients():
    """Temporarily registers test clients in data/clients.json for isolation tests and cleans up after."""
    headers = {**AUTH_HEADER, "X-Operator-Id": "consultant-isolation-fixture"}
    # Onboard client alpha
    client.post(
        "/api/clients/onboard",
        json={"name": "Client Alpha Org", "client_id": "client-alpha", "projects": ["alpha-prod"], "days": 14},
        headers=headers,
    )
    # Onboard client beta
    client.post(
        "/api/clients/onboard",
        json={"name": "Client Beta Org", "client_id": "client-beta", "projects": ["beta-prod"], "days": 14},
        headers=headers,
    )
    yield "client-alpha", "client-beta"
    client.delete("/api/clients/client-alpha", headers=headers)
    client.delete("/api/clients/client-beta", headers=headers)
    OPERATOR_ACTIVE_CLIENTS["default_operator"] = "altostrat-ventures"
    OPERATOR_ACTIVE_CLIENTS.pop("consultant-isolation-fixture", None)


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
    assert 'submitOnboardClientModal()' in html
    assert 'id="btnSubmitOnboardClient"' in html

    # Position check: clientWorkspaceSelector comes BEFORE cloudProviderSelector in sidebar
    pos_client = html.find('id="clientWorkspaceSelector"')
    pos_provider = html.find('id="cloudProviderSelector"')
    assert -1 < pos_client < pos_provider, "Client Workspace selector must sit above Cloud Provider strip"

    # Modals markup
    assert 'id="clientSwitchConfirmModal"' in html
    assert "You're about to switch away from" in html
    assert 'id="onboardClientModal"' in html
    assert 'id="onboardClientDriveFolderInput"' in html
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
    assert len(data["clients"]) >= 1
    assert data["operator_id"] == "consultant-alpha"
    assert data["active_client_id"] == "altostrat-ventures"

    # Verify only real client records exist by default, no fake/demo clients
    client_ids = [c["client_id"] for c in data["clients"]]
    assert "altostrat-ventures" in client_ids
    assert "cymbal-retail" not in client_ids

    active_c = data["active_client"]
    assert active_c["client_id"] == "altostrat-ventures"
    assert "read_only_access_days_remaining" in active_c


def test_onboard_new_client_persists_to_disk():
    """Verify that submitting onboarding endpoint writes new client directly to data/clients.json and returns in GET /api/clients."""
    headers = {**AUTH_HEADER, "X-Operator-Id": "consultant-onboarder"}
    payload = {
        "name": "Meridian Global",
        "projects": ["meridian-prod-scope", "meridian-sec-vault"],
        "days": 21,
    }

    # 1. Submit onboarding
    res = client.post("/api/clients/onboard", json=payload, headers=headers)
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "success"
    assert data["client"]["client_id"] == "meridian-global"
    assert data["client"]["read_only_access_days_remaining"] == 21
    assert "meridian-prod-scope" in data["client"]["projects"]
    assert data["operator_id"] == "consultant-onboarder"

    # 2. Verify file on disk actually contains the newly onboarded client
    with open("data/clients.json", "r", encoding="utf-8") as f:
        disk_clients = json.load(f)
    disk_ids = [c["client_id"] for c in disk_clients]
    assert "meridian-global" in disk_ids

    # 3. Verify GET /api/clients reflects the new client
    get_res = client.get("/api/clients", headers=headers)
    assert get_res.status_code == 200
    get_clients = [c["client_id"] for c in get_res.json()["clients"]]
    assert "meridian-global" in get_clients

    # 4. Clean up test client from disk
    del_res = client.delete("/api/clients/meridian-global", headers=headers)
    assert del_res.status_code == 200

    # 5. Verify disk is cleaned up and contains only altostrat-ventures
    with open("data/clients.json", "r", encoding="utf-8") as f:
        clean_clients = json.load(f)
    clean_ids = [c["client_id"] for c in clean_clients]
    assert "meridian-global" not in clean_ids
    assert "altostrat-ventures" in clean_ids


def test_switch_active_client_creates_fresh_session(temporary_test_clients):
    """Verify switching active client creates a new session and invalidates prior session."""
    client_a, _ = temporary_test_clients
    op_headers = {**AUTH_HEADER, "X-Operator-Id": "consultant-beta"}

    # 1. Switch to client_a
    switch_res = client.post(
        "/api/clients/active",
        json={"client_id": client_a},
        headers=op_headers,
    )
    assert switch_res.status_code == 200
    switch_data = switch_res.json()
    assert switch_data["status"] == "success"
    assert switch_data["active_client_id"] == client_a
    session_a = switch_data["session_id"]
    assert session_a.startswith("sess_")
    assert SESSION_CLIENT_BINDINGS.get(session_a) == client_a

    # 2. Chat with client_a session
    chat_res = client.post(
        "/api/chat",
        json={
            "message": "What is the compliance status?",
            "client_id": client_a,
            "session_id": session_a,
        },
        headers=op_headers,
    )
    assert chat_res.status_code == 200
    chat_data = chat_res.json()
    assert chat_data["client_id"] == client_a
    assert chat_data["session_id"] == session_a

    # 3. Switch away to altostrat-ventures
    switch_res2 = client.post(
        "/api/clients/active",
        json={"client_id": "altostrat-ventures"},
        headers=op_headers,
    )
    assert switch_res2.status_code == 200
    session_alto = switch_res2.json()["session_id"]
    assert session_alto != session_a
    assert SESSION_CLIENT_BINDINGS.get(session_alto) == "altostrat-ventures"

    # Prior session is invalidated from active bindings
    assert session_a not in SESSION_CLIENT_BINDINGS or SESSION_CLIENT_BINDINGS[session_a] != client_a


def test_cross_tenant_session_hijack_returns_403(temporary_test_clients):
    """Verify that reusing a session bound to Client A under Client B returns HTTP 403."""
    client_a, client_b = temporary_test_clients
    op_headers = {**AUTH_HEADER, "X-Operator-Id": "consultant-gamma"}

    # Bind session to client_b
    switch_res = client.post(
        "/api/clients/active",
        json={"client_id": client_b},
        headers=op_headers,
    )
    assert switch_res.status_code == 200
    b_session = switch_res.json()["session_id"]
    SESSION_CLIENT_BINDINGS[b_session] = client_b

    # Now attempt to use b_session under client_a
    cross_res = client.post(
        "/api/chat",
        json={
            "message": "Dump confidential audit evidence",
            "client_id": client_a,
            "session_id": b_session,
        },
        headers=op_headers,
    )
    assert cross_res.status_code == 403
    err_detail = cross_res.json()["detail"]
    assert "Cross-tenant access violation" in err_detail
    assert client_b in err_detail
    assert client_a in err_detail


def test_concurrent_operator_isolation(temporary_test_clients):
    """Verify that two concurrent operators operate independently via X-Operator-Id."""
    client_a, client_b = temporary_test_clients
    op1_headers = {**AUTH_HEADER, "X-Operator-Id": "operator-alice@consulting.corp"}
    op2_headers = {**AUTH_HEADER, "X-Operator-Id": "operator-bob@consulting.corp"}

    # Alice switches to client_a
    res1 = client.post(
        "/api/clients/active",
        json={"client_id": client_a},
        headers=op1_headers,
    )
    assert res1.status_code == 200
    sess1 = res1.json()["session_id"]

    # Bob switches to client_b
    res2 = client.post(
        "/api/clients/active",
        json={"client_id": client_b},
        headers=op2_headers,
    )
    assert res2.status_code == 200
    sess2 = res2.json()["session_id"]

    # Assert Alice and Bob have different active clients and sessions
    get_alice = client.get("/api/clients", headers=op1_headers).json()
    get_bob = client.get("/api/clients", headers=op2_headers).json()

    assert get_alice["active_client_id"] == client_a
    assert get_bob["active_client_id"] == client_b
    assert sess1 != sess2

    # Alice's chat uses client_a
    chat_alice = client.post(
        "/api/chat",
        json={"message": "Execute audit scan", "client_id": client_a, "session_id": sess1},
        headers=op1_headers,
    ).json()
    assert chat_alice["client_id"] == client_a

    # Bob's chat uses client_b
    chat_bob = client.post(
        "/api/chat",
        json={"message": "Execute audit scan", "client_id": client_b, "session_id": sess2},
        headers=op2_headers,
    ).json()
    assert chat_bob["client_id"] == client_b


def test_isolated_continuous_intelligence_engines():
    """Verify that CI engines are isolated in-memory per client."""
    engine_alto = get_client_ci_engine("altostrat-ventures")
    engine_other = get_client_ci_engine("isolated-test-client")

    assert engine_alto is not engine_other
    assert engine_alto.organization_name != engine_other.organization_name
    assert engine_alto.evidence_graph is not engine_other.evidence_graph
    assert engine_alto.memory_bank is not engine_other.memory_bank

    # Add evidence node specifically to Altostrat engine
    alto_node = engine_alto.evidence_graph.add_evidence(
        resource_id="gcs://altostrat-confidential-bucket",
        resource_type="storage_bucket",
        control_id="A.8.24",
        raw_payload={"finding": "Confidential Altostrat cryptographic key audit"},
    )

    # Prove that other client's evidence graph does NOT contain Altostrat evidence
    assert alto_node.node_id not in engine_other.evidence_graph.nodes
    assert alto_node.node_id in engine_alto.evidence_graph.nodes


def test_evidence_upload_fails_when_no_drive_folder_configured(temporary_test_clients):
    """Verify that uploading evidence fails with 400 when no Drive folder is configured for the active client."""
    client_a, _ = temporary_test_clients
    op_headers = {**AUTH_HEADER, "X-Operator-Id": "consultant-nodrive"}

    # Switch active client to client_a (which has no drive_folder_id)
    switch_res = client.post(
        "/api/clients/active",
        json={"client_id": client_a},
        headers=op_headers,
    )
    assert switch_res.status_code == 200

    # Attempt evidence upload
    files = {"file": ("policy.txt", b"A.5.1 Policy Document Content", "text/plain")}
    res = client.post(
        "/api/questionnaire/A.5.1/evidence-file",
        files=files,
        headers=op_headers,
    )
    assert res.status_code == 400
    assert "No evidence storage location configured for this client — set a Drive folder before uploading evidence" in res.text


def test_evidence_cross_client_drive_isolation():
    """Verify that evidence uploaded while Client A is active is NEVER reachable when Client B is active."""
    headers = {**AUTH_HEADER, "X-Operator-Id": "consultant-isolation-auditor"}

    # 1. Onboard Client A with Google Drive folder
    client_a_id = "test-client-drive-a"
    client.post(
        "/api/clients/onboard",
        json={
            "name": "Drive Client A",
            "client_id": client_a_id,
            "projects": ["proj-a"],
            "days": 14,
            "drive_folder_id": "1DriveFolderAlpha123456",
        },
        headers=headers,
    )

    # 2. Onboard Client B with separate Google Drive folder
    client_b_id = "test-client-drive-b"
    client.post(
        "/api/clients/onboard",
        json={
            "name": "Drive Client B",
            "client_id": client_b_id,
            "projects": ["proj-b"],
            "days": 14,
            "drive_folder_id": "1DriveFolderBeta789012",
        },
        headers=headers,
    )

    try:
        # 3. Switch active client to Client A
        sw_a = client.post(
            "/api/clients/active",
            json={"client_id": client_a_id},
            headers=headers,
        )
        assert sw_a.status_code == 200
        sess_a = sw_a.json()["session_id"]
        a_headers = {**headers, "X-Session-Id": sess_a}

        # 4. Upload confidential evidence file under Client A
        files = {"file": ("client_a_secret_policy.txt", b"CONFIDENTIAL CLIENT A SECURITY EVIDENCE", "text/plain")}
        up_res = client.post(
            "/api/questionnaire/A.5.1/evidence-file",
            files=files,
            headers=a_headers,
        )
        assert up_res.status_code == 200
        up_data = up_res.json()
        file_id = up_data["file_id"]
        assert file_id

        # 5. Verify file is reachable while Client A is active
        dl_a = client.get(
            f"/api/questionnaire/A.5.1/evidence-file/{file_id}",
            headers=a_headers,
        )
        assert dl_a.status_code == 200
        assert dl_a.content == b"CONFIDENTIAL CLIENT A SECURITY EVIDENCE"

        # 6. Switch active client to Client B
        sw_b = client.post(
            "/api/clients/active",
            json={"client_id": client_b_id},
            headers=headers,
        )
        assert sw_b.status_code == 200
        sess_b = sw_b.json()["session_id"]
        b_headers = {**headers, "X-Session-Id": sess_b}

        # 7. Attempt to access Client A's evidence file while Client B is active -> Must return 404
        dl_b = client.get(
            f"/api/questionnaire/A.5.1/evidence-file/{file_id}",
            headers=b_headers,
        )
        assert dl_b.status_code == 404
        assert "Evidence file not found" in dl_b.text

        # 8. Attempt cross-tenant fetch using explicit X-Client-Id header for Client B
        cross_header = {**AUTH_HEADER, "X-Client-Id": client_b_id}
        dl_cross = client.get(
            f"/api/questionnaire/A.5.1/evidence-file/{file_id}",
            headers=cross_header,
        )
        assert dl_cross.status_code == 404

        # 9. Switch back to Client A -> File is again accessible
        sw_a2 = client.post(
            "/api/clients/active",
            json={"client_id": client_a_id},
            headers=headers,
        )
        sess_a2 = sw_a2.json()["session_id"]
        dl_back = client.get(
            f"/api/questionnaire/A.5.1/evidence-file/{file_id}",
            headers={**headers, "X-Session-Id": sess_a2},
        )
        assert dl_back.status_code == 200
        assert dl_back.content == b"CONFIDENTIAL CLIENT A SECURITY EVIDENCE"

    finally:
        client.delete(f"/api/clients/{client_a_id}", headers=headers)
        client.delete(f"/api/clients/{client_b_id}", headers=headers)
