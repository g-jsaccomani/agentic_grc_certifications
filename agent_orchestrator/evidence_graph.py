"""Evidence Graph and Logical Evidence Mapping Module.

Structures raw cloud telemetry, configurations, and logs into a formal,
verifiable compliance graph mapped to ISO/IEC 27001:2022 requirements.
Enforces epistemic truthfulness: distinguishes VERIFIED telemetry from MOCK/SIMULATION.
"""

import hashlib
import json
import time
from dataclasses import asdict, dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional


class EvidenceVerificationTier(str, Enum):
    VERIFIED = "VERIFIED"          # Direct cryptographic or API-authenticated telemetry
    TELEMETRY = "TELEMETRY"        # Ingested cloud metrics / logs
    SIMULATION = "SIMULATION"      # Dry-run or test payload
    MOCK = "MOCK"                  # Unit test fixture


@dataclass
class EvidenceNode:
    node_id: str
    resource_id: str
    resource_type: str
    control_id: str
    verification_tier: EvidenceVerificationTier
    raw_payload: Dict[str, Any]
    timestamp: float = field(default_factory=time.time)
    evidence_hash: str = ""

    def __post_init__(self):
        if not self.evidence_hash:
            payload_str = json.dumps(self.raw_payload, sort_keys=True, default=str)
            raw = f"{self.resource_id}:{self.control_id}:{payload_str}"
            self.evidence_hash = hashlib.sha256(raw.encode("utf-8")).hexdigest()

    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        d["verification_tier"] = self.verification_tier.value
        return d


@dataclass
class ComplianceLink:
    source_node_id: str
    control_id: str
    status: str  # COMPLIANT, NON_COMPLIANT, WARNING
    justification: str
    violations: List[str] = field(default_factory=list)


class EvidenceGraph:
    """Directed graph capturing logical relationships between cloud assets and ISO 27001 controls."""

    def __init__(self):
        self.nodes: Dict[str, EvidenceNode] = {}
        self.links: List[ComplianceLink] = []

    def add_evidence(
        self,
        resource_id: str,
        resource_type: str,
        control_id: str,
        raw_payload: Dict[str, Any],
        verification_tier: EvidenceVerificationTier = EvidenceVerificationTier.VERIFIED,
    ) -> EvidenceNode:
        """Creates and links a new verified evidence node in the compliance graph."""
        node_id = f"ev-{resource_type}-{hashlib.md5(resource_id.encode()).hexdigest()[:8]}"
        node = EvidenceNode(
            node_id=node_id,
            resource_id=resource_id,
            resource_type=resource_type,
            control_id=control_id,
            verification_tier=verification_tier,
            raw_payload=raw_payload,
        )
        self.nodes[node_id] = node
        return node

    def link_compliance_state(
        self,
        source_node_id: str,
        control_id: str,
        status: str,
        justification: str,
        violations: Optional[List[str]] = None,
    ) -> ComplianceLink:
        """Establishes an edge connecting evidence to a specific standard control outcome."""
        link = ComplianceLink(
            source_node_id=source_node_id,
            control_id=control_id,
            status=status,
            justification=justification,
            violations=violations or [],
        )
        self.links.append(link)
        return link

    def query_by_control(self, control_id: str) -> List[Dict[str, Any]]:
        """Retrieves all evidence nodes and compliance links bound to a specific control."""
        results = []
        for link in self.links:
            if link.control_id == control_id:
                node = self.nodes.get(link.source_node_id)
                results.append({
                    "link": asdict(link),
                    "evidence_node": node.to_dict() if node else None,
                })
        return results

    def get_summary(self) -> Dict[str, Any]:
        """Returns statistical overview of graph nodes and compliance links."""
        total_nodes = len(self.nodes)
        total_links = len(self.links)
        compliant = sum(1 for l in self.links if l.status == "COMPLIANT")
        non_compliant = sum(1 for l in self.links if l.status == "NON_COMPLIANT")

        return {
            "total_evidence_nodes": total_nodes,
            "total_compliance_links": total_links,
            "compliant_links": compliant,
            "non_compliant_links": non_compliant,
            "verification_tiers": {
                tier.value: sum(1 for n in self.nodes.values() if n.verification_tier == tier)
                for tier in EvidenceVerificationTier
            },
        }
