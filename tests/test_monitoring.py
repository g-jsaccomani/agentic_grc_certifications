"""Unit tests for ISO/IEC 27001:2022 Control A.8.16 Monitoring Activities."""

import pytest
from mcp_server_grc.tools.monitoring import audit_monitoring_activities


def test_monitoring_activities_compliant():
    config = {
        "sinks": [
            {"name": "bq-sink", "destination": "bigquery.googleapis.com/projects/p/datasets/audit"}
        ],
        "data_access_logs_enabled": True,
        "retention_days": 400,
        "alert_policies": ["iam_change", "firewall_change", "kms_destruction"],
    }
    result = audit_monitoring_activities("prod-project-123", config)
    assert result["status"] == "COMPLIANT"
    assert len(result["violations"]) == 0
    assert result["control"] == "ISO/IEC 27001:2022 A.8.16"


def test_monitoring_activities_violations():
    config = {
        "sinks": [
            {"name": "storage-sink", "destination": "storage.googleapis.com/unmonitored-bucket"}
        ],
        "data_access_logs_enabled": False,
        "retention_days": 90,  # < 365
        "alert_policies": ["cpu_utilization"],  # missing required security alert types
    }
    result = audit_monitoring_activities("dev-project-456", config)
    assert result["status"] == "NON_COMPLIANT"
    assert any("lacks centralized log export" in v for v in result["violations"])
    assert any("Data Access Audit Logging is disabled" in v for v in result["violations"])
    assert any("less than required 365 days" in v for v in result["violations"])
    assert any("Missing automated alerts" in v for v in result["violations"])
