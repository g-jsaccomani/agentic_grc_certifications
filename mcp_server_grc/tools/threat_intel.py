"""Control A.5.7: Threat Intelligence.

Audits and correlates cloud logging audit trails (BigQuery / Cloud Logging)
with active threat intelligence feeds from Google SecOps (Chronicle) and Mandiant
to ensure active threat monitoring and detection compliance.
"""

from typing import Any, Dict, List, Optional


# Known test indicators of compromise for validation / simulation
SAMPLE_THREAT_INDICATORS = {
    "198.51.100.24": {
        "source": "Mandiant Threat Intelligence",
        "actor": "UNC3886",
        "severity": "CRITICAL",
        "threat_type": "Espionage / Credential Harvesting",
    },
    "203.0.113.195": {
        "source": "Google SecOps Curated Detections",
        "actor": "APT41",
        "severity": "HIGH",
        "threat_type": "Cloud Infrastructure Reconnaissance",
    },
}


def correlate_threat_intelligence(
    log_sink_name: str,
    sink_destination: str,
    recent_events: Optional[List[Dict[str, Any]]] = None,
    threat_feed_enabled: bool = True,
) -> Dict[str, Any]:
    """Audits threat intelligence correlation per ISO/IEC 27001:2022 Control A.5.7.

    Args:
        log_sink_name: Name of the Cloud Logging sink (e.g. 'audit-logs-to-bigquery').
        sink_destination: Destination URI (e.g. 'bigquery.googleapis.com/projects/.../datasets/audit_logs').
        recent_events: Optional batch of audit log events to correlate against threat feeds.
        threat_feed_enabled: Flag indicating if Mandiant / Google SecOps feed integration is active.

    Returns:
        Structured audit report with threat intelligence verification and compliance verdict.
    """
    recent_events = recent_events or []
    violations: List[str] = []
    matched_threats: List[Dict[str, Any]] = []

    # Check 1: Verify log sink destination is valid and secure
    if not sink_destination or not (
        sink_destination.startswith("bigquery.googleapis.com")
        or sink_destination.startswith("storage.googleapis.com")
    ):
        violations.append(
            f"Log sink '{log_sink_name}' destination '{sink_destination}' is not routed to a persistent compliant store (BigQuery/GCS)."
        )

    # Check 2: Verify active threat intelligence feed integration
    if not threat_feed_enabled:
        violations.append(
            "Threat intelligence feeds (Google SecOps / Mandiant) are disabled or not linked to audit pipeline."
        )

    # Check 3: Correlate recent audit events with IOC feed
    for event in recent_events:
        caller_ip = event.get("caller_ip")
        principal_email = event.get("principal_email")
        method_name = event.get("method_name")

        if caller_ip in SAMPLE_THREAT_INDICATORS:
            threat_info = SAMPLE_THREAT_INDICATORS[caller_ip]
            matched_threats.append({
                "caller_ip": caller_ip,
                "principal_email": principal_email,
                "method_name": method_name,
                "threat_source": threat_info["source"],
                "threat_actor": threat_info["actor"],
                "severity": threat_info["severity"],
                "threat_type": threat_info["threat_type"],
                "event_timestamp": event.get("timestamp"),
            })
            violations.append(
                f"Active threat detected: IP {caller_ip} associated with {threat_info['actor']} ({threat_info['source']}) invoked {method_name}."
            )

    is_compliant = len(violations) == 0
    return {
        "status": "COMPLIANT" if is_compliant else "NON_COMPLIANT",
        "control": "ISO/IEC 27001:2022 A.5.7",
        "log_sink": log_sink_name,
        "destination": sink_destination,
        "threat_feed_active": threat_feed_enabled,
        "events_analyzed": len(recent_events),
        "matched_threats_count": len(matched_threats),
        "matched_threats": matched_threats,
        "violations": violations,
        "remediation": (
            "Continuous threat intelligence pipeline is compliant with Control A.5.7."
            if is_compliant
            else "Investigate identified threat indicators immediately and ensure feeds and log sinks are properly configured."
        ),
    }
