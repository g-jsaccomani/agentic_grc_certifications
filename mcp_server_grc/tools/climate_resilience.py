"""ISO/IEC 27001:2022 / Amd 1:2024 (Climate Action Amendment).

Audits ISMS Clauses 4.1 & 4.2 and business continuity resilience:
- Geographic distribution of critical cloud assets (multi-region / dual-region).
- Active-active or automated failover capabilities.
- Climate risk assessment & extreme weather disaster recovery preparedness.
"""

from typing import Any, Dict, List, Optional


def audit_climate_resilience(
    workload_id: str,
    topology: Dict[str, Any],
    climate_risk_assessed: bool = True,
) -> Dict[str, Any]:
    """Audits cloud architecture resilience against climate events (ISO 27001 Amd 1:2024).

    Args:
        workload_id: Identifier of the critical workload or application service.
        topology: Dictionary containing deployment regions, failover mechanisms, and backup strategies.
                  Example:
                  {
                      "primary_region": "us-central1",
                      "secondary_region": "us-east4",
                      "storage_redundancy": "multi-region", # or "dual-region", "single-region"
                      "automated_failover": True,
                      "rto_minutes": 15,
                      "rpo_minutes": 5
                  }
        climate_risk_assessed: Whether climate risk factors were explicitly documented in Clauses 4.1/4.2.

    Returns:
        Structured compliance report under ISO 27001:2022 / Amd 1:2024.
    """
    violations: List[str] = []
    recommendations: List[str] = []

    primary_region = topology.get("primary_region", "")
    secondary_region = topology.get("secondary_region")
    storage_redundancy = topology.get("storage_redundancy", "single-region").lower()
    automated_failover = topology.get("automated_failover", False)
    rto_minutes = topology.get("rto_minutes", 120)
    rpo_minutes = topology.get("rpo_minutes", 60)

    # Check 1: Mandatory ISO 27001 Amd 1:2024 Clause 4.1 Climate Context Assessment
    if not climate_risk_assessed:
        violations.append(
            f"Workload '{workload_id}' lacks explicit climate change risk assessment in ISMS Clause 4.1 context documentation."
        )
        recommendations.append(
            "Document climate risk factors (extreme weather, regional grid stress, flood zones) in organizational context register."
        )

    # Check 2: Single Region Risk (SPOF)
    if not secondary_region or secondary_region == primary_region:
        violations.append(
            f"Critical workload '{workload_id}' is deployed in a single region ({primary_region}) without regional redundancy."
        )
        recommendations.append(
            "Configure a secondary disaster recovery region (e.g. cross-region replica or active-active multi-region)."
        )

    # Check 3: Storage Redundancy
    if storage_redundancy == "single-region":
        violations.append(
            f"Storage for workload '{workload_id}' uses 'single-region' redundancy, vulnerable to localized regional disaster."
        )
        recommendations.append(
            "Upgrade critical storage to dual-region or multi-region bucket configurations."
        )

    # Check 4: Automated Failover
    if not automated_failover:
        violations.append(
            f"Workload '{workload_id}' does not have automated regional failover enabled."
        )
        recommendations.append(
            "Implement automated health-check routing (e.g., Cloud Load Balancing with cross-region failover backends)."
        )

    # Check 5: RTO / RPO sanity check for critical services
    if rto_minutes > 60:
        recommendations.append(
            f"Current Recovery Time Objective ({rto_minutes} min) is high for tier-1 service. Target RTO <= 60 minutes."
        )

    is_compliant = len(violations) == 0
    return {
        "status": "COMPLIANT" if is_compliant else "NON_COMPLIANT",
        "standard": "ISO/IEC 27001:2022 + Amd 1:2024",
        "clauses": ["4.1", "4.2", "A.8.14", "A.5.30"],
        "workload_id": workload_id,
        "metrics": {
            "primary_region": primary_region,
            "secondary_region": secondary_region,
            "geographic_redundancy": "MULTI_REGION" if secondary_region else "SINGLE_REGION",
            "storage_redundancy": storage_redundancy,
            "automated_failover": automated_failover,
            "rto_minutes": rto_minutes,
            "rpo_minutes": rpo_minutes,
            "climate_risk_assessed": climate_risk_assessed,
        },
        "violations": violations,
        "recommendations": recommendations,
        "verdict": (
            "Architecture satisfies ISO 27001:2022 Amd 1:2024 Climate Resilience criteria."
            if is_compliant
            else f"Identified {len(violations)} climate resilience defect(s) requiring remediation."
        ),
    }
