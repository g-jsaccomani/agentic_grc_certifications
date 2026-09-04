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


def test_individual_phases_and_remediation():
    # 1. Run single phase 1
    res_p1 = client.post("/api/audit/run_phases", json={"projects": ["agentic-grc-cd06"], "phase": 1})
    assert res_p1.status_code == 200
    data_p1 = res_p1.json()
    assert len(data_p1["phases"]) == 1
    assert data_p1["phases"][0]["phase"].startswith("Fase 1")

    # 2. Run single phase 2
    res_p2 = client.post("/api/audit/run_phases", json={"projects": ["agentic-grc-cd06"], "phase": 2})
    assert res_p2.status_code == 200
    assert len(res_p2.json()["phases"]) == 1
    assert res_p2.json()["phases"][0]["phase"].startswith("Fase 2")

    # 3. Remediate phase 2
    res_rem = client.post("/api/audit/remediate_phase", json={"phase": 2, "project_id": "agentic-grc-cd06"})
    assert res_rem.status_code == 200
    rem_data = res_rem.json()
    assert rem_data["details"]["status"] == "REMEDIATED"
    assert rem_data["details"]["new_score"] == 100.0


def test_custom_subagents_lifecycle():
    # 1. Create a custom subagent
    new_agent = {
        "name": "Custom Test FinOps Agent",
        "role": "Cloud Cost and Compliance Inspector",
        "description": "Tests storage cost allocation and tagging",
        "system_prompt": "Inspect tags and labels on all compute resources",
        "tools": ["iam", "asset_inventory"],
        "model": "gemini-2.5-flash",
        "temperature": 0.2,
        "target_controls": ["A.5.9", "A.8.10"]
    }
    res_create = client.post("/api/subagents", json=new_agent)
    assert res_create.status_code == 200
    created = res_create.json()["subagent"]
    agent_id = created["id"]
    assert agent_id.startswith("custom-")

    # 2. List subagents
    res_list = client.get("/api/subagents")
    assert res_list.status_code == 200
    data = res_list.json()
    assert any(a["id"] == agent_id for a in data["custom_subagents"])

    # 3. Run custom subagent
    res_run = client.post(f"/api/subagents/{agent_id}/run")
    assert res_run.status_code == 200
    assert res_run.json()["status"] == "COMPLETED"
    assert len(res_run.json()["findings"]) > 0

    # 4. Delete custom subagent
    res_del = client.delete(f"/api/subagents/{agent_id}")
    assert res_del.status_code == 200
    assert res_del.json()["status"] == "DELETED"


def test_agentic_recommendation_and_autonomous_policy_update():
    # 1. Test subagent recommendation
    res_rec = client.post("/api/agent/recommend_subagent", json={"project_id": "agentic-grc-cd06", "industry": "FINANCIAL_SERVICES"})
    assert res_rec.status_code == 200
    rec_data = res_rec.json()
    assert rec_data["status"] == "SUCCESS"
    assert "Fintech & Banking" in rec_data["recommendation"]["name"]
    assert len(rec_data["recommendation"]["target_controls"]) > 0

    # 2. Test autonomous monitor
    res_mon = client.post("/api/agent/autonomous_monitor", json={"project_id": "agentic-grc-cd06", "simulate_deviation": True})
    assert res_mon.status_code == 200
    mon_data = res_mon.json()
    assert mon_data["active_alert"] is True
    assert mon_data["alert"]["control_id"] == "A.8.24"
    assert "proposed_amendment_text" in mon_data["alert"]

    # 3. Test autonomous policy update
    res_update = client.post("/api/agent/update_policy_autonomously", json={"project_id": "agentic-grc-cd06", "control_id": "A.8.24"})
    assert res_update.status_code == 200
    up_data = res_update.json()
    assert up_data["status"] == "POLICY_UPDATED_AND_ENFORCED"
    assert len(up_data["hash_sha256"]) == 64
    assert up_data["new_score"] == 100.0


def test_cloudstyle_html_report_export():
    res_html = client.get("/api/reports/export?format=html")
    assert res_html.status_code == 200
    assert "Continuous Compliance & Audit Dossier" in res_html.text
    assert "data:image/png;base64," in res_html.text
    assert "google-color-stripe-bar" in res_html.text

    # Verify static assets
    res_icon = client.get("/static/images/google_cloud_icon.png")
    assert res_icon.status_code == 200
    assert len(res_icon.content) > 1000

    res_wordmark = client.get("/static/images/google_cloud_wordmark.png")
    assert res_wordmark.status_code == 200
    assert len(res_wordmark.content) > 1000


def test_finops_and_org_scope_toggle():
    # Test GET /api/projects returns organization metadata and all_org_projects
    res_proj = client.get("/api/projects")
    assert res_proj.status_code == 200
    data_proj = res_proj.json()
    assert "all_org_projects" in data_proj
    assert data_proj["total_org_projects"] >= 10
    assert "org_metadata" in data_proj
    assert data_proj["org_metadata"]["org_id"] == "108928374619"

    # Test toggle scope endpoint
    res_toggle = client.post("/api/projects/toggle_scope", json={"project_id": "agentic-grc-ai-workloads", "in_scope": True})
    assert res_toggle.status_code == 200
    toggle_data = res_toggle.json()
    assert toggle_data["status"] == "ok"
    assert toggle_data["in_scope"] is True

    # Test FinOps API
    res_finops = client.get("/api/finops")
    assert res_finops.status_code == 200
    data_finops = res_finops.json()
    assert "summary" in data_finops
    assert data_finops["summary"]["total_cost_usd"] > 0
    assert data_finops["summary"]["total_tokens"] > 0
    assert "agents" in data_finops
    assert len(data_finops["agents"]) >= 8

    # Test FinOps simulation
    res_sim = client.post("/api/finops/simulate")
    assert res_sim.status_code == 200
    sim_data = res_sim.json()
    assert sim_data["summary"]["total_invocations"] > data_finops["summary"]["total_invocations"]




