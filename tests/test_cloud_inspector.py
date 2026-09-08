"""Comprehensive Unit Tests for Cloud Inspector (mcp_server_grc/cloud_inspector.py).

Verifies real-time read-only Google Cloud inspection tools, mock responses,
error handling, and ISO 27001 evaluation rules.
"""

from unittest.mock import MagicMock, patch
import pytest

from mcp_server_grc.cloud_inspector import (
    get_authorized_session,
    inspect_cloud_kms_key,
    list_cloud_kms_keys,
    inspect_cloud_storage_bucket,
    list_cloud_storage_buckets,
    inspect_project_iam_policy,
    inspect_cloud_run_services,
    check_and_increment_call_budget,
    get_session_call_count,
    reset_session_call_budget,
    get_session_disclosure_statement,
)


def test_get_authorized_session_mock_and_adc():
    """Verifies that mock tokens are skipped and valid ADC / sessions are created."""
    # Test mock token skips user credentials
    session, proj = get_authorized_session(bearer_token="ya29.test-token", project_id="test-proj")
    assert proj == "test-proj"

    # Test real-looking token
    with patch("google.oauth2.credentials.Credentials") as mock_creds, \
         patch("google.auth.transport.requests.AuthorizedSession") as mock_auth_session:
        mock_session_inst = MagicMock()
        mock_auth_session.return_value = mock_session_inst
        sess, pr = get_authorized_session(bearer_token="ya29.real-token-abc", project_id="my-proj")
        assert sess == mock_session_inst
        assert pr == "my-proj"


def test_inspect_cloud_kms_key_full_path_success():
    """Tests inspect_cloud_kms_key when given a full resource path."""
    mock_session = MagicMock()
    mock_resp = MagicMock()
    mock_resp.status_code = 200
    mock_resp.json.return_value = {
        "name": "projects/my-p/locations/global/keyRings/kr/cryptoKeys/key1",
        "rotationPeriod": "5184000s",
        "versionTemplate": {
            "protectionLevel": "HSM",
            "algorithm": "GOOGLE_SYMMETRIC_ENCRYPTION"
        },
        "purpose": "ENCRYPT_DECRYPT",
        "primary": {"state": "ENABLED"},
        "nextRotationTime": "2026-11-01T00:00:00Z"
    }
    mock_session.get.return_value = mock_resp

    with patch("mcp_server_grc.cloud_inspector.get_authorized_session", return_value=(mock_session, "my-p")):
        res = inspect_cloud_kms_key("projects/my-p/locations/global/keyRings/kr/cryptoKeys/key1")
        assert res["status"] == "FOUND"
        assert res["key_details"]["rotation_seconds"] == 5184000
        assert res["key_details"]["protectionLevel"] == "HSM"
        assert res["compliance"]["status"] == "COMPLIANT"


def test_inspect_cloud_kms_key_full_path_404_and_403():
    """Tests 404 and 403 responses on full KMS path."""
    mock_session = MagicMock()
    mock_resp = MagicMock()
    mock_resp.status_code = 404
    mock_session.get.return_value = mock_resp

    with patch("mcp_server_grc.cloud_inspector.get_authorized_session", return_value=(mock_session, "my-p")):
        res = inspect_cloud_kms_key("projects/my-p/locations/global/keyRings/kr/cryptoKeys/missing-key")
        assert res["status"] == "NOT_FOUND"

    mock_resp.status_code = 403
    with patch("mcp_server_grc.cloud_inspector.get_authorized_session", return_value=(mock_session, "my-p")):
        res = inspect_cloud_kms_key("projects/my-p/locations/global/keyRings/kr/cryptoKeys/forbidden-key")
        assert res["status"] == "PERMISSION_DENIED"


def test_inspect_cloud_kms_key_discovery_search():
    """Tests automatic multi-location scanning for short key name."""
    mock_session = MagicMock()
    
    def side_effect(url, timeout=5):
        m = MagicMock()
        if "cryptoKeys" in url:
            m.status_code = 200
            m.json.return_value = {
                "cryptoKeys": [{
                    "name": "projects/my-p/locations/global/keyRings/ring-a/cryptoKeys/found-key",
                    "rotationPeriod": "15552000s",  # > 90 days
                    "versionTemplate": {"protectionLevel": "SOFTWARE"}
                }]
            }
        elif "keyRings" in url:
            m.status_code = 200
            m.json.return_value = {"keyRings": [{"name": "projects/my-p/locations/global/keyRings/ring-a"}]}
        else:
            m.status_code = 200
            m.json.return_value = {}
        return m

    mock_session.get.side_effect = side_effect

    with patch("mcp_server_grc.cloud_inspector.get_authorized_session", return_value=(mock_session, "my-p")):
        res = inspect_cloud_kms_key("found-key", location="global")
        assert res["status"] == "FOUND"
        assert res["key_details"]["rotation_seconds"] == 15552000
        assert res["compliance"]["status"] == "NON_COMPLIANT"  # Exceeds 90 days


def test_list_cloud_kms_keys():
    """Tests list_cloud_kms_keys aggregation."""
    mock_session = MagicMock()
    def side_effect(url, timeout=5):
        m = MagicMock()
        if "cryptoKeys" in url:
            m.status_code = 200
            m.json.return_value = {"cryptoKeys": [{"name": "key-1", "rotationPeriod": "7776000s"}]}
        elif "keyRings" in url:
            m.status_code = 200
            m.json.return_value = {"keyRings": [{"name": "projects/my-p/locations/global/keyRings/ring-1"}]}
        else:
            m.status_code = 200
            m.json.return_value = {}
        return m

    mock_session.get.side_effect = side_effect

    with patch("mcp_server_grc.cloud_inspector.get_authorized_session", return_value=(mock_session, "my-p")):
        res = list_cloud_kms_keys(location="global")
        assert res["status"] == "SUCCESS"
        assert res["total_keys_found"] == 1


def test_inspect_cloud_storage_bucket_scenarios():
    """Tests Cloud Storage bucket inspection with compliant and non-compliant PAP/UBLA."""
    mock_session = MagicMock()
    mock_resp = MagicMock()
    mock_resp.status_code = 200
    mock_resp.json.return_value = {
        "name": "secure-bucket",
        "location": "US-CENTRAL1",
        "locationType": "region",
        "iamConfiguration": {
            "publicAccessPrevention": "enforced",
            "uniformBucketLevelAccess": {"enabled": True}
        },
        "encryption": {"defaultKmsKeyName": "projects/p/locations/g/keyRings/r/cryptoKeys/k"}
    }
    mock_session.get.return_value = mock_resp

    with patch("mcp_server_grc.cloud_inspector.get_authorized_session", return_value=(mock_session, "my-p")):
        res = inspect_cloud_storage_bucket("secure-bucket")
        assert res["status"] == "FOUND"
        assert res["compliance"]["status"] == "COMPLIANT"

    # Test 404
    mock_resp.status_code = 404
    with patch("mcp_server_grc.cloud_inspector.get_authorized_session", return_value=(mock_session, "my-p")):
        res = inspect_cloud_storage_bucket("missing-bucket")
        assert res["status"] == "NOT_FOUND"

    # Test 403
    mock_resp.status_code = 403
    with patch("mcp_server_grc.cloud_inspector.get_authorized_session", return_value=(mock_session, "my-p")):
        res = inspect_cloud_storage_bucket("forbidden-bucket")
        assert res["status"] == "PERMISSION_DENIED"


def test_list_cloud_storage_buckets():
    """Tests list_cloud_storage_buckets."""
    mock_session = MagicMock()
    mock_resp = MagicMock()
    mock_resp.status_code = 200
    mock_resp.json.return_value = {
        "items": [
            {
                "name": "bucket-a",
                "location": "US-CENTRAL1",
                "locationType": "region",
                "iamConfiguration": {
                    "publicAccessPrevention": "enforced",
                    "uniformBucketLevelAccess": {"enabled": True}
                }
            }
        ]
    }
    mock_session.get.return_value = mock_resp

    with patch("mcp_server_grc.cloud_inspector.get_authorized_session", return_value=(mock_session, "my-p")):
        res = list_cloud_storage_buckets()
        assert res["status"] == "SUCCESS"
        assert res["total_buckets"] == 1


def test_inspect_project_iam_policy_scenarios():
    """Tests IAM policy inspection for primitive roles and public exposures."""
    mock_session = MagicMock()
    mock_resp = MagicMock()
    mock_resp.status_code = 200
    mock_resp.json.return_value = {
        "bindings": [
            {"role": "roles/owner", "members": ["user:admin@example.com"]},
            {"role": "roles/viewer", "members": ["allUsers"]},
        ]
    }
    mock_session.post.return_value = mock_resp

    with patch("mcp_server_grc.cloud_inspector.get_authorized_session", return_value=(mock_session, "my-p")):
        res = inspect_project_iam_policy()
        assert res["status"] == "SUCCESS"
        assert res["compliance"]["status"] == "NON_COMPLIANT"
        assert len(res["compliance"]["violations"]) >= 2


def test_inspect_cloud_run_services():
    """Tests Cloud Run services inspection."""
    mock_session = MagicMock()
    mock_resp = MagicMock()
    mock_resp.status_code = 200
    mock_resp.json.return_value = {
        "services": [
            {
                "name": "projects/p/locations/us-central1/services/mcp-server-grc",
                "uri": "https://mcp-server-grc.run.app",
                "ingress": "INGRESS_TRAFFIC_ALL"
            }
        ]
    }
    mock_session.get.return_value = mock_resp

    with patch("mcp_server_grc.cloud_inspector.get_authorized_session", return_value=(mock_session, "my-p")):
        res = inspect_cloud_run_services()
        assert res["status"] == "SUCCESS"
        assert res["total_services"] == 1
        assert res["services"][0]["name"] == "mcp-server-grc"


def test_call_budget_exhaustion_returns_undetermined():
    """Verifies that exceeding the session call budget returns UNDETERMINED without continuing calls."""
    reset_session_call_budget("budget_test_session")
    mock_session = MagicMock()
    mock_resp = MagicMock()
    mock_resp.status_code = 200
    mock_resp.json.return_value = {
        "name": "projects/my-p/locations/global/keyRings/kr/cryptoKeys/key1",
        "rotationPeriod": "5184000s",
        "versionTemplate": {"protectionLevel": "HSM"},
    }
    mock_session.get.return_value = mock_resp

    with patch.dict("os.environ", {"MAX_LIVE_INSPECTION_CALLS_PER_SESSION": "2"}), \
         patch("mcp_server_grc.cloud_inspector.get_authorized_session", return_value=(mock_session, "my-p")):

        # Call 1: Under budget
        res1 = inspect_cloud_kms_key(
            "projects/my-p/locations/global/keyRings/kr/cryptoKeys/key1",
            session_id="budget_test_session"
        )
        assert res1["status"] == "FOUND"

        # Call 2: Reaches budget limit
        res2 = inspect_cloud_kms_key(
            "projects/my-p/locations/global/keyRings/kr/cryptoKeys/key1",
            session_id="budget_test_session"
        )
        assert res2["status"] == "FOUND"

        # Call 3: Budget exhausted -> Must return UNDETERMINED
        res3 = inspect_cloud_kms_key(
            "projects/my-p/locations/global/keyRings/kr/cryptoKeys/key1",
            session_id="budget_test_session"
        )
        assert res3["status"] == "UNDETERMINED"
        assert res3["compliance"]["status"] == "UNDETERMINED"
        assert any("budget" in v.lower() for v in res3["compliance"]["violations"])
        assert "exhausted" in res3["message"].lower()

        # Verify no further HTTP GET was executed on call 3 (only 2 calls reached the mock)
        assert mock_session.get.call_count == 2


def test_live_api_call_timeout_returns_undetermined():
    """Verifies that API timeouts return UNDETERMINED with actionable remediation."""
    reset_session_call_budget("timeout_test_session")
    mock_session = MagicMock()
    mock_session.get.side_effect = TimeoutError("Connection timed out after 10 seconds")

    with patch("mcp_server_grc.cloud_inspector.get_authorized_session", return_value=(mock_session, "my-p")):
        res = inspect_cloud_storage_bucket("my-timeout-bucket", session_id="timeout_test_session")
        assert res["status"] == "UNDETERMINED"
        assert res["compliance"]["status"] == "UNDETERMINED"
        assert any("timed out" in v.lower() for v in res["compliance"]["violations"])


def test_session_call_budget_counting_and_disclosure_statement():
    """Verifies session call counting and the exact disclosure statement format."""
    sid = "disclosure_test_session"
    reset_session_call_budget(sid)
    assert get_session_call_count(sid) == 0

    allowed1, c1, _ = check_and_increment_call_budget(sid)
    assert allowed1 is True
    assert c1 == 1

    allowed2, c2, _ = check_and_increment_call_budget(sid)
    assert allowed2 is True
    assert c2 == 2

    statement = get_session_disclosure_statement(sid)
    assert statement == "2 read-only API calls were made against your environment during this session."


def test_reset_session_call_budget():
    """Verifies that reset_session_call_budget properly clears counters."""
    sid = "reset_test_session"
    check_and_increment_call_budget(sid)
    check_and_increment_call_budget(sid)
    assert get_session_call_count(sid) == 2

    reset_session_call_budget(sid)
    assert get_session_call_count(sid) == 0

