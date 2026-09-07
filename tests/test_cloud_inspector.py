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
