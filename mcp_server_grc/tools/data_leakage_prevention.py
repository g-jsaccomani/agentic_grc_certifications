"""Control A.8.12: Data Leakage Prevention (DLP).

Audits network security perimeters (VPC Service Controls), egress rule enforcement,
and measures to prevent unauthorized data exfiltration from GCP services.
"""

from typing import Any, Dict, List, Optional


def audit_data_leakage_prevention(
    perimeter_name: str,
    perimeter_config: Optional[Dict[str, Any]] = None,
    bearer_token: Optional[str] = None,
) -> Dict[str, Any]:
    """Audits VPC Service Controls (VPC-SC) perimeters against ISO/IEC 27001:2022 Control A.8.12.

    Args:
        perimeter_name: Name of the VPC Service Controls perimeter (e.g. 'accessPolicies/.../servicePerimeters/prod_perimeter').
        perimeter_config: Dictionary containing perimeter status, restricted services, egress/ingress rules.
        bearer_token: Delegated user OAuth token for live Cloud API queries if needed.

    Returns:
        Structured audit finding with DLP / VPC-SC compliance verdict and remediation.
    """
    perimeter_config = perimeter_config or {}
    violations: List[str] = []
    evidence: Dict[str, Any] = {
        "perimeter_name": perimeter_name,
        "control": "ISO/IEC 27001:2022 A.8.12",
    }

    # Check 1: Perimeter Enforcement Status
    enforced = perimeter_config.get("enforced", True)
    evidence["enforced"] = enforced
    if not enforced:
        violations.append(
            f"VPC-SC Perimeter '{perimeter_name}' is in DRY-RUN mode or disabled. Active enforcement is required."
        )

    # Check 2: Core Data Services Protected
    restricted_services = set(perimeter_config.get("restricted_services", []))
    evidence["restricted_services"] = list(restricted_services)
    mandatory_services = {
        "storage.googleapis.com",
        "bigquery.googleapis.com",
    }
    missing_services = mandatory_services.difference(restricted_services)
    if missing_services:
        violations.append(
            f"Perimeter '{perimeter_name}' does not restrict core data services: {list(missing_services)}."
        )

    # Check 3: Egress Rules (Data Exfiltration Boundary)
    egress_policies = perimeter_config.get("egress_policies", [])
    evidence["egress_policies_count"] = len(egress_policies)
    for policy in egress_policies:
        to_rule = policy.get("egress_to", {})
        resources = to_rule.get("resources", [])
        if "*" in resources:
            violations.append(
                f"Perimeter '{perimeter_name}' defines wildcard '*' egress resource target. Permits exfiltration outside authorized perimeter."
            )

    is_compliant = len(violations) == 0
    return {
        "status": "COMPLIANT" if is_compliant else "NON_COMPLIANT",
        "control": "ISO/IEC 27001:2022 A.8.12",
        "perimeter_name": perimeter_name,
        "violations": violations,
        "evidence": evidence,
        "remediation": (
            "VPC-SC perimeter is fully compliant with ISO 27001:2022 A.8.12 DLP requirements."
            if is_compliant
            else "Enforce perimeter, include storage/bigquery in restricted services, and restrict egress rules."
        ),
    }
