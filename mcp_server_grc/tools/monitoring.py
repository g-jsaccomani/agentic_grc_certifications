"""Control A.8.16: Monitoring Activities.

Audits continuous monitoring capabilities:
- Ingestion of audit trails into BigQuery or Google SecOps (Chronicle)
- Log retention compliance (minimum 365 days)
- Coverage of Admin Activity and Data Access logging
- Security alert configurations
"""

from typing import Any, Dict, List, Optional


def audit_monitoring_activities(
    project_id: str,
    monitoring_config: Optional[Dict[str, Any]] = None,
    bearer_token: Optional[str] = None,
) -> Dict[str, Any]:
    """Audits centralized logging and monitoring against ISO/IEC 27001:2022 Control A.8.16.

    Args:
        project_id: GCP Project ID being audited.
        monitoring_config: Dictionary detailing log sinks, retention, and security alert policies.
        bearer_token: Delegated user OAuth token for live Cloud API queries if needed.

    Returns:
        Structured audit finding with monitoring activities compliance verdict and evidence.
    """
    monitoring_config = monitoring_config or {}
    violations: List[str] = []
    evidence: Dict[str, Any] = {
        "project_id": project_id,
        "control": "ISO/IEC 27001:2022 A.8.16",
    }

    # Check 1: Centralized Destination (BigQuery or Google SecOps)
    sinks = monitoring_config.get("sinks", [])
    has_centralized_sink = False
    valid_dest_prefixes = ("bigquery.googleapis.com", "chronicle.security", "secops.googleapis.com")

    for sink in sinks:
        dest = sink.get("destination", "")
        if any(dest.startswith(prefix) for prefix in valid_dest_prefixes):
            has_centralized_sink = True
            break

    evidence["centralized_sink_active"] = has_centralized_sink
    if not has_centralized_sink:
        violations.append(
            f"Project '{project_id}' lacks centralized log export to BigQuery or Google SecOps (Chronicle)."
        )

    # Check 2: Data Access Logging
    data_access_enabled = monitoring_config.get("data_access_logs_enabled", True)
    evidence["data_access_logs_enabled"] = data_access_enabled
    if not data_access_enabled:
        violations.append(
            f"Data Access Audit Logging is disabled or incomplete for critical services in project '{project_id}'."
        )

    # Check 3: Retention Period (>= 365 days required for ISO audit trail compliance)
    retention_days = monitoring_config.get("retention_days", 365)
    evidence["retention_days"] = retention_days
    if retention_days < 365:
        violations.append(
            f"Log retention period ({retention_days} days) is less than required 365 days for regulatory audit trails."
        )

    # Check 4: Real-time Alerting Coverage
    alert_policies = monitoring_config.get("alert_policies", [])
    evidence["alert_policies_count"] = len(alert_policies)
    required_alert_types = {"iam_change", "firewall_change", "kms_destruction"}
    configured_alerts = set(alert_policies)
    missing_alerts = required_alert_types.difference(configured_alerts)
    if missing_alerts:
        violations.append(
            f"Missing automated alerts for critical events: {list(missing_alerts)}."
        )

    is_compliant = len(violations) == 0
    return {
        "status": "COMPLIANT" if is_compliant else "NON_COMPLIANT",
        "control": "ISO/IEC 27001:2022 A.8.16",
        "project_id": project_id,
        "violations": violations,
        "evidence": evidence,
        "remediation": (
            "Monitoring activities comply with ISO 27001:2022 Control A.8.16."
            if is_compliant
            else "Configure centralized BigQuery/SecOps sink, enable data access logs, set retention >= 365 days, and configure critical alerts."
        ),
    }
