"""Unit tests for ISO/IEC 27001:2022 Control A.8.12 Data Leakage Prevention (DLP)."""

import pytest
from mcp_server_grc.tools.data_leakage_prevention import audit_data_leakage_prevention


def test_dlp_perimeter_compliant():
    config = {
        "enforced": True,
        "restricted_services": [
            "storage.googleapis.com",
            "bigquery.googleapis.com",
            "aiplatform.googleapis.com",
        ],
        "egress_policies": [
            {
                "egress_to": {
                    "resources": ["projects/123456789/locations/us-central1"],
                    "operations": [{"service_name": "storage.googleapis.com"}],
                }
            }
        ],
    }
    result = audit_data_leakage_prevention("accessPolicies/1/servicePerimeters/prod", config)
    assert result["status"] == "COMPLIANT"
    assert len(result["violations"]) == 0
    assert result["control"] == "ISO/IEC 27001:2022 A.8.12"


def test_dlp_perimeter_dry_run_and_missing_services():
    config = {
        "enforced": False,  # Dry run
        "restricted_services": ["compute.googleapis.com"],  # missing storage and bigquery
        "egress_policies": [
            {
                "egress_to": {
                    "resources": ["*"],  # wildcard exfiltration risk
                }
            }
        ],
    }
    result = audit_data_leakage_prevention("accessPolicies/1/servicePerimeters/dev", config)
    assert result["status"] == "NON_COMPLIANT"
    assert len(result["violations"]) >= 3
    assert any("DRY-RUN mode" in v for v in result["violations"])
    assert any("core data services" in v for v in result["violations"])
    assert any("wildcard '*'" in v for v in result["violations"])
