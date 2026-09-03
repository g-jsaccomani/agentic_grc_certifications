"""Unit and integration tests for Custom MCP Server (StreamableHTTP & A2A)."""

import pytest
from fastapi.testclient import TestClient
from mcp_server_grc.server import app

client = TestClient(app)

VALID_HEADERS = {
    "X-Serverless-Authorization": "Bearer mock-service-agent-id-token",
    "Authorization": "Bearer mock-end-user-oauth-token",
}


def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["service"] == "mcp-server-grc"


def test_agent_card_discovery():
    response = client.get("/.well-known/agent.json")
    assert response.status_code == 200
    card = response.json()
    assert card["protocol_version"] == "1.0"
    assert card["name"] == "mcp-server-grc-evidence"
    assert "oauth2" in card["capabilities"]["auth_schemes"]
    skill_names = [s["name"] for s in card["skills"]]
    assert "audit_cloud_security" in skill_names
    assert "scan_iac_configuration" in skill_names
    assert "correlate_threat_intelligence" in skill_names
    assert "audit_climate_resilience" in skill_names
    assert "get_iam_policy" in skill_names


def test_mcp_endpoint_missing_auth_headers():
    payload = {"tool": "get_iam_policy", "arguments": {"bucket_name": "test-bucket"}}
    # Missing all auth headers
    res1 = client.post("/mcp", json=payload)
    assert res1.status_code == 401

    # Missing user Authorization header
    res2 = client.post(
        "/mcp",
        json=payload,
        headers={"X-Serverless-Authorization": "Bearer test-id-token"},
    )
    assert res2.status_code == 401


def test_mcp_get_iam_policy():
    payload = {"tool": "get_iam_policy", "arguments": {"bucket_name": "production-data-bucket"}}
    response = client.post("/mcp", json=payload, headers=VALID_HEADERS)
    assert response.status_code == 200
    data = response.json()
    assert data["tool"] == "get_iam_policy"
    assert data["result"]["bucket"] == "production-data-bucket"
    assert data["result"]["status"] == "COMPLIANT_WITH_A.5.23_REQUIREMENTS"


def test_mcp_audit_cloud_security():
    payload = {
        "tool": "audit_cloud_security",
        "arguments": {
            "resource_type": "gcs_bucket",
            "resource_name": "test-b",
            "config": {
                "public_access_prevention": "enforced",
                "uniform_bucket_level_access": True,
            },
        },
    }
    response = client.post("/mcp", json=payload, headers=VALID_HEADERS)
    assert response.status_code == 200
    assert response.json()["result"]["status"] == "COMPLIANT"


def test_mcp_scan_iac_configuration():
    payload = {
        "tool": "scan_iac_configuration",
        "arguments": {
            "iac_type": "terraform",
            "content": "resource \"google_storage_bucket\" \"b\" { acl = \"public-read\" }",
        },
    }
    response = client.post("/mcp", json=payload, headers=VALID_HEADERS)
    assert response.status_code == 200
    assert response.json()["result"]["status"] == "NON_COMPLIANT"


def test_mcp_correlate_threat_intelligence():
    payload = {
        "tool": "correlate_threat_intelligence",
        "arguments": {
            "log_sink_name": "bq-sink",
            "sink_destination": "bigquery.googleapis.com/p/d",
            "recent_events": [],
            "threat_feed_enabled": True,
        },
    }
    response = client.post("/mcp", json=payload, headers=VALID_HEADERS)
    assert response.status_code == 200
    assert response.json()["result"]["status"] == "COMPLIANT"


def test_mcp_audit_climate_resilience():
    payload = {
        "tool": "audit_climate_resilience",
        "arguments": {
            "workload_id": "payment-gateway",
            "topology": {
                "primary_region": "us-central1",
                "secondary_region": "us-east4",
                "storage_redundancy": "multi-region",
                "automated_failover": True,
            },
        },
    }
    response = client.post("/mcp", json=payload, headers=VALID_HEADERS)
    assert response.status_code == 200
    assert response.json()["result"]["status"] == "COMPLIANT"


def test_mcp_unknown_tool():
    payload = {"tool": "unknown_tool_xyz", "arguments": {}}
    response = client.post("/mcp", json=payload, headers=VALID_HEADERS)
    assert response.status_code == 404
