"""Memory Bank & Persistent State Layer for GEAP.

Persists organizational context, historical compliance baselines,
remediation velocity, and temporal drift vectors across audit cycles.
"""

import time
from dataclasses import asdict, dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class AuditCycleRecord:
    cycle_id: str
    timestamp: float
    score: float
    rating: str
    total_controls: int
    non_compliant_controls: List[str]
    remediated_controls: List[str] = field(default_factory=list)


class MemoryBank:
    """Persistent state and organizational context store for GEAP Orchestrator."""

    def __init__(self, organization_name: str = "Enterprise-Client"):
        self.organization_name = organization_name
        self.organizational_profile: Dict[str, Any] = {
            "primary_cloud": "Google Cloud Platform",
            "critical_regions": ["us-central1", "us-east4"],
            "data_sensitivity_level": "RESTRICTED",
            "regulatory_frameworks": ["ISO/IEC 27001:2022", "ISO/IEC 27001 Amd 1:2024"],
        }
        self.audit_history: List[AuditCycleRecord] = []
        self.recurring_violations: Dict[str, int] = {}  # control_id -> frequency count

    def record_audit_cycle(
        self,
        cycle_id: str,
        score: float,
        rating: str,
        total_controls: int,
        non_compliant_controls: List[str],
        remediated_controls: Optional[List[str]] = None,
    ) -> AuditCycleRecord:
        """Records the results of an audit execution cycle and updates recurring drift statistics."""
        record = AuditCycleRecord(
            cycle_id=cycle_id,
            timestamp=time.time(),
            score=score,
            rating=rating,
            total_controls=total_controls,
            non_compliant_controls=non_compliant_controls,
            remediated_controls=remediated_controls or [],
        )
        self.audit_history.append(record)

        # Track frequency of recurring non-compliances
        for ctrl in non_compliant_controls:
            self.recurring_violations[ctrl] = self.recurring_violations.get(ctrl, 0) + 1

        return record

    def calculate_drift_trend(self) -> Dict[str, Any]:
        """Analyzes historical cycles to calculate compliance velocity and drift trajectory."""
        if not self.audit_history:
            return {
                "cycles_recorded": 0,
                "trend": "NO_DATA",
                "score_delta": 0.0,
                "recurring_hotspots": [],
            }

        if len(self.audit_history) == 1:
            return {
                "cycles_recorded": 1,
                "trend": "BASELINE_ESTABLISHED",
                "current_score": self.audit_history[-1].score,
                "score_delta": 0.0,
                "recurring_hotspots": list(self.recurring_violations.keys()),
            }

        first_score = self.audit_history[0].score
        latest_score = self.audit_history[-1].score
        delta = round(latest_score - first_score, 2)

        if delta > 0:
            trend = "IMPROVING"
        elif delta < 0:
            trend = "DEGRADING"
        else:
            trend = "STABLE"

        # Hotspots: controls violating in > 50% of cycles
        cycles_count = len(self.audit_history)
        hotspots = [
            ctrl for ctrl, count in self.recurring_violations.items()
            if (count / cycles_count) >= 0.5
        ]

        return {
            "cycles_recorded": cycles_count,
            "trend": trend,
            "first_score": first_score,
            "latest_score": latest_score,
            "score_delta": delta,
            "recurring_hotspots": hotspots,
        }

    def get_state_snapshot(self) -> Dict[str, Any]:
        """Exports complete state for GEAP context hydration."""
        return {
            "organization_name": self.organization_name,
            "profile": self.organizational_profile,
            "total_audit_cycles": len(self.audit_history),
            "drift_trend": self.calculate_drift_trend(),
            "recurring_violations": self.recurring_violations,
        }
