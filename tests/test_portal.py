"""Unit tests for the Client Web Portal and its REST API."""

import io
from fastapi.testclient import TestClient
from mcp_server_grc.server import app

client = TestClient(app)


def test_portal_html_serving():
    res = client.get("/")
    assert res.status_code == 200
    assert "Gemini Enterprise Agent Platform" in res.text
    assert "Chatbot Auditor" in res.text

    res_portal = client.get("/portal")
    assert res_portal.status_code == 200


def test_portal_chat_endpoints():
    # 1. Audit prompt
    res_audit = client.post("/api/chat", json={"message": "Execute proactive audit"})
    assert res_audit.status_code == 200
    data = res_audit.json()
    assert "Proactive Audit Cycle Completed" in data["response"]
    assert data["subagent_used"] == "ContinuousIntelligenceEngine"

    # 2. Horizon scanning prompt
    res_horizon = client.post("/api/chat", json={"message": "Horizon scanning regulatory update"})
    assert res_horizon.status_code == 200
    assert "Horizon Scanning Regulatory Review" in res_horizon.json()["response"]

    # 3. Cryptography prompt
    res_crypto = client.post("/api/chat", json={"message": "Audit KMS cryptography A.8.24"})
    assert res_crypto.status_code == 200
    assert "Control A.8.24 Analysis" in res_crypto.json()["response"]

    # 4. General prompt
    res_gen = client.post("/api/chat", json={"message": "What is your capability?"})
    assert res_gen.status_code == 200
    assert "GEAP Compliance" in res_gen.json()["response"]


def test_portal_upload_file():
    tf_content = """
    resource "google_storage_bucket" "bad" {
      name = "bad-bucket"
      acl  = "public-read"
    }
    """
    file_bytes = io.BytesIO(tf_content.encode("utf-8"))
    res = client.post(
        "/api/upload",
        files={"file": ("main.tf", file_bytes, "text/plain")}
    )
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "SUCCESS"
    assert data["filename"] == "main.tf"
    assert data["audit_finding"]["status"] == "NON_COMPLIANT"


def test_portal_storage_link():
    res = client.post(
        "/api/storage/link",
        json={"source": "google_drive", "uri": "drive-folder-123", "user_token": "valid-token"}
    )
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "CONNECTED"
    assert data["zero_copy_guarantee"] is True
    assert len(data["discovered_documents"]) > 0


def test_portal_subagents_and_dashboard():
    # Subagents listing
    res_sub = client.get("/api/subagents")
    assert res_sub.status_code == 200
    subagents = res_sub.json()["subagents"]
    assert len(subagents) >= 4

    # Trigger subagent
    res_trigger = client.post(
        "/api/subagents/trigger",
        json={"subagent": "annex_a", "target": "kms"}
    )
    assert res_trigger.status_code == 200

    # Dashboard
    res_dash = client.get("/api/dashboard")
    assert res_dash.status_code == 200
    dash_data = res_dash.json()
    assert dash_data["overall_score"] == 100.0

    # Remediation approval
    res_app = client.post(
        "/api/remediation/approve",
        json={"remediation_id": "HITL-AMENDMENT-001"}
    )
    assert res_app.status_code == 200
    assert res_app.json()["status"] == "APPROVED"
