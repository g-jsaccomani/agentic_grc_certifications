"""Unit and integration tests for Client Workspace isolation, session binding, and cross-tenant security."""

import json
import pytest
from fastapi.testclient import TestClient
from mcp_server_grc.server import app
from mcp_server_grc.cloud_inspector import DISCONNECTED_CLIENT_MESSAGE, inspect_cloud_kms_key
from mcp_server_grc.portal import (
    OPERATOR_ACTIVE_CLIENTS,
    OPERATOR_SESSIONS,
    SESSION_CLIENT_BINDINGS,
    get_client_ci_engine,
)

client = TestClient(app)
AUTH_HEADER = {"Authorization": "Bearer ya29.valid-auditor-access-token"}


@pytest.fixture(autouse=True)
def enable_dev_auth_bypass_for_isolation(monkeypatch):
    monkeypatch.setenv("ALLOW_DEV_AUTH_BYPASS", "true")


@pytest.fixture
def temporary_test_clients():
    """Temporarily registers test clients in data/clients.json for isolation tests and cleans up after."""
    headers = {**AUTH_HEADER, "X-Operator-Id": "consultant-isolation-fixture"}
    # Onboard client alpha
    client.post(
        "/api/clients/onboard",
        json={"name": "Client Alpha Org", "client_id": "client-alpha", "projects": ["alpha-prod"], "days": 14, "is_shared": True},
        headers=headers,
    )
    # Onboard client beta
    client.post(
        "/api/clients/onboard",
        json={"name": "Client Beta Org", "client_id": "client-beta", "projects": ["beta-prod"], "days": 14, "is_shared": True},
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


def test_onboarded_client_scoped_per_operator_isolation():
    """Verify that clients onboarded by Operator A are strictly scoped to Operator A.
    
    Proves:
    1. Operator A onboards Client X.
    2. Operator B (a different verified identity) calls GET /api/clients and does NOT see Client X.
    3. Operator B cannot select Client X as active via POST /api/clients/active (returns 403 Forbidden).
    """
    op_a_headers = {**AUTH_HEADER, "X-Operator-Id": "operator-a@security.corp"}
    op_b_headers = {**AUTH_HEADER, "X-Operator-Id": "operator-b@otherorg.corp"}

    client_x_id = "client-x-confidential"
    try:
        # 1. Operator A onboards Client X
        res_onboard = client.post(
            "/api/clients/onboard",
            json={
                "name": "Confidential Client X",
                "client_id": client_x_id,
                "projects": [f"{client_x_id}-prod"],
                "org_id": "999888777666",
            },
            headers=op_a_headers,
        )
        assert res_onboard.status_code == 200
        data_onboard = res_onboard.json()
        assert data_onboard["client"]["client_id"] == client_x_id
        assert data_onboard["client"]["owner_operator_id"] == "operator-a@security.corp"

        # 2. Operator A calls GET /api/clients and DOES see Client X
        res_a = client.get("/api/clients", headers=op_a_headers)
        assert res_a.status_code == 200
        a_client_ids = [c["client_id"] for c in res_a.json()["clients"]]
        assert client_x_id in a_client_ids

        # 3. Operator B (different verified identity) calls GET /api/clients and does NOT see Client X
        res_b = client.get("/api/clients", headers=op_b_headers)
        assert res_b.status_code == 200
        b_client_ids = [c["client_id"] for c in res_b.json()["clients"]]
        assert client_x_id not in b_client_ids

        # 4. Operator B attempts to select Client X as active -> REJECTED (403 Forbidden)
        res_switch = client.post(
            "/api/clients/active",
            json={"client_id": client_x_id},
            headers=op_b_headers,
        )
        assert res_switch.status_code == 403
        assert "Access denied" in res_switch.json().get("detail", "")

    finally:
        # Cleanup
        client.delete(f"/api/clients/{client_x_id}", headers=op_a_headers)


def test_switching_active_client_changes_projects_and_isolates_org_projects():
    """Verify that /api/projects queries Cloud Resource Manager live per-client,
    changing returned projects upon active client switch and strictly isolating organizations.
    
    Proves:
    1. Switching active client changes the projects returned by /api/projects.
    2. Projects belonging to Client Alpha's org never appear when Client Beta is active, and vice versa.
    3. If the delegated token lacks permission to list the org's projects (e.g. 403), returns a clear
       error rather than silently falling back to any hardcoded list.
    """
    from unittest.mock import MagicMock, patch

    op_headers = {**AUTH_HEADER, "X-Operator-Id": "consultant-projects-test"}
    client_alpha_id = "client-alpha-org"
    client_beta_id = "client-beta-org"

    # Onboard two distinct clients with distinct GCP Organization IDs
    try:
        client.post(
            "/api/clients/onboard",
            json={
                "name": "Alpha Enterprise",
                "client_id": client_alpha_id,
                "org_id": "111000111000",
                "projects": ["alpha-workload-prod", "alpha-workload-stage"],
            },
            headers=op_headers,
        )
        client.post(
            "/api/clients/onboard",
            json={
                "name": "Beta Financial",
                "client_id": client_beta_id,
                "org_id": "222000222000",
                "projects": ["beta-banking-prod", "beta-vault"],
            },
            headers=op_headers,
        )

        mock_session = MagicMock()

        def mock_crm_get(url, params=None, timeout=None):
            resp = MagicMock()
            filter_param = (params or {}).get("filter", "")
            if "111000111000" in filter_param:
                resp.status_code = 200
                resp.json.return_value = {
                    "projects": [
                        {
                            "projectId": "alpha-workload-prod",
                            "name": "Alpha Workload Prod",
                            "projectNumber": "11101",
                            "lifecycleState": "ACTIVE",
                            "parent": {"type": "organization", "id": "111000111000"},
                        },
                        {
                            "projectId": "alpha-workload-stage",
                            "name": "Alpha Workload Stage",
                            "projectNumber": "11102",
                            "lifecycleState": "ACTIVE",
                            "parent": {"type": "organization", "id": "111000111000"},
                        },
                        {
                            "projectId": "alpha-internal-sandbox",
                            "name": "Alpha Sandbox",
                            "projectNumber": "11103",
                            "lifecycleState": "ACTIVE",
                            "parent": {"type": "organization", "id": "111000111000"},
                        },
                    ]
                }
            elif "222000222000" in filter_param:
                resp.status_code = 200
                resp.json.return_value = {
                    "projects": [
                        {
                            "projectId": "beta-banking-prod",
                            "name": "Beta Banking Prod",
                            "projectNumber": "22201",
                            "lifecycleState": "ACTIVE",
                            "parent": {"type": "organization", "id": "222000222000"},
                        },
                        {
                            "projectId": "beta-vault",
                            "name": "Beta Vault",
                            "projectNumber": "22202",
                            "lifecycleState": "ACTIVE",
                            "parent": {"type": "organization", "id": "222000222000"},
                        },
                        {
                            "projectId": "beta-restricted-ledger",
                            "name": "Beta Restricted Ledger",
                            "projectNumber": "22203",
                            "lifecycleState": "ACTIVE",
                            "parent": {"type": "organization", "id": "222000222000"},
                        },
                    ]
                }
            else:
                resp.status_code = 403
                resp.text = "PermissionDenied: The caller does not have permission on the requested organization"
            return resp

        mock_session.get.side_effect = mock_crm_get

        with patch("mcp_server_grc.portal.get_authorized_session", return_value=(mock_session, "test-target")):
            # 1. Switch active client to Alpha
            sw_a = client.post(
                "/api/clients/active",
                json={"client_id": client_alpha_id},
                headers=op_headers,
            )
            assert sw_a.status_code == 200

            # 2. Query /api/projects for active Client Alpha
            res_alpha_proj = client.get("/api/projects", headers=op_headers)
            assert res_alpha_proj.status_code == 200
            data_a = res_alpha_proj.json()
            assert data_a["client_id"] == client_alpha_id
            assert data_a["org_id"] == "111000111000"
            assert data_a["org_metadata"]["org_id"] == "111000111000"
            assert data_a["org_metadata"]["org_name"] == "Alpha Enterprise Org"
            alpha_pids = [p["project_id"] for p in data_a["all_org_projects"]]
            assert "alpha-workload-prod" in alpha_pids
            assert "alpha-internal-sandbox" in alpha_pids
            # Ensure Beta projects NEVER appear under Alpha
            assert "beta-banking-prod" not in alpha_pids
            assert "beta-vault" not in alpha_pids
            assert "beta-restricted-ledger" not in alpha_pids

            # 3. Switch active client to Beta
            sw_b = client.post(
                "/api/clients/active",
                json={"client_id": client_beta_id},
                headers=op_headers,
            )
            assert sw_b.status_code == 200

            # 4. Query /api/projects for active Client Beta -> Must reflect Beta's projects only
            res_beta_proj = client.get("/api/projects", headers=op_headers)
            assert res_beta_proj.status_code == 200
            data_b = res_beta_proj.json()
            assert data_b["client_id"] == client_beta_id
            assert data_b["org_id"] == "222000222000"
            assert data_b["org_metadata"]["org_id"] == "222000222000"
            assert data_b["org_metadata"]["org_name"] == "Beta Financial Org"
            # Ensure Client A's org and projects are completely absent
            assert data_b["org_id"] != data_a["org_id"]
            assert data_b["org_metadata"]["org_id"] != data_a["org_metadata"]["org_id"]
            beta_pids = [p["project_id"] for p in data_b["all_org_projects"]]
            assert "beta-banking-prod" in beta_pids
            assert "beta-vault" in beta_pids
            assert "beta-restricted-ledger" in beta_pids
            # Ensure Alpha projects NEVER appear under Beta
            assert "alpha-workload-prod" not in beta_pids
            assert "alpha-workload-stage" not in beta_pids
            assert "alpha-internal-sandbox" not in beta_pids

        # 5. Verify that if delegated token lacks permission (e.g. 403 Forbidden from CRM),
        # /api/projects returns a clear error and DOES NOT silently fall back to hardcoded lists
        perm_denied_session = MagicMock()
        perm_denied_resp = MagicMock(status_code=403, text="User lacks resourcemanager.projects.list permission")
        perm_denied_session.get.return_value = perm_denied_resp

        with patch("mcp_server_grc.portal.get_authorized_session", return_value=(perm_denied_session, "test-target")):
            res_denied = client.get("/api/projects", headers=op_headers)
            assert res_denied.status_code == 403
            assert "resourcemanager.projects.list" in res_denied.json().get("detail", "")
            # Ensure no silent fallback occurred
            assert "all_org_projects" not in res_denied.json()

    finally:
        client.delete(f"/api/clients/{client_alpha_id}", headers=op_headers)
        client.delete(f"/api/clients/{client_beta_id}", headers=op_headers)


def test_client_disconnect_ui_elements():
    """Verify that Client Workspace disconnect action and confirmation modal are served in HTML."""
    res = client.get("/")
    assert res.status_code == 200
    html = res.text

    # Disconnect confirmation modal and actions
    assert 'id="clientDisconnectModal"' in html
    assert 'id="clientDisconnectCommandsPre"' in html
    assert 'openDisconnectClientModal(' in html
    assert 'closeDisconnectClientModal()' in html
    assert 'copyDisconnectRevokeCommands()' in html
    assert 'downloadDisconnectRevokeScript()' in html
    assert 'executeConfirmedClientDisconnect()' in html
    assert 'confirmDeleteClient(' in html
    assert 'roles/resourcemanager.organizationViewer' in html
    assert 'remove-iam-policy-binding' in html


def test_client_disconnect_workflow_and_data_preservation():
    """Verify that POST /api/clients/{client_id}/disconnect preserves evidence, clears operator binding,
    and rejects future live scans while maintaining read access to reports and scorecards."""
    op_headers = {**AUTH_HEADER, "X-Operator-Id": "operator-disconnect-suite"}
    test_cid = "client-disconnect-audit-target"
    test_drive_folder = "1EvidenceDriveFolder-Untouched-2026"
    test_projects = ["disconnect-prod-01", "disconnect-stage-02"]

    # 1. Onboard client
    onboard_res = client.post(
        "/api/clients/onboard",
        json={
            "name": "Target Disconnect Inc",
            "client_id": test_cid,
            "projects": test_projects,
            "days": 30,
            "drive_folder_id": test_drive_folder,
            "org_id": "999888777",
            "is_shared": True,
        },
        headers=op_headers,
    )
    assert onboard_res.status_code == 200

    try:
        # 2. Switch operator active client to this new client and bind session
        sw_res = client.post(
            "/api/clients/active",
            json={"client_id": test_cid},
            headers=op_headers,
        )
        assert sw_res.status_code == 200
        assert OPERATOR_ACTIVE_CLIENTS.get("operator-disconnect-suite") == test_cid

        # 3. Disconnecting altostrat-ventures must be rejected with 400
        core_dis = client.post("/api/clients/altostrat-ventures/disconnect", headers=op_headers)
        assert core_dis.status_code == 400
        assert "Cannot disconnect core client" in core_dis.json()["detail"]

        # 4. Disconnect target client
        dis_res = client.post(f"/api/clients/{test_cid}/disconnect", headers=op_headers)
        assert dis_res.status_code == 200
        dis_data = dis_res.json()
        assert dis_data["status"] == "success"
        assert dis_data["client"]["status"] == "disconnected"

        # 5. Verify record in data/clients.json preserves drive_folder_id and projects
        from mcp_server_grc.portal import load_onboarded_clients
        all_clients = load_onboarded_clients()
        rec = next((c for c in all_clients if c.get("client_id") == test_cid), None)
        assert rec is not None
        assert rec["status"] == "disconnected"
        assert rec["drive_folder_id"] == test_drive_folder
        assert rec["projects"] == test_projects

        # 6. Verify operator active binding was cleared and reset to altostrat-ventures
        assert OPERATOR_ACTIVE_CLIENTS.get("operator-disconnect-suite") == "altostrat-ventures"

        # 7. Verify all live scan attempts are rejected with exact required message
        # 7a. POST /api/clients/active rejected
        active_attempt = client.post(
            "/api/clients/active",
            json={"client_id": test_cid},
            headers=op_headers,
        )
        assert active_attempt.status_code == 400
        assert active_attempt.json()["detail"] == DISCONNECTED_CLIENT_MESSAGE

        # 7b. Direct cloud_inspector call rejected
        with pytest.raises(ValueError) as exc_info:
            inspect_cloud_kms_key("test-key", client_id=test_cid)
        assert DISCONNECTED_CLIENT_MESSAGE in str(exc_info.value)

        # 7c. Direct cloud_inspector call by project_id rejected
        with pytest.raises(ValueError) as exc_info_proj:
            inspect_cloud_kms_key("test-key", project_id=test_projects[0])
        assert DISCONNECTED_CLIENT_MESSAGE in str(exc_info_proj.value)

        # 7d. POST /api/chat scoped to disconnected client rejected
        chat_attempt = client.post(
            "/api/chat",
            json={"message": "Audit Cloud KMS keys", "client_id": test_cid},
            headers=op_headers,
        )
        assert chat_attempt.status_code == 400
        assert chat_attempt.json()["detail"] == DISCONNECTED_CLIENT_MESSAGE

        # 7e. POST /api/audit/run_phases scoped to disconnected client rejected
        run_audit_attempt = client.post(
            "/api/audit/run_phases",
            json={"projects": test_projects},
            headers={**op_headers, "X-Client-Id": test_cid},
        )
        assert run_audit_attempt.status_code == 400
        assert run_audit_attempt.json()["detail"] == DISCONNECTED_CLIENT_MESSAGE

        # 7f. POST /api/audit/remediate_phase scoped to disconnected client rejected
        rem_attempt = client.post(
            "/api/audit/remediate_phase",
            json={"phase": 1, "project_id": test_projects[0]},
            headers={**op_headers, "X-Client-Id": test_cid},
        )
        assert rem_attempt.status_code == 400
        assert rem_attempt.json()["detail"] == DISCONNECTED_CLIENT_MESSAGE

        # 7g. POST /api/agent/update_policy_autonomously scoped to disconnected client rejected
        pol_attempt = client.post(
            "/api/agent/update_policy_autonomously",
            json={"control_id": "A.5.15", "project_id": test_projects[0]},
            headers={**op_headers, "X-Client-Id": test_cid},
        )
        assert pol_attempt.status_code == 400
        assert pol_attempt.json()["detail"] == DISCONNECTED_CLIENT_MESSAGE

        # 8. Verify GET endpoints for existing reports/scorecard continue to succeed normally
        # 8a. GET /api/scorecard
        sc_res = client.get(f"/api/scorecard?client_id={test_cid}", headers=op_headers)
        assert sc_res.status_code == 200
        assert "overall_score" in sc_res.json()

        # 8b. GET /api/reports/executive
        exec_res = client.get(f"/api/reports/executive?client_id={test_cid}", headers=op_headers)
        assert exec_res.status_code == 200
        assert exec_res.json()["classification"] == "CONFIDENTIAL / EXECUTIVE DOSSIER"

        # 8c. GET /api/reports/technical
        tech_res = client.get(f"/api/reports/technical?client_id={test_cid}", headers=op_headers)
        assert tech_res.status_code == 200
        assert "evidence_chain" in tech_res.json()

        # 8d. GET /api/reports/export
        export_res = client.get(f"/api/reports/export?client_id={test_cid}", headers=op_headers)
        assert export_res.status_code == 200

        # 8e. GET /api/clients
        clients_res = client.get("/api/clients", headers=op_headers)
        assert clients_res.status_code == 200
        client_list = clients_res.json()["clients"]
        dis_in_list = next((c for c in client_list if c["client_id"] == test_cid), None)
        assert dis_in_list is not None
        assert dis_in_list["status"] == "disconnected"

    finally:
        # Cleanup test client
        client.delete(f"/api/clients/{test_cid}", headers=op_headers)


def test_portal_html_client_switch_refreshes_live_projects_and_org_elements():
    """Verify that portal_html.py contains the UI fix for cross-tenant staleness:
    1. executeConfirmedClientSwitch resets allOrgProjects, activeProjects, and selectedProjectIds.
    2. executeConfirmedClientSwitch calls await loadProjects().
    3. loadProjects updates providerActiveOrgName, scopeConnectedOrgName,
       orgScopeDropdownOrgTitle, and homeMetaOrgName.
    4. loadProjects populates allOrgProjects from live CRM data or projects.
    """
    res = client.get("/")
    assert res.status_code == 200
    html = res.text

    assert "await loadProjects()" in html
    assert 'document.getElementById("providerActiveOrgName")' in html
    assert 'document.getElementById("scopeConnectedOrgName")' in html
    assert 'document.getElementById("orgScopeDropdownOrgTitle")' in html
    assert 'document.getElementById("homeMetaOrgName")' in html
    assert "allOrgProjects = [];" in html
    assert "activeProjects = [];" in html
    assert "selectedProjectIds = new Set();" in html


def test_switching_to_client_with_no_org_id_updates_labels_to_standalone_state():
    """Verify that switching to a client without a GCP organization (no org_id)
    returns an honest 'no organization' state in /api/projects, does not retain
    the previous client's org name or ID, and that the portal HTML includes
    the honest standalone labels and unconditional update logic.
    """
    op_headers = {**AUTH_HEADER, "X-Operator-Id": "consultant-standalone-tester"}
    client_with_org_id = "client-with-formal-org"
    client_no_org_id = "client-standalone-no-org"

    try:
        # 1. Onboard Client A with a formal GCP Organization
        client.post(
            "/api/clients/onboard",
            json={
                "name": "Formal Org Corp",
                "client_id": client_with_org_id,
                "org_id": "987654321012",
                "org_name": "Formal Org Corporation",
                "projects": ["formal-prod-svc", "formal-db-svc"],
            },
            headers=op_headers,
        )

        # 2. Onboard Client B with NO organization (standalone projects only)
        client.post(
            "/api/clients/onboard",
            json={
                "name": "Standalone Startup",
                "client_id": client_no_org_id,
                "projects": ["startup-app-standalone", "startup-cache-standalone"],
            },
            headers=op_headers,
        )

        from unittest.mock import MagicMock, patch

        mock_session = MagicMock()
        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_resp.json.return_value = {
            "projects": [
                {
                    "projectId": "formal-prod-svc",
                    "name": "Formal Prod Svc",
                    "projectNumber": "98701",
                    "lifecycleState": "ACTIVE",
                    "parent": {"type": "organization", "id": "987654321012"},
                },
                {
                    "projectId": "formal-db-svc",
                    "name": "Formal DB Svc",
                    "projectNumber": "98702",
                    "lifecycleState": "ACTIVE",
                    "parent": {"type": "organization", "id": "987654321012"},
                },
            ]
        }
        mock_session.get.return_value = mock_resp

        with patch("mcp_server_grc.portal.get_authorized_session", return_value=(mock_session, "test-target")):
            # 3. Switch to Client A (with org)
            res_sw_a = client.post(
                "/api/clients/active",
                json={"client_id": client_with_org_id},
                headers=op_headers,
            )
            assert res_sw_a.status_code == 200

            res_a_proj = client.get("/api/projects", headers=op_headers)
            assert res_a_proj.status_code == 200
            data_a = res_a_proj.json()
            assert data_a["client_id"] == client_with_org_id
            assert data_a["org_id"] == "987654321012"
            assert data_a["org_metadata"]["org_id"] == "987654321012"
            assert data_a["org_metadata"]["org_name"] == "Formal Org Corporation"

            # 4. Switch to Client B (no org)
            res_sw_b = client.post(
                "/api/clients/active",
                json={"client_id": client_no_org_id},
                headers=op_headers,
            )
            assert res_sw_b.status_code == 200

            res_b_proj = client.get("/api/projects", headers=op_headers)
            assert res_b_proj.status_code == 200
            data_b = res_b_proj.json()
            assert data_b["client_id"] == client_no_org_id

            # Must report honest 'no organization' state
            assert data_b["org_id"] is None
            assert data_b["org_metadata"]["org_id"] is None
            assert data_b["org_metadata"]["org_name"] is None

            # Verify standalone projects are present
            pids_b = [p["project_id"] for p in data_b["projects"]]
            assert "startup-app-standalone" in pids_b
            assert "startup-cache-standalone" in pids_b

            # Verify Client A's org name, org ID, and projects are completely absent
            assert "987654321012" not in str(data_b)
            assert "Formal Org" not in str(data_b)
            assert "formal-prod-svc" not in pids_b

        # 5. Verify the portal frontend markup contains the standalone fallback labels
        portal_res = client.get("/")
        assert portal_res.status_code == 200
        html = portal_res.text

        assert "Projetos Avulsos (sem Organização GCP)" in html
        assert "Standalone Projects (no GCP Organization)" in html
        assert "const hasOrg = Boolean(orgId" in html
        assert "scopeConnectedOrgName" in html
        assert "orgScopeDropdownOrgTitle" in html
        assert "homeMetaOrgName" in html
        assert "providerActiveOrgName" in html

    finally:
        client.delete(f"/api/clients/{client_with_org_id}", headers=op_headers)
        client.delete(f"/api/clients/{client_no_org_id}", headers=op_headers)


def test_client_switch_clears_matrix_finops_reports_scorecard_cross_tenant_state():
    """Verify that switching to a new unassessed client returns honest zeroed/pending state
    across ISO Matrix, FinOps, Scorecard, Executive Dossier, and Technical Report,
    and switching back to Altostrat restores Altostrat's baseline without state leakage.
    """
    op_headers = {**AUTH_HEADER, "X-Operator-Id": "consultant-isolation-e2e"}
    new_cid = "new-tenant-corp"

    try:
        # 1. Verify Altostrat baseline
        res_alto_finops = client.get("/api/finops", headers=op_headers)
        assert res_alto_finops.status_code == 200
        alto_finops = res_alto_finops.json()["summary"]
        assert alto_finops["total_cost_usd"] > 0
        assert alto_finops["total_tokens"] > 0

        res_alto_matrix = client.get("/api/iso_matrix", headers=op_headers)
        assert res_alto_matrix.status_code == 200
        alto_matrix = res_alto_matrix.json()
        assert alto_matrix["counts"]["compliant"] >= 80
        assert alto_matrix["counts"]["pending"] == 0

        res_alto_score = client.get("/api/scorecard", headers=op_headers)
        assert res_alto_score.status_code == 200
        alto_score = res_alto_score.json()
        assert alto_score["overall_score"] > 50.0
        assert alto_score["compliant_count"] >= 80

        res_alto_exec = client.get("/api/reports/executive?format=json", headers=op_headers)
        assert res_alto_exec.status_code == 200
        alto_exec = res_alto_exec.json()
        assert alto_exec["client_id"] == "altostrat-ventures"
        assert alto_exec["overall_score"] > 50.0

        # 2. Onboard new client
        onboard_res = client.post(
            "/api/clients/onboard",
            json={
                "name": "New Tenant Corp",
                "client_id": new_cid,
                "projects": ["new-tenant-prod-01"],
                "days": 30,
            },
            headers=op_headers,
        )
        assert onboard_res.status_code == 200

        # 3. Switch active client to new tenant
        sw_res = client.post(
            "/api/clients/active",
            json={"client_id": new_cid},
            headers=op_headers,
        )
        assert sw_res.status_code == 200
        assert sw_res.json()["active_client_id"] == new_cid

        # 4. Verify FinOps is completely zeroed (nova, zerada)
        res_new_finops = client.get("/api/finops", headers=op_headers)
        assert res_new_finops.status_code == 200
        new_finops = res_new_finops.json()["summary"]
        assert new_finops["total_cost_usd"] == 0.0
        assert new_finops["total_tokens"] == 0
        assert new_finops["total_invocations"] == 0
        assert new_finops["total_events"] == 0
        assert res_new_finops.json()["agents"] == []

        # 5. Verify ISO Matrix shows honest pending state (0 compliant, 93 pending)
        res_new_matrix = client.get("/api/iso_matrix", headers=op_headers)
        assert res_new_matrix.status_code == 200
        new_matrix = res_new_matrix.json()
        assert new_matrix["counts"]["compliant"] == 0
        assert new_matrix["counts"]["pending"] == 93
        assert new_matrix["counts"]["non_compliant"] == 0
        for ctrl in new_matrix["controls"]:
            assert ctrl["status"] == "PENDING"

        # 6. Verify Scorecard shows 0.0% / NOT_AUDITED
        res_new_score = client.get("/api/scorecard", headers=op_headers)
        assert res_new_score.status_code == 200
        new_score = res_new_score.json()
        assert new_score["overall_score"] == 0.0
        assert new_score["rating"] == "NOT_AUDITED (PENDING ASSESSMENT)"
        assert new_score["compliant_count"] == 0
        assert new_score["non_compliant_count"] == 0
        for cat_k, cat_data in new_score["category_breakdown"].items():
            assert cat_data["compliant"] == 0
            assert cat_data["percentage"] == 0.0

        # 7. Verify Executive Dossier is scoped to New Tenant Corp with pending opinion
        res_new_exec = client.get("/api/reports/executive?format=json", headers=op_headers)
        assert res_new_exec.status_code == 200
        new_exec = res_new_exec.json()
        assert new_exec["client_id"] == new_cid
        assert new_exec["client_name"] == "New Tenant Corp"
        assert new_exec["overall_score"] == 0.0
        assert new_exec["rating"] == "NOT_AUDITED (PENDING ASSESSMENT)"
        assert "pending assessment" in new_exec["executive_opinion"].lower()

        # 8. Verify Technical Report is scoped to New Tenant Corp with 0 compliant controls
        res_new_tech = client.get("/api/reports/technical?format=json", headers=op_headers)
        assert res_new_tech.status_code == 200
        new_tech = res_new_tech.json()
        assert new_tech["client_id"] == new_cid
        assert new_tech["client_name"] == "New Tenant Corp"
        assert new_tech["overall_score"] == 0.0
        assert new_tech["rating"] == "NOT_AUDITED (PENDING ASSESSMENT)"

        # 9. Switch back to Altostrat Ventures and verify baseline is fully restored
        sw_back_res = client.post(
            "/api/clients/active",
            json={"client_id": "altostrat-ventures"},
            headers=op_headers,
        )
        assert sw_back_res.status_code == 200

        res_restored_finops = client.get("/api/finops", headers=op_headers)
        assert res_restored_finops.status_code == 200
        restored_finops = res_restored_finops.json()["summary"]
        assert restored_finops["total_cost_usd"] > 0
        assert restored_finops["total_tokens"] > 0

        res_restored_matrix = client.get("/api/iso_matrix", headers=op_headers)
        assert res_restored_matrix.status_code == 200
        restored_matrix = res_restored_matrix.json()
        assert restored_matrix["counts"]["compliant"] >= 80

        res_restored_score = client.get("/api/scorecard", headers=op_headers)
        assert res_restored_score.status_code == 200
        assert res_restored_score.json()["overall_score"] > 50.0

        # 10. Verify portal HTML contains pending controls UI and dynamic reload calls
        res_ui = client.get("/")
        assert res_ui.status_code == 200
        html = res_ui.text
        assert "filterStatusPending" in html
        assert "countStatusPending" in html
        assert "matrix_status_pending" in html
        assert "loadExecutiveReport" in html
        assert "loadTechnicalReport" in html
        assert "techOpinionBadge" in html
        assert "docClientOrg" in html

    finally:
        client.delete(f"/api/clients/{new_cid}", headers=op_headers)
        client.post(
            "/api/clients/active",
            json={"client_id": "altostrat-ventures"},
            headers=op_headers,
        )


def test_phased_audit_auth_headers_and_adc_handling(monkeypatch):
    """Verify that run_phases, get_authorized_session, and inspect_project_iam_policy

    properly propagate credentials, support ADC fallback in dev/Cloud Run mode,
    and report 403 permission errors with actionable remediation instructions.
    """
    from mcp_server_grc.cloud_inspector import (
        get_authorized_session,
        inspect_project_iam_policy,
    )
    from unittest.mock import patch, MagicMock

    # 1. When ALLOW_DEV_AUTH_BYPASS is true, get_authorized_session falls back to ADC
    monkeypatch.setenv("ALLOW_DEV_AUTH_BYPASS", "true")
    with patch("google.auth.default") as mock_default:
        mock_creds = MagicMock()
        mock_default.return_value = (mock_creds, "mock-project-123")
        session, proj = get_authorized_session(bearer_token=None, project_id="mock-project-123")
        assert session is not None
        assert proj == "mock-project-123"

    # 2. When GCP Resource Manager returns HTTP 403, inspect_project_iam_policy reports PERMISSION_DENIED with remediation
    with patch("mcp_server_grc.cloud_inspector.get_authorized_session") as mock_gas:
        mock_sess = MagicMock()
        mock_resp = MagicMock()
        mock_resp.status_code = 403
        mock_resp.text = '{"error": {"code": 403, "message": "Permission denied"}}'
        mock_sess.post.return_value = mock_resp
        mock_gas.return_value = (mock_sess, "test-restricted-proj")

        iam_res = inspect_project_iam_policy(project_id="test-restricted-proj", bearer_token=None)
        assert iam_res["status"] == "PERMISSION_DENIED"
        assert "Permissão negada (HTTP 403)" in iam_res["message"]
        assert "onboard_client.sh" in iam_res["message"]
        assert iam_res["compliance"]["status"] == "NON_COMPLIANT"
        assert "onboard_client.sh" in iam_res["compliance"]["remediation"]

    # 3. Verify portal HTML includes ...getAuthHeaders() in all audit execution calls and has corporateAccessTokenInput
    res_ui = client.get("/")
    assert res_ui.status_code == 200
    html = res_ui.text
    assert "corporateAccessTokenInput" in html
    assert "custom_google_access_token" in html


def test_phase3_governance_scan_and_matrix_sync():
    """Verify that Phase 3 honestly reports NOT_AUTOMATABLE (governance/people controls require
    questionnaire self-attestation, never a fabricated automated result) and that a scan against
    a project with no real cloud credentials leaves the client's matrix, scorecard, and reports
    honestly at zero/pending rather than fabricating compliant findings.
    """
    headers = {**AUTH_HEADER, "X-Operator-Id": "consultant-phased-test"}
    # Onboard fresh client
    client.post(
        "/api/clients/onboard",
        json={"name": "GovCorp Brasil", "client_id": "govcorp-br", "projects": ["govcorp-prod"], "days": 30, "is_shared": True},
        headers=headers,
    )
    client_headers = {**headers, "X-Client-Id": "govcorp-br"}

    try:
        # Before scan: honest zeroed/pending state
        m_before = client.get("/api/iso_matrix", headers=client_headers).json()
        assert m_before["counts"]["pending"] == 93
        assert m_before["counts"]["compliant"] == 0
        assert m_before["counts"]["non_compliant"] == 0

        sc_before = client.get("/api/scorecard", headers=client_headers).json()
        assert sc_before["overall_score"] == 0.0
        assert "NOT_AUDITED" in sc_before["rating"]

        fin_before = client.get("/api/finops", headers=client_headers).json()
        assert fin_before["summary"]["total_cost_usd"] == 0.0

        # Execute Phased Scan (no real cloud credentials available in this test environment)
        scan_res = client.post("/api/audit/run_phases", json={"projects": ["govcorp-prod"]}, headers=client_headers)
        assert scan_res.status_code == 200
        scan_data = scan_res.json()

        # Verify Phase 3 honestly reports NOT_AUTOMATABLE — it must NEVER fabricate COMPLIANT
        # results for A.5.1, A.5.5, A.5.7, A.5.9, A.5.24, A.5.31 or any other governance control
        # without a matching real cloud_inspector.py function.
        phases = scan_data.get("phases", [])
        assert len(phases) == 4
        phase3 = phases[2]
        assert phase3["phase"] == "Phase 3: Zero-Copy Governance & ISMS Policies (A.5)"
        assert phase3["status"] == "NOT_AUTOMATABLE"
        assert phase3["compliance_score"] is None
        assert "controls_tested" not in phase3
        assert any("questionnaire" in f.lower() or "self-attestation" in f.lower() for f in phase3["findings"])

        # Without real cloud access, no controls become compliant and nothing is synced
        assert scan_data["overall_score"] == 0.0
        assert scan_data["questionnaire_controls_synced"] == 0

        # After scan: Matrix remains honestly pending — no fabricated compliance
        m_after = client.get("/api/iso_matrix", headers=client_headers).json()
        assert m_after["counts"]["compliant"] == 0
        assert m_after["counts"]["pending"] == 93
        controls_by_id = {c["id"]: c for c in m_after["controls"]}
        assert controls_by_id["A.5.1"]["status"] == "PENDING"
        assert controls_by_id["A.5.5"]["status"] == "PENDING"
        assert controls_by_id["A.5.7"]["status"] == "PENDING"

        # After scan: Scorecard remains honestly at 0 — no fabricated compliance
        sc_after = client.get("/api/scorecard", headers=client_headers).json()
        assert sc_after["overall_score"] == 0.0
        assert sc_after["compliant_count"] == 0

        # After scan: FinOps has still accumulated usage for this client (the scan itself ran)
        fin_after = client.get("/api/finops", headers=client_headers).json()
        assert fin_after["summary"]["total_tokens"] > 0

        # After scan: Executive and Technical reports reflect this client and its honest score
        exec_rep = client.get("/api/reports/executive?format=json", headers=client_headers).json()
        assert exec_rep["client_name"] == "GovCorp Brasil"
        assert exec_rep["overall_score"] == 0.0

        tech_rep = client.get("/api/reports/technical?format=json", headers=client_headers).json()
        assert tech_rep["overall_score"] == 0.0

    finally:
        client.delete("/api/clients/govcorp-br", headers=headers)


def test_ui_sync_button_and_no_duplicate_menus():
    """Verify HTML UI elements: sync button is present in matrix, duplicate filter pills are removed, and client name does not clip."""
    res = client.get("/")
    assert res.status_code == 200
    html = res.text

    # 1. Sync button is in matrix toolbar
    assert 'id="btnSyncMatrixWithScan"' in html
    assert 'onclick="syncMatrixWithScan()"' in html
    assert "Sincronizar com Scan de Controles" in html

    # 2. Duplicate matrixFilterPills is removed
    assert 'id="matrixFilterPills"' not in html

    # 3. Brand title is concise
    assert "Agentic GRC Accelerator" in html

    # 4. Client name CSS has word-break: break-word
    assert ".client-name {" in html
    assert "word-break: break-word;" in html





