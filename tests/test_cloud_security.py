"""Unit tests for ISO/IEC 27001:2022 Control A.5.23 Cloud Security Auditor."""

import pytest
from mcp_server_grc.tools.cloud_security import audit_cloud_security


def test_gcs_bucket_compliant():
    config = {
        "public_access_prevention": "enforced",
        "uniform_bucket_level_access": True,
        "kms_key_name": "projects/my-p/locations/us-central1/keyRings/kr/cryptoKeys/key1",
        "iam_bindings": [
            {"role": "roles/storage.objectViewer", "members": ["group:auditors@company.com"]}
        ],
    }
    result = audit_cloud_security("gcs_bucket", "secure-audit-bucket", config=config)
    assert result["status"] == "COMPLIANT"
    assert len(result["violations"]) == 0
    assert result["control"] == "ISO/IEC 27001:2022 A.5.23"


def test_gcs_bucket_public_access_violation():
    config = {
        "public_access_prevention": "inherited",
        "uniform_bucket_level_access": False,
        "iam_bindings": [
            {"role": "roles/storage.objectViewer", "members": ["allUsers"]}
        ],
    }
    result = audit_cloud_security("gcs_bucket", "leaky-bucket", config=config)
    assert result["status"] == "NON_COMPLIANT"
    assert any("Public Access Prevention" in v for v in result["violations"])
    assert any("Uniform Bucket-Level Access" in v for v in result["violations"])
    assert any("allUsers" in v for v in result["violations"])


def test_kms_key_rotation_compliant():
    config = {
        "rotation_period_seconds": 5184000,  # 60 days <= 90 days
        "protection_level": "HSM",
        "require_hsm": True,
    }
    result = audit_cloud_security("kms_key", "projects/p/locations/global/keyRings/r/cryptoKeys/k", config=config)
    assert result["status"] == "COMPLIANT"
    assert len(result["violations"]) == 0


def test_kms_key_rotation_exceeded():
    config = {
        "rotation_period_seconds": 15552000,  # 180 days > 90 days
        "protection_level": "SOFTWARE",
        "require_hsm": True,
    }
    result = audit_cloud_security("kms_key", "projects/p/locations/global/keyRings/r/cryptoKeys/k", config=config)
    assert result["status"] == "NON_COMPLIANT"
    assert any("rotation period" in v for v in result["violations"])
    assert any("HSM" in v for v in result["violations"])


def test_firewall_rule_unrestricted_ingress():
    config = {
        "direction": "INGRESS",
        "source_ranges": ["0.0.0.0/0"],
        "allowed": [{"ip_protocol": "tcp", "ports": [22, 80]}],
        "log_config": {"enable": False},
    }
    result = audit_cloud_security("firewall_rule", "allow-all-ssh", config=config)
    assert result["status"] == "NON_COMPLIANT"
    assert any("unrestricted 0.0.0.0/0 ingress to sensitive ports" in v for v in result["violations"])
    assert any("logging disabled" in v for v in result["violations"])


def test_iam_primitive_roles():
    config = {
        "bindings": [
            {"role": "roles/owner", "members": ["user:contractor@external.com"]},
            {"role": "roles/viewer", "members": ["group:engineering@company.com"]},
        ]
    }
    result = audit_cloud_security("iam_binding", "project-iam-policy", config=config)
    assert result["status"] == "NON_COMPLIANT"
    assert any("roles/owner" in v for v in result["violations"])
