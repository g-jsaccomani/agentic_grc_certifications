"""Unit tests for ISO/IEC 27001:2022 Control A.5.7 Threat Intelligence Correlation."""

import pytest
from mcp_server_grc.tools.threat_intel import correlate_threat_intelligence


def test_threat_intel_compliant():
    events = [
        {"caller_ip": "10.0.0.15", "principal_email": "ci-builder@company.iam.gserviceaccount.com", "method_name": "storage.objects.get"}
    ]
    result = correlate_threat_intelligence(
        log_sink_name="audit-logs-sink",
        sink_destination="bigquery.googleapis.com/projects/p/datasets/audit_logs",
        recent_events=events,
        threat_feed_enabled=True,
    )
    assert result["status"] == "COMPLIANT"
    assert result["matched_threats_count"] == 0
    assert len(result["violations"]) == 0


def test_threat_intel_ioc_detected():
    events = [
        {
            "caller_ip": "198.51.100.24",  # Mandiant UNC3886 IOC
            "principal_email": "compromised-user@company.com",
            "method_name": "cloudkms.cryptoKeyVersions.destroy",
            "timestamp": "2026-09-03T12:00:00Z",
        }
    ]
    result = correlate_threat_intelligence(
        log_sink_name="audit-logs-sink",
        sink_destination="bigquery.googleapis.com/projects/p/datasets/audit_logs",
        recent_events=events,
        threat_feed_enabled=True,
    )
    assert result["status"] == "NON_COMPLIANT"
    assert result["matched_threats_count"] == 1
    match = result["matched_threats"][0]
    assert match["threat_actor"] == "UNC3886"
    assert match["threat_source"] == "Mandiant Threat Intelligence"


def test_threat_intel_feed_disabled():
    result = correlate_threat_intelligence(
        log_sink_name="sink1",
        sink_destination="bigquery.googleapis.com/p/d",
        threat_feed_enabled=False,
    )
    assert result["status"] == "NON_COMPLIANT"
    assert any("Threat intelligence feeds" in v for v in result["violations"])


def test_threat_intel_invalid_destination():
    result = correlate_threat_intelligence(
        log_sink_name="sink1",
        sink_destination="pubsub.googleapis.com/unverified-topic",
        threat_feed_enabled=True,
    )
    assert result["status"] == "NON_COMPLIANT"
    assert any("not routed to a persistent compliant store" in v for v in result["violations"])
